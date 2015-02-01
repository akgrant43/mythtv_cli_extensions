#!/usr/bin/env python3

import argparse
import logging.config
import sys
from lxml.etree import parse
from os.path import exists, join, isdir, abspath, dirname, realpath, basename

# Try and ensure imports will work in development workspace
mydir = dirname(realpath(__file__))
proposed_path = abspath(join(mydir, '..'))
if isdir(join(proposed_path, 'mythtvlib')) and (proposed_path not in sys.path):
    sys.path.append(proposed_path)

from mythtvlib.services import MythTVService
from mythtvlib.object import MythTVObject

try:
    from mythtv_chanmaint_settings import *
except:
    from mythtv_chanmaint_default import *

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)



class MaintenanceException(Exception):
    pass


class MythTVChannelMaintenance(object):
    
    def __init__(self, args):
        self.args = args
        self._xmltv_data = None
        self._callsign_map = None
        self._channel_client = None
        return

    def require_xmltv(self):
        "Check that the XMLTV file name has been supplied and exists"
        if self.args.xmltv is None:
            msg = "--xmltv not specified"
            print(msg)
            exit(0)
        if not exists(self.args.xmltv):
            msg = "{0} doesn't exist".format(self.args.xmltv)
            print(msg)
            exit(0)
        return

    def execute(self):
        "Execute the requested command"
        getattr(self, self.args.command)(self.args.params)
        return

    def list(self, param):
        "List the XMLTV or MythTV channel data"
        if param == "xmltv":
            self.list_xmltv()
        elif param == "channels":
            self.list_channels()
        else:
            raise MaintenanceException("Unknown list parameter: {0}".format(param))
        return

    @property
    def channel_client(self):
        "Answer a suds client for the Channel service"
        if self._channel_client is not None:
            return self._channel_client
        self._channel_client = MythTVService('Channel',
                                   hostname=self.args.hostname,
                                   port=self.args.port)
        return self._channel_client

    def videosources(self):
        """Iterate over all videosources in the backend"""
        video_services = self.channel_client.service.GetVideoSourceList()
        for vss in video_services.VideoSources:
            yield vss[1]
        return

    def channels(self, videosource_id):
        """Iterate over all channels in the specified videosource id"""
        channels = self.channel_client.service.GetChannelInfoList(videosource_id)
        # channels is a ChannelInfoList
        # channels.ChannelInfos is ArrayOfChannelInfo,
        # which is a an array like object with one entry,
        # a list of ChannelInfo
        for channel in channels.ChannelInfos[0]:
            yield channel
        return        

    def all_channels(self):
        "Iterate over all channels, i.e. over all videosources"
        for vss in self.videosources():
            for vs in vss:
                for channel in self.channels(vs.Id):
                    yield channel
        return

    def list_channels(self):
        "List the MythTV Channels"

        fmt_string = "{id:<5} {callsign:<20} {channum:<7} {name:<20} {visible:<7} {xmltvid:<20} {icon:<20}"
        #import pdb; pdb.set_trace()
        for vss in self.videosources():
            # VideoSources is ... 
            for vs in vss:
                source_id = vs.Id
                print("Video Source: {0}".format(vs.SourceName))
                print("="*105)
                print(fmt_string.format(
                        id="Id",
                        callsign="CallSign",
                        channum="ChanNum",
                        name="Name",
                        visible="Visible",
                        xmltvid="XMLTVID",
                        icon="Icon URL"))
                print('-'*90)
                for channel in self.channels(source_id):
                    print(fmt_string.format(
                        id=channel.ChanId,
                        callsign=channel.CallSign,
                        channum=channel.ChanNum,
                        name=channel.ChannelName,
                        visible=channel.Visible,
                        xmltvid=channel.XMLTVID or "",
                        icon=channel.IconURL or ""))
                print("")
        return

    @property
    def xmltv_data(self):
        """Answer a dictionary of callsign->xmltvid
        from the specificed xmltv file."""
        if self._xmltv_data is not None:
            return self._xmltv_data
        
        self.require_xmltv()
        self._xmltv_data = {}
        tree = parse(self.args.xmltv)
        channels = tree.findall(".//channel")
        for channel in channels:
            display_name = channel.find(".//display-name")
            self._xmltv_data[display_name.text] = channel.get('id')
        return self._xmltv_data

    def list_xmltv(self):
        "List the XMLTV channels"
        fmt_string = "{callsign:<20} {xmltvid:<64}"
        print(fmt_string.format(
                callsign="CallSign",
                xmltvid="XMLTVID"))
        print('-'*41)
        channels = list(self.xmltv_data.keys())
        channels.sort()
        for channel in channels:
            print(fmt_string.format(
                callsign=channel,
                xmltvid=self.xmltv_data[channel]))
        return

    @property
    def callsign_map(self):
        """Answer a dictionary mapping all callsign variations to the
        appropriate XMLTVID."""
        if self._callsign_map is not None:
            return self._callsign_map
        if len(XMLTV_CALLSIGNS) == 0:
            logger.warn("CallSign mapping is empty."
                "  This normally should be configured in mythtv_chanmaint_settings.py")
        self._callsign_map = {}
        # Ensure that the callsigns in the XMLTV file map to themselves
        for callsign, xmltvid in self.xmltv_data.items():
            self._callsign_map[callsign] = xmltvid
            alternates = XMLTV_CALLSIGNS.get(callsign)
            if alternates is not None:
                for alternate in alternates:
                    self._callsign_map[alternate] = xmltvid
        return self._callsign_map

    def update_xmltvids(self, empty):
        """Update the Channel database from the supplied XMLTV file."""
        csmap = self.callsign_map
        proposed_changes = []
        # proposed_changes is a list of tuples:
        #    (ChanID, CallSign, New XMLTVID)
        for channel in self.all_channels():
            new_xmltvid = csmap.get(channel.CallSign)
            if new_xmltvid is None:
                continue
            if self.args.replace or (new_xmltvid != channel.XMLTVID):
                proposed_changes.append((channel.ChanId, channel.CallSign, new_xmltvid))
        if len(proposed_changes) == 0:
            logging.info("update_xmltvids: no updates required")
            return
        if self.args.yes:
            proceed = True
        else:
            # List the proposed changes and request confirmation
            fmt_string = "{id:<6} {callsign:<20} {xmltvid:<64}"
            print(fmt_string.format(
                id="Id",
                callsign="CallSign",
                xmltvid="XMLTVID"))
            print('-'*85)
            for proposed in proposed_changes:
                print(fmt_string.format(
                    id=proposed[0],
                    callsign=proposed[1],
                    xmltvid=proposed[2]))
            answer = input("Proceed [y/N]? ")
            proceed = answer.lower() in ["y", "yes"]
        if proceed:
            for proposed in proposed_changes:
                old_xmltvid = channel.XMLTVID
                channel = MythTVObject('Channel', [proposed[0]],
                                       self.args.hostname, self.args.port)
                channel.XMLTVID = proposed[2]
                channel.save()
                logging.info("ChanID: {callsign} ({cid}): XMLTVID {old} -> {new}".format(
                        callsign=proposed[1],
                        cid=proposed[0],
                        old=old_xmltvid,
                        new=proposed[2]))
        return
 


