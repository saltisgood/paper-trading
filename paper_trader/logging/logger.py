import logging
import sys

from .formatter import ColourFormatter


def init_logger(name: str):
    logger = logging.getLogger(name)
    if logger.handlers:
        return

    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    sh.setLevel(logging.DEBUG if verbose else logging.INFO)
    sh.setFormatter(ColourFormatter())

    logger.addHandler(sh)
