#!/usr/bin/env python3

import argparse
import logging.config
import sys
from lxml.etree import parse
from os.path import exists, join, isdir, abspath, dirname, realpath, basename
from urllib.error import URLError

# Try and ensure imports will work in development workspace
mydir = dirname(realpath(__file__))
proposed_path = abspath(join(mydir, '..'))
if isdir(join(proposed_path, 'mythtvlib')) and (proposed_path not in sys.path):
    sys.path.append(proposed_path)

from mythtvlib import __VERSION__
from mythtvlib.backend import MythTVBackend
from mythtvlib.query import MythTVQuerySet

from mythtvlib.settings import settings

logging.config.dictConfig(settings.LOGGING)
logger = logging.getLogger(basename(sys.argv[0]))



class MythTVMaintenanceException(Exception):
    pass


class MythTVChannelMaintenance(object):
    
    def __init__(self, args):
        self.args = args
        self._xmltv_data = None
        self._callsign_map = None
        self._backend = MythTVBackend.default(hostname=self.args.hostname,
                                              port=self.args.port)
        self._channels = None
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

    @property
    def channels(self):
        if self._channels is not None:
            return self._channels
        try:
            self._channels = MythTVQuerySet('ChannelInfo').all()
        except (ConnectionRefusedError, URLError) as e:
            if self._backend.hostname == "localhost":
                logger.info("hostname=='localhost' - has it been set in mythtv_cli_settings?")
            msg = ("Unable to get backend service.  Please check "
                   "hostname={host}, port={port} is correct and the backend "
                   "is up").format(
                        host=self._backend.hostname, port=self._backend.port)
            logger.fatal(msg)
            logger.fatal("Error: {0}".format(e))
            exit(1)
        return self._channels

    def require_xmltv(self):
        "Check that the XMLTV file name exists"
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

    def list(self, params):
        "List the XMLTV or MythTV channel data"
        if len(params) != 1:
            logger.fatal("Expecting only 1 parameter, got: {0}".format(params))
            exit(1)
        param = params[0]
        if param == "xmltv":
            self.list_xmltv()
        elif param == "channels":
            self.list_channels()
        else:
            logger.fatal("Unknown list parameter: {0}".format(param))
            exit(1)
        return

    def list_channels(self):
        "List the MythTV Channels"
        fmt_string = "{id:<5} {vs:<3} {callsign:<20} {channum:<7} {name:<20} {visible:<7} {xmltvid:<20} {icon:<20}"
        #import pdb; pdb.set_trace()
        print(fmt_string.format(
                id="Id",
                vs="Src",
                callsign="CallSign",
                channum="ChanNum",
                name="Name",
                visible="Visible",
                xmltvid="XMLTVID",
                icon="Icon URL"))
        print('-'*100)
        for channel in self.channels:
            print(fmt_string.format(
                id=channel.ChanId,
                vs=channel.SourceId,
                callsign=channel.CallSign,
                channum=channel.ChanNum,
                name=channel.ChannelName,
                visible=channel.Visible,
                xmltvid=channel.XMLTVID or "",
                icon=channel.IconURL or ""))
        print("")
        return

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
        if len(settings.XMLTV_CALLSIGNS) == 0:
            logger.warn("CallSign mapping is empty."
                "  This normally should be configured in mythtv_cli_settings.py")
        self._callsign_map = {}
        # Ensure that the callsigns in the XMLTV file map to themselves
        for callsign, xmltvid in self.xmltv_data.items():
            self._callsign_map[callsign] = xmltvid
            alternates = settings.XMLTV_CALLSIGNS.get(callsign)
            if alternates is not None:
                for alternate in alternates:
                    self._callsign_map[alternate] = xmltvid
        return self._callsign_map

    def update(self, params):
        "Parse and execute the supplied icons command"
        if len(params) != 1:
            msg = "Expected single parameter, got: {0}".format(params)
            logger.fatal(msg)
            exit(1)
        if params[0] == "xmltvids":
            self.update_xmltvids()
        else:
            msg = "Unknown update parameters: {0}".format(params)
            logger.fatal(msg)
            exit(1)
        return

    def update_xmltvids(self):
        """Update the Channel database from the supplied XMLTV file."""
        csmap = self.callsign_map
        proposed_changes = []
        # proposed_changes is a list of tuples:
        #    (ChanID, CallSign, New XMLTVID)
        for channel in self.channels:
            new_xmltvid = csmap.get(channel.CallSign)
            if new_xmltvid is None:
                continue
            if new_xmltvid != channel.XMLTVID:
                proposed_changes.append((channel, new_xmltvid))
        if len(proposed_changes) == 0:
            logger.info("update xmltvids: no updates required")
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
                    id=proposed[0].ChanId,
                    callsign=proposed[0].CallSign,
                    xmltvid=proposed[1]))
            answer = input("Proceed [y/N]? ")
            proceed = answer.lower() in ["y", "yes"]
        if proceed:
            for proposed in proposed_changes:
                channel = proposed[0]
                old_xmltvid = channel.XMLTVID
                channel.XMLTVID = proposed[1]
                channel.save()
                logger.info("ChanID: {callsign} ({cid}): XMLTVID '{old}' -> '{new}'".format(
                        callsign=channel.CallSign,
                        cid=channel.ChanId,
                        old=old_xmltvid,
                        new=channel.XMLTVID))
            logger.info("Updated {0} record(s)".format(len(proposed_changes)))
        return
 
    def icons(self, params):
        "Parse and execute the supplied icons command"
        if len(params) != 2:
            msg = "Expected parameter and file name, got: {0}".format(params)
            logger.fatal(msg)
            exit(1)
        if params[0] == "save":
            self.icons_save(params[1])
        elif params[0] == "load":
            self.icons_load(params[1])
        else:
            msg = "Unknown icons parameters: {0}".format(params)
            logger.fatal(msg)
            exit(1)
        return

    def icons_save(self, file_name):
        "Save the backend's icons to file_name"
        # Build a dictionary of CallSign to Icon URL.
        # We won't over-write an existing config file
        if exists(file_name):
            msg = ("{0} already exists: "
                   "please rename or delete prior to saving").format(file_name)
            logger.fatal(msg)
            exit(1)
        # There may be multiple entries with the same values, but no conflicts
        icon_map = {}
        for channel in self.channels:
            call_sign = channel.CallSign
            current_icon = icon_map.get(call_sign) 
            if current_icon is not None:
                if current_icon != channel.IconURL:
                    msg = "{0} has conflicting icons: '{1}' & '{2}'".format(
                        call_sign, current_icon, channel.IconURL)
                    logger.fatal(msg)
                    exit(1)
                # else:
                #    Icons match, no action required
            else:
                if channel.IconURL is not None:
                    icon_map[call_sign] = channel.IconURL
        # Write the dictionary to the specified file
        with open(file_name, "w") as fp:
            fp.write("""#
# mythtv_cli_extensions icon map
#
# icon_map is a dictionary of:
#
#    Call Sign ==> Icon URL
#
icon_map = {
""")
            for k, v in icon_map.items():
                fp.write("    '{0}' : '{1}',\n".format(k, v))
            fp.write("}\n")
        return

    def icons_load(self, file_name):
        "Load the backend's icons from file_name"
        if not exists(file_name):
            msg = ("{0} doesn't exist: "
                   "please check the file name and location prior to loading").format(file_name)
            logger.fatal(msg)
            exit(1)
        # Load the icon map
        with open(file_name) as fp:
            fcontents = fp.read()
        file_globals = {}
        file_locals = {}
        exec(fcontents, file_globals, file_locals)
        if 'icon_map' not in file_locals:
            msg = ("The Icon Map file doesn't contain the expected "
                   "dictionary: icon_map.  Please check the specified "
                   "file is a valid icon map")
            logger.fatal(msg)
            exit(1)
        icon_map = file_locals['icon_map']
        # Iterate over the channels and produce proposed changes
        proposed_changes = []
        for channel in self.channels:
            new_icon = icon_map.get(channel.CallSign)
            if new_icon is None:
                # No icon specified, move on
                continue
            if new_icon == channel.IconURL:
                # No change, move on
                continue
            # Save the old Icon for user confirmation
            channel._Old_IconURL = channel.IconURL
            channel.IconURL = new_icon
            proposed_changes.append(channel)
        if len(proposed_changes) == 0:
            logger.info("No Icon URLs to change")
            exit(0)
        proceed = self.args.yes
        if not proceed:
            # Ask the user for confirmation
            fmt_string = "{id:<6} {callsign:<20} {old_icon:<50} {new_icon:<50}"
            print(fmt_string.format(
                    id="Id",
                    callsign="CallSign",
                    old_icon="Old Icon URL",
                    new_icon="New Icon URL"))
            print("-"*132)
            for channel in proposed_changes:
                print(fmt_string.format(
                    id=channel.ChanId,
                    callsign=channel.CallSign,
                    old_icon=channel._Old_IconURL,
                    new_icon=channel.IconURL))
            answer = input("Proceed [y/N]? ")
            proceed = answer.lower() in ["y", "yes"]
        if proceed:
            for channel in proposed_changes:
                channel.save()
                logger.info("Channel: {callsign} ({cid}): IconURL '{old}' -> '{new}'".format(
                        callsign=channel.CallSign,
                        cid=channel.ChanId,
                        old=channel._Old_IconURL,
                        new=channel.IconURL))
            logger.info("Updated {0} record(s)".format(len(proposed_changes)))
        return



