#
# mythtv_chainmaint_example.py
#
# Sample mythtv_chanmaint configuration, e.g.:
#
# * Logging details
# * XMLTV callsign mapping
#

from mythtv_chanmaint_default import *

#
# XMLTV CallSign Mapping
#
# This table maps the CallSigns as provided in the XMLTV file to
# one or more CallSigns as provided in the MythTV backend.
#
# Note:
# * It isn't necessary to specify channels where the callsigns match.
# * This is from the free-to-air channels in the Czech Republic, however
#   it isn't intended to be complete or accurate data.
#

XMLTV_CALLSIGNS = {
#   XMLTV callsign         : MythTV CallSign(s)
    "ČT1"                  : ["CT 1"],
    "ČT2"                  : ["CT 2"],
    # In this example I'm assuming that the SD and HD channels are the same
    "ČT sport"             : ["CT sport", "CT sport HD"],
    "ČT24"                 : ["CT 24"],
    "ČT :D"                : ["CT :D / CT art"],
    "Nova Cinema"          : ["NOVA CINEMA"],
    "TV Barrandov"         : ["BARRANDOV TV"],
    "Fanda"                : ["FANDA"],
    "Óčko"                 : ["Ocko"]
    }
