# mythtv_cli_extensions
MythTV python CLI utilities and classes

First: Many thanks to the developers of the MythTV project for making such a great piece of software available.  The mythtv_cli_extensions are my personal work and any shortcomings, bugs, problems, etc. are mine and no reflection on the MythTV developers.

mythtv_cli_extensions provides two utilities and a couple of python libraries for use with the MythTV DVR software.  To find out more about MythTV please see http://mythtv.org.

WARNING: This software is still in the early development stage, there's no guarantee of backward compatibility until it reaches V1.0.

## Utilities

<dl>
    <dt>mythtv_cli.py</dt>
    <dd>Provides a command line utility for:
    <ul>
        <li>calling the MythTV web services and exploring the database a bit.</li>
        <li>updating the database.  Only fields that are considered user maintainable can be modifed.  Currently only the Channel class can be updated.
    </dd>

    <dt>mythtv_chanmaint.py</dt>
    <dd><p>Provides a utility for maintaining XMLTVIDs and (eventually) channel icons in MythTV.</p>
        <p>This is typically used to restore XMLTVIDs after a channel re-scan has been performed.</p>
    </dd>
</dl>

The current functionality is enough to allow a simple shell script to be written that will allow the channels to be put back to their correct state after a re-scan.

The help text for each is included below.

## Python3 Libraries

<dl>
    <dt>MythTVServiceAPI</dt>
    <dd>Provides low level access to the MythTV web services using the suds-jurko module.<br/>
        See https://bitbucket.org/jurko/suds for information about suds-jurko.</dd>
    <dt>MythTVQuerySet</dt>
    <dd>Provides a django like interface to query the backend.</dd>
    <dt>MythTVClass</dt>
    <dd>Provides a python object representation of the back end web service objects, taking care of naming inconsistencies, etc.  Currently on Channel is supported.  Look at the version number if you're wondering.</dd>
</dl>

An example of retrieving all channels with call sign "ABC" and updating the first record:

```
from mythtvlib.object import MythTVQuerySet

# Get a QuerySet on the Channel class
query_set = MythTVQuerySet("MythTVChannel")
# Filter records with CallSign equal to "ABC"
query_set = query_set.filter(CallSign="^ABC$")  # This is a regular expression, and we don't want callsigns containing "ABC"
matching_records = query_set.all()
print(matching_records)
# Update the first record's name to be "DEF"
query_set[0].ChannelName = "DEF"
query_set[0].save()
```


## Dependencies

mythtv_cli_extensions depend on the suds-jurko module (https://bitbucket.org/jurko/suds).  The simplest way to install suds-jurko is:

    [sudo] pip install suds-jurko


## ToDo:

LOTS!

* Save and restore icon definitions
  * This can be done using mythtv_cli.py update, but must be manually maintained
* Extend the library to handle all the classes defined by the web services
* Extend filter() to do proper numeric comparisons


# mythtv_cli.py help

```
usage: mythtv_cli.py [-h] [--post] [--hostname HOSTNAME] [--server-port PORT]
                     [-y] [--version]
                     {dump,update} params [params ...]

MythTV Web Services CLI

positional arguments:
  {dump,update}        Maintenance command, see below
  params               Command parameter(s)

optional arguments:
  -h, --help           show this help message and exit
  --post               Show POST operations with operation help
  --hostname HOSTNAME  MythTV Backend hostname
  --server-port PORT   MythTV Backend services port
  -y                   Execute updates without user confirmation
  --version            show program's version number and exit

mythtv_cli.py has 2 basic use cases:

    mythtv_cli.py dump &lt;service&gt; &lt;operation&gt; &lt;key...&gt;
        Print the results of the requested service/operation
    mythtv_cli.py update &lt;class name&gt; &lt;filter field&gt; &lt;filter regex&gt; &lt;update field&gt; &lt;update value&gt;
        Update the records matching the supplied regular expression in the
        requested class.

Valid Services: Capture, Channel, Content, DVR, Frontend, Guide, Myth, Video

Valid Class Names: Channel

Additional Help:

   mythtv_cli.py dump &lt;service&gt; help # for help on individual services.
   mythtv_cli.py dump &lt;service&gt; &lt;operation&gt; help # for detailed parameter information

    
MythTV Web Services Documentation: https://www.mythtv.org/wiki/Services_API
```

# mythtv_chanmaint.py help

```
usage: mythtv_chanmaint.py [-h] [--xmltv XMLTV] [--hostname HOSTNAME]
                           [--server-port PORT] [--config CONFIG]
                           [--create-config] [-y] [--version]
                           {list,update_xmltvids} [params]

MythTV Channel Maintenance

positional arguments:
  {list,update_xmltvids}
                        Maintenance command, see below
  params                Command parameter

optional arguments:
  -h, --help            show this help message and exit
  --xmltv XMLTV         XMLTV data file (default=tvgrab.xml)
  --hostname HOSTNAME   MythTV Backend hostname (localhost)
  --server-port PORT    MythTV Backend services port (6544)
  --config CONFIG       Configuration data
  --create-config       Create a new configuration data file
  -y                    Execute updates without user confirmation
  --version             show program's version number and exit

mythtv_chanmaint.py has 3 basic use cases:

    mythtv_chanmaint.py list xmltv --xmltv file.name
        List the channel and XMLTVID data contained in the xmltv file
    mythtv_chanmaint.py list channels
        List the channel data contained in the MythTV backend
    mythtv_chanmaint.py update_xmltvids --xmltv file.name [-y]
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
```

