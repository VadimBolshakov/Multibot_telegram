"""Configuring logging for the project and add class TelegramHandler for sending messages to the telegram channel"""
import logging
import logging.config

import requests

import create

EMAIL_SENDER = create.EMAIL_SENDER
EMAIL_PASSWORD = create.EMAIL_PASSWORD
EMAIL_RECIPIENT = create.EMAIL_RECIPIENT
LOG_FILE = create.LOG_FILE
TOKEN_BOT = create.TOKEN_BOT
CHAT_ID = create.CHAT_ID


class TelegramHandler(logging.Handler):
    """Class for sending messages to the telegram channel"""
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={log_entry}')


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(asctime)s:%(levelname)s] %(message)s, func=%(funcName)s, file=%(filename)s'
        },
        'short_formatter': {
            'format': '[%(asctime)s:%(levelname)s] %(message)s '
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'short_formatter',
            'level': 'INFO',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default_formatter',
            'level': 'INFO',
            'filename': LOG_FILE,
            'maxBytes': 32768,
            'backupCount': 5
        },
        'email': {
            'class': 'logging.handlers.SMTPHandler',
            'mailhost': ('smtp.gmail.com', 587),
            'fromaddr': EMAIL_SENDER,
            'credentials': (EMAIL_SENDER, EMAIL_PASSWORD),
            'toaddrs': [EMAIL_RECIPIENT, ],
            'secure': (),
            'subject': 'Houston, we have a problem',
            'level': 'ERROR',
            'formatter': 'default_formatter',
        },
    },
    'loggers': {
        'my_logger': {
            # 'handlers': ['console'],
            'handlers': ['file', 'email'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)
telegram_handler = TelegramHandler(TOKEN_BOT, CHAT_ID)
telegram_handler.setLevel(logging.ERROR)
telegram_handler.setFormatter(logging.Formatter('[%(asctime)s:%(levelname)s] %(message)s'))
logger.addHandler(telegram_handler)

if __name__ == '__main__':
    logger.debug('debug log it is logger')
    logger.info('logger info it is logger')
    logger.warning('warning it is logger')
    logger.error('ZeroDivisionError it is logger', exc_info=True)
    logger.exception('exception it is logger', exc_info=True)
    logger.critical('critical it is logger')

