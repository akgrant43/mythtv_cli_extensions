#
# mythtv_chainmaint_settings.py
#
# mythtv_chanmaint configuration, i.e.:
#
# * Logging details
# * XMLTV callsign mapping
#

from mythtv_cli_default import *

#
# XMLTV CallSign Mapping
#
# This table maps the CallSigns as provided in the XMLTV file to
# one or more CallSigns as provided in the MythTV backend.
#
# Note:
# * It isn't necessary to specify channels where the callsigns match.
# * See mythtv_chanmaint_example.py for additional comments and an example.
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
HOSTNAME="myth-usb.local"