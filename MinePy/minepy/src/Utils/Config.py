import json
import os.path

CONFIG_YAML = 0
CONFIG_JSON = 1


class config:
    path = None
    config = {}
    type = None

    def __init__(self, path: str, type: int):
        self.type = type
        self.path = path
        if not os.path.exists(path):
            open(path, "w+")
            self.save()

        self.load()

    def load(self):
        if self.type == CONFIG_JSON:
            with open(self.path, "r") as file:
                self.config = json.load(file)

    def save(self):
        data = ""
        if self.type == CONFIG_JSON:
            data = json.dumps(self.config)

        with open(self.path, "w") as file:
            file.write(data)

    def set(self, target, value):
        self.config[target] = value

    def get(self, target, defaultValue=None):
        if not target in self.config:
            return defaultValue
        return self.config[target]

    def getNested(self, target, defaultValue=None):
        if target in self.config:
            return self.config[target]

        vars = target.split(".")
        base = self.config
        for value in vars:
            if value in base:
                base = base[value]
            else:
                return defaultValue
        return base

    def setNested(self, target, value):
        vars = target.split(".")
        base = self.config
        i = 0
        for name in vars:
            if i == len(vars) - 1:
                base[name] = value
                break
            if not name in base:
                base[name] = {}
            base = base[name]

            i = i + 1


config = config("test.json", CONFIG_JSON)
print(config.getNested("ola.tg"))
config.setNested("ola.tg", "salut")
print(config.getNested("ola.tg"))
config.save()