def main():
    logger.debug("Starting")
    services_string = ", ".join(MythTVService.services)
    epilog = """
{prog} has 3 basic use cases:

    {prog} list xmltv --xmltv file.name
        List the channel and XMLTVID data contained in the xmltv file
    {prog} list channels
        List the channel data contained in the MythTV backend
    {prog} update_xmltvids --xmltv file.name [-y] [--replace]
        Update Channel XMLTVIDs, see below

Updating Channel XMLTVIDs
-------------------------

This option can be used to re-populate and correct XMLTVIDs in the Backend
database.

It reads the XMLTVIDs from the supplied file (--xmltv file.name), creates a
mapping from all CallSign variations as defined in the users settings file
(mythtv_chanmaint_settings.py) and reads and checks each channel in the 
backend.  If -y is not supplied the proposed updates are listed and the user
is asked for confirmation prior to updating the backend.



Typical Workflow
----------------

The typical workflow is to recognise that you aren't getting EPG data for all
your channels, or that you need to re-scan for whatever reason.

1. Get a copy of the XMLTV EPG data.  Hopefully you know how this is done
   already.  The program data isn't needed, just the channel data.
   For my system:

   $ tv_grab_huro --days 1 --offset 0 --output xmltv.xml --config ~/.mythtv/tv_grab.xmltv

2. List the xmltv callsigns:

   $ mythtv_chanmaint.py list xmltv --xmltv xmltv.xml

3. List the MythTV callsigns:

   $ mythtv_chanmaint.py list channels --host backend.host.name

4. Update the mapping table in mythtv_chanmaint_settings.py (XMLTV_CALLSIGNS).

   Note that the callsign as it exists in the xmltv file is the key
   (left of the colon), and the MythTV callsign is the value (right of the
   colon).

   See mythtv_chanmaint_example.py for an example configuration with some
   comments.

5. Run the update:

   $ mythtv_chanmaint.py update_xmltvids --host backend.host.name

   Check the proposed updates and confirm if you're happy.  If not, go back
   to step 4 and check the mapping table.

6. Run mythfilldatabase

   You should then be able to see the correct / additional EPG data in the
   MythTV program guide.
   
""".format(
            services=services_string,
            prog=basename(sys.argv[0]))
    parser = argparse.ArgumentParser(description="MythTV Channel Maintenance",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=epilog)
    parser.add_argument('--xmltv',
                        default=None,
                        help='XMLTV data file')
    parser.add_argument('--hostname',
                        default="localhost",
                        help='MythTV Backend hostname (localhost)')
    parser.add_argument('--server-port', dest='port',
                        default="6544",
                        help="MythTV Backend services port (6544)")
    parser.add_argument('--frontend-port',
                        default="1234",
                        help="MythTV Frontend services port (1234)")
    parser.add_argument('--config',
                        default="mythtv_chanmaint.dat",
                        help="Configuration data")
    parser.add_argument('--create-config', action='store_true',
                        default=False,
                        help="Create a new configuration data file")
    parser.add_argument('-y', action='store_true',
                        dest='yes',
                        default=False,
                        help="Execute updates without user confirmation")
    parser.add_argument('command',
                        choices=['list', 'update_xmltvids'],
                        help="Maintenance command, see below")
    parser.add_argument('params',
                        nargs='?',
                        help="Command parameter")
    args = parser.parse_args()

    maint = MythTVChannelMaintenance(args)
    maint.execute()
    logger.debug("Done")

    return


if __name__ == "__main__":
    main()
