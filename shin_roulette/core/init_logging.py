import os
import logging
from logging.config import dictConfig


class CustomRotatingFileHandler(logging.handlers.RotatingFileHandler):
    """Rollover when logging gets configured."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.doRollover()


LOG_PATH = 'logs/bot.log'

LOGGING_CONFIG = {
    'version': 1,
    'disabled_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            '%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s'
        },
        'standard': {
            'format': '%(levelname)-10s - %(name)-15s : %(message)s'
        },
    },
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'console_info': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'console_warning': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'DEBUG',
            '()': CustomRotatingFileHandler,
            'filename': LOG_PATH,
            'mode': 'a',
            'formatter': 'verbose',
            'backupCount': 10
        },
    },
    'loggers': {
        '': {   # root logger
            'handlers': ['console_debug', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'discord': {
            # have discord.py setup its own console logger
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'cogwatch': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False
        }
    },
}


def init_logging():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    dictConfig(LOGGING_CONFIG)
