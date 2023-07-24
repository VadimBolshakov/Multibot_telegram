import logging.handlers
import logging.config
import create


EMAIL_SENDER = create.EMAIL_SENDER
EMAIL_PASSWORD = create.EMAIL_PASSWORD
EMAIL_RECIPIENT = create.EMAIL_RECIPIENT
LOG_FILE = create.LOG_FILE
TOKEN_BOT = create.TOKEN_BOT


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
        'telegram': {
            'class': 'logging.handlers.HTTPHandler',
            'host': 'localhost:8000',
            'url': 'https://api.telegram.org/bot{TOKEN_BOT}/sendMessage',
            'method': 'POST',
            'level': 'ERROR',
            'formatter': 'default_formatter',
        }
    },
    'loggers': {
        'my_logger': {
            # 'handlers': ['console', 'telegram'],
            'handlers': ['file', 'email'],
            'level': 'DEBUG',
            'propagate': True
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('my_logger')


if __name__ == '__main__':
    logger.debug('debug log it is logger')
    logger.info('logger info it is logger')
    logger.warning('warning it is logger')
    # logger.error('ZeroDivisionError it is logger', exc_info=True)
    logger.exception('exception it is logger', exc_info=True)
    # logger.critical('critical it is logger')

