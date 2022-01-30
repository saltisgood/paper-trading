import logging

from .colours import BLUE, BOLD_RED, GREY, RED, YELLOW, format_colour


class ColourFormatter(logging.Formatter):
    """
    Originally from https://stackoverflow.com/a/56944256/10611068
    """

    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: format_colour(format_str, GREY),
        logging.INFO: format_colour(format_str, BLUE),
        logging.WARNING: format_colour(format_str, YELLOW),
        logging.ERROR: format_colour(format_str, RED),
        logging.CRITICAL: format_colour(format_str, BOLD_RED),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
