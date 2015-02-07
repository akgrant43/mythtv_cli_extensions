# mythtv_cli_extensions

MythTV python CLI utilities and classes

First: Many thanks to the developers of the MythTV project for making such a great piece of software available.  The mythtv_cli_extensions are my personal work and any shortcomings, bugs, problems, etc. are mine and no reflection on the MythTV developers.

mythtv_cli_extensions provides two utilities and a couple of python libraries for use with the MythTV DVR software.  To find out more about MythTV please see http://mythtv.org.

WARNING: This software is still in the early development stage, there's no guarantee of backward compatibility until it reaches V1.0.

## Utilities

<dl>
    <dt>mythtv_cli</dt>
    <dd>Provides a command line utility for:
    <ul>
        <li>calling the MythTV web services and exploring the database a bit.</li>
        <li>updating the database.  Only fields that are considered user maintainable can be modifed.  Currently only the Channel class can be updated.
    </ul>
    </dd>

    <dt>mythtv_chanmaint</dt>
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


## Installation

mythtv_cli_extensions currently requires Python 3.4.0 or later.
It will probably work on 3.3, but as I haven't been able to test it
the check is for 3.4.0.  If a developer would like to confirm that it runs
under 3.3 I'll update the check.

mythtv_cli_extensions has the following dependencies:

* lxml
* setuptools
* suds-jurko
* fuzzywuzzy (automated tests only)
* python-Levenshtein (automated tests only, optional)

On Ubuntu only the first two need to be explicitly installed to use
mythtv_cli_extensions:

    sudo apt-get install python3-lxml
    sudo apt-get install python3-setuptools

To install the two automated test dependencies:

    [sudo] pip3 install fuzzywuzzy
    [sudo] pip3 install python-Levenshtein

mythtv_cli_extensions can be installed in the normal python fashion:

    [sudo] python3 setup.py install

The run-time dependency, suds-jurko, should be installed automatically.

The automated tests also use fuzzywuzzy, which has better performance with python-Levenshtein.

These are not installed automatically:


## ToDo:

LOTS!

* Save and restore icon definitions
  * This can be done using mythtv_cli.py update, but must be manually scripted
* Extend the library to handle all the classes defined by the web services
* Extend filter() to do proper numeric comparisons


