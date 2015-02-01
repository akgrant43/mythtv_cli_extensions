#
# mythtv_chanmaint default settings.
#
# This file should not be modified by users.
#
# Custom configuration should be placed in mythtv_chanmaint_settings.py
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
        'level' : 'INFO',
    }
}

XMLTV_CALLSIGNS = {}