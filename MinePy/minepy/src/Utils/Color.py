from colorama import Fore, Style

class baseFormat:
    ESCAPE = "§"
    BLACK = ESCAPE + "0"
    DARK_BLUE = ESCAPE + "1"
    DARK_GREEN = ESCAPE + "2"
    DARK_AQUA = ESCAPE + "3"
    DARK_RED = ESCAPE + "4"
    DARK_PURPLE = ESCAPE + "5"
    GOLD = ESCAPE + "6"
    GRAY = ESCAPE + "8"
    BLUE = ESCAPE + "9"
    GREEN = ESCAPE + "a"
    AQUA = ESCAPE + "b"
    RED = ESCAPE + "c"
    LIGHT_PURPLE = ESCAPE + "d"
    YELLOW = ESCAPE + "e"
    WHITE = ESCAPE + "f"
    OBFUSC = ESCAPE + "k"
    BOLD = ESCAPE + "l"
    ITALIC = ESCAPE + "o"
    RESET = ESCAPE + "r"


Format = baseFormat


def colorLogger(text: str):
    text = text.replace(Format.BLACK, Fore.BLACK)
    text = text.replace(Format.DARK_BLUE, Fore.BLUE)
    text = text.replace(Format.DARK_GREEN, Fore.GREEN)
    text = text.replace(Format.DARK_AQUA, Fore.CYAN)
    text = text.replace(Format.DARK_RED, Fore.RED)
    text = text.replace(Format.DARK_PURPLE, Fore.MAGENTA)
    text = text.replace(Format.GOLD, Fore.YELLOW)
    text = text.replace(Format.GRAY, Fore.LIGHTBLACK_EX)
    text = text.replace(Format.BLUE, Fore.LIGHTBLUE_EX)
    text = text.replace(Format.GREEN, Fore.LIGHTGREEN_EX)
    text = text.replace(Format.AQUA, Fore.LIGHTCYAN_EX)
    text = text.replace(Format.RED, Fore.LIGHTRED_EX)
    text = text.replace(Format.LIGHT_PURPLE, Fore.LIGHTMAGENTA_EX)
    text = text.replace(Format.YELLOW, Fore.LIGHTYELLOW_EX)
    text = text.replace(Format.WHITE, Fore.LIGHTWHITE_EX)
    text = text.replace(Format.OBFUSC, "")
    text = text.replace(Format.BOLD, "")
    text = text.replace(Format.ITALIC, "")
    text = text.replace(Format.RESET, Style.RESET_ALL)
    return text + Style.RESET_ALL
