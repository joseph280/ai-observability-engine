import logging
import sys

from pythonjsonlogger import jsonlogger


def get_logger(name: str):
    logger = logging.getLogger(name)

    #Singleton-like check: If logger has handlers, don't add more (prevents duplicate logs)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)

        #We configure the JSON structure here
        formatter = jsonlogger.JsonFormatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        #Set to INFO to avoid debug noise
        logger.setLevel(logging.INFO)

    return logger