GREY = "\x1b[38;20m"
YELLOW = "\x1b[33;20m"
BLUE = "\x1b[1;34m"
RED = "\x1b[31;20m"
BOLD_RED = "\x1b[31;1m"
RESET = "\x1b[0m"

def format_colour(s: str, colour: str):
    return colour + s + RESET