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
            'filename': 'mythtv_chanmaint.log',
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
        'pmlib': {
            'handlers' : ['rotate', 'console'],
            'propagate' : False,
            'level' : 'INFO',
        },
    },
    'root' : {
        'handlers' : ['rotate', 'console'],
        'level' : 'DEBUG',
    }
}

XMLTV_CALLSIGNS = {}
HOSTNAME='localhost'
PORT=6544