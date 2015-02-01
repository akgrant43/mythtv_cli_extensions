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


