import logging
import logging.config
from logging.handlers import RotatingFileHandler
import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')

log_dir = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, 'app.log')

# Define the logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_file,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': LOG_LEVEL,
            'propagate': True
        },
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
