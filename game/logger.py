""" Configure the logging module """
import logging
from .config import LOGGER_LEVEL

logging.basicConfig()
logger = logging.getLogger("")
logger.setLevel(LOGGER_LEVEL)
