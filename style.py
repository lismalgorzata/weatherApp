PADDING = 20
# center city and weather_description strings within a consistent length of characters :^{PADDING}

RED = "\033[1;31m"
YELLOW = "\033[33m"


REVERSE = "\033[;7m"
RESET = "\033[0m"


def change_color(color):
    print(color, end="")