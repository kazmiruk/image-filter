""" Settings for simple test server
"""
SERVER_ADDRESS = ''
SERVER_PORT = 3434

POLL_INTERVAL = 0.5
#End of server settings

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console': {
            'format': u'%(asctime)-15s: %(levelname)s: %(filename)s:%(lineno)d: %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': 'http://89bea7ad01544e6388b8bfba7f2d0021:56967d7d455b4909b9f9b3162ff5d292@sentry.dev.pearbox.net/7'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}

RESAMPLE = 'ANTIALIAS'

# http://redmine.pearbox.net/issues/2178
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
