import logging
import logging.config
from logging.handlers import RotatingFileHandler
import os


LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
log_dir = os.path.join(os.getcwd(), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
fastapi_file = os.path.join(log_dir, 'FastAPI.log')
healthcheck_file = os.path.join(log_dir, 'HealthCheck.log')


# Define the logging configuration for FastAPI
FASTAPI_CONFIG = {
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
            'filename': fastapi_file,
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
        'fastapi_logger': {
            'handlers': ['file', 'console'],
            'level': LOG_LEVEL,
            'propagate': False
        },
    }
}


# Define the logging configuration for health checks
HEALTHCHECK_CONFIG = {
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
            'filename': healthcheck_file,
            'maxBytes': 10 * 1024 * 1024,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'health_check_logger': {
            'handlers': ['file'],
            'level': LOG_LEVEL,
            'propagate': False
        },
    }
}


def fastapi_logging():
    logging.config.dictConfig(FASTAPI_CONFIG)


def healthcheck_logging():
    logging.config.dictConfig(HEALTHCHECK_CONFIG)
