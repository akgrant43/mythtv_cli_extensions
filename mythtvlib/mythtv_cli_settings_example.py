#
# mythtv_chainmaint_settings_example.py
#
# mythtv_chanmaint configuration, i.e.:
#
# * Logging details
# * XMLTV callsign mapping
#
# Copy this file to mythtv_cli_settings.py and modify.
#
# DO NOT use mythtv_cli_settings_example.py directly, it will be overwritten
# by updates to the software
#

from mythtvlib.mythtv_cli_default import *

#
# XMLTV CallSign Mapping
#
# This table maps the CallSigns as provided in the XMLTV file to
# one or more CallSigns as provided in the MythTV backend.
#
# Note:
# * It isn't necessary to specify channels where the callsigns match.
# * See mythtv_cli_settings_example.py for additional comments and an example.
# * The example isn't meant to be complete, if you live in the Czech Republic,
#   you will still need to update this.
#
XMLTV_CALLSIGNS = {
#   XMLTV callsign         : MythTV CallSign(s)
    "ČT1"                  : ["CT 1"],
    "ČT2"                  : ["CT 2"],
    "ČT sport"             : ["CT sport", "CT sport HD"],
    "ČT24"                 : ["CT 24"],
    "ČT :D"                : ["CT :D / CT art"],
    "Nova Cinema"          : ["NOVA CINEMA"],
    "Nova TV"              : ["NOVA"],
    "TV Barrandov"         : ["BARRANDOV TV"],
    "Fanda"                : ["FANDA"],
    "Óčko"                 : ["Ocko"]
    }

# Backend hostname
HOSTNAME="localhost"