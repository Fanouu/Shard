from colorama import Style, Fore


class Logger:
    prefix = []

    def __init__(self, prefix=None):
        if prefix is None:
            prefix = ["Server Thread"]
        self.prefix = prefix

    def getPrefix(self):
        prefix = ""
        for p in self.prefix:
            prefix = prefix + f"[{p}]"

        return prefix

    def send(self, COLOR, level, text):
        print(COLOR + self.getPrefix() + level + ":" + Style.RESET_ALL, self.valueIsString(text))
    def warning(self, text):
        self.send(Fore.RED, "[WARNING]", text)

    def notice(self, text):
        self.send(Fore.BLUE, "[NOTICE]", text)

    def valueIsString(self, value):
        if type(value) != str:
            raise TypeError(f"\"{value}\" is not a string")

        return value