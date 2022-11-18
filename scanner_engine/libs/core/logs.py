import logging
import sys
import traceback


FORMATTER = logging.Formatter(fmt="[%(asctime)s] - [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

LOGGER = logging.getLogger("SCANNER")

FILE_HANDLER = logging.FileHandler("")

FILE_HANDLER.setFormatter(FORMATTER)

STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
STDOUT_HANDLER.setFormatter(FORMATTER)

LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(STDOUT_HANDLER)
LOGGER.setLevel(logging.DEBUG)


def _error(msg: str):
    if any(sys.exc_info()):
        LOGGER.error("\n".join((msg, traceback.format_exc())))
    else:
        LOGGER.error(msg)


ERROR = _error
DEBUG = LOGGER.debug
INFO = LOGGER.info
WARN = LOGGER.warn