def main():
    logger.debug("Starting")
    epilog = """
{prog} has 4 basic use cases:

    {prog} list xmltv --xmltv file.name
        List the channel and XMLTVID data contained in the xmltv file
    {prog} list channels
        List the channel data contained in the MythTV backend
    {prog} update xmltvids --xmltv file.name [-y]
        Update Channel XMLTVIDs, see below
    {prog} icons save/load file.name
        Save or load the icon URLs to/from the specified file
 

Updating Channel XMLTVIDs
-------------------------

This option can be used to re-populate and correct XMLTVIDs in the Backend
database.

It reads the XMLTVIDs from the supplied file (--xmltv file.name), creates a
mapping from all CallSign variations as defined in the users settings file
(mythtv_chanmaint_settings.py) and reads and checks each channel in the 
backend.  If -y is not supplied the proposed updates are listed and the user
is asked for confirmation prior to updating the backend.



Typical XMLTVID Workflow
------------------------

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

""".format(prog=basename(sys.argv[0]))
    parser = argparse.ArgumentParser(description="MythTV Channel Maintenance",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=epilog)
    parser.add_argument('--xmltv',
                        default='tv_grab.xml',
                        help='XMLTV data file (default=tvgrab.xml)')
    parser.add_argument('--hostname',
                        default=None,
                        help='MythTV Backend hostname (localhost)')
    parser.add_argument('--server-port', dest='port',
                        default=None,
                        help="MythTV Backend services port (6544)")
#     parser.add_argument('--frontend-port',
#                         default=None,
#                         help="MythTV Frontend services port (1234)")
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
                        choices=['list', 'update', 'icons'],
                        help="Maintenance command, see below")
    parser.add_argument('params',
                        nargs='+',
                        help="Command parameter")
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s version '+ __VERSION__)
    args = parser.parse_args()

    maint = MythTVChannelMaintenance(args)
    maint.execute()
    logger.debug("Done")

    return


if __name__ == "__main__":
    main()
