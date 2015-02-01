# mythtv_cli_extensions
MythTV python CLI utilities and classes

First: Many thanks to the developers of the MythTV project for making such a great piece of software available.  The mythtv_cli_extensions are my personal work and any shortcomings, bugs, problems, etc. are mine and no reflection on the MythTV developers.

mythtv_cli_extensions provides two utilities and a couple of python libraries for use with the MythTV DVR software.  To find out more about MythTV please see http://mythtv.org.

## Utilities

<dl>
    <dt>mythtv_cli.py</dt>
    <dd>Provides a command line utility for calling the MythTV web services and exploring the database a bit.</dd>

    <dt>mythtv_chanmaint.py</dt>
    <dd>Provides a utility for maintaining XMLTVIDs and (eventually) channel icons in MythTV.</dd>
</dl>

The help text for each is included below.

## Python Libraries

<dl>
    <dt>MythTVService</dt>
    <dd>Provides low level access to the MythTV web services using the suds-jurko module.<br/>
        See https://bitbucket.org/jurko/suds for information about suds-jurko.</dd>
    <dt>MythTVObject</dl>
    <dd>Provides an easy way to write entries back to the MythTV backend, taking care of naming inconsistencies, etc.  Currently on Channel is supported.</dd>
</dl>

## Dependencies

mythtv_cli_extensions depend on the suds-jurko module (https://bitbucket.org/jurko/suds).  The simplest way to install suds-jurko is:

    [sudo] pip install suds-jurko


# mythtv_cli.py help

usage: mythtv_cli.py [-h] [--post] service operation [operation ...]

MythTV Web Services CLI

positional arguments:
  service     MythTV Service Name
  operation   MythTV Service Operation and parameters

optional arguments:
  -h, --help  show this help message and exit
  --post      Show POST operations with operation help

Valid Services: Capture, Channel, Content, DVR, Frontend, Guide, Myth, Video
    
Additional Help:

   mythtv_cli.py <service> help # for help on individual services.
   mythtv_cli.py <service> <operation> help # for detailed parameter information
    
Documentation: https://www.mythtv.org/wiki/Services_API

# mythtv_chanmaint.py help

usage: mythtv_chanmaint.py [-h] [--xmltv XMLTV] [--hostname HOSTNAME]
                           [--server-port PORT]
                           [--frontend-port FRONTEND_PORT] [--config CONFIG]
                           [--create-config] [-y]
                           {list,update_xmltvids} [params]

MythTV Channel Maintenance

positional arguments:
  {list,update_xmltvids}
                        Maintenance command, see below
  params                Command parameter

optional arguments:
  -h, --help            show this help message and exit
  --xmltv XMLTV         XMLTV data file
  --hostname HOSTNAME   MythTV Backend hostname (localhost)
  --server-port PORT    MythTV Backend services port (6544)
  --frontend-port FRONTEND_PORT
                        MythTV Frontend services port (1234)
  --config CONFIG       Configuration data
  --create-config       Create a new configuration data file
  -y                    Execute updates without user confirmation

mythtv_chanmaint.py has 3 basic use cases:

    mythtv_chanmaint.py list xmltv --xmltv file.name
        List the channel and XMLTVID data contained in the xmltv file
    mythtv_chanmaint.py list channels
        List the channel data contained in the MythTV backend
    mythtv_chanmaint.py update_xmltvids --xmltv file.name [-y] [--replace]
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

