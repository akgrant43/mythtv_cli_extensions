#
# mythtv_cli default settings.
#
# DO NOT modify this file, it will be overwritten by software updates.
# You should create your own muthtv_cli_settings.py and place all custom
# configuration information there.
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'rotate': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'mythtv_cli.log',
            'maxBytes': 10000000,
            'backupCount': 5
            },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'mythtvlib': {
            'handlers' : ['rotate', 'console'],
            'propagate' : True,
            'level' : 'DEBUG',
        },
    },
    'root' : {
        'handlers' : ['rotate', 'console'],
        'level' : 'DEBUG',
    }
}

# See the mythtv_clie_settings_example for a description of XMLTV_CALLSIGNS
XMLTV_CALLSIGNS = {}

# Default hostname and port for the MythTV backend
HOSTNAME='localhost'
PORT=6544

# Default tmp directories
TMP_DIRS = ['/tmp/']
TMP_DIR_NAME = 'MythTV_CLI'