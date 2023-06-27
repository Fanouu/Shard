import json
import os.path

from jproperties import Properties
import yaml

CONFIG_YAML = 0
CONFIG_JSON = 1
CONFIG_PROPERTIES = 2


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
        if self.type == CONFIG_YAML:
            with open(self.path, "r") as file:
                load = yaml.full_load(file)
                if load is None:
                    load = {}
                self.config = load
        if self.type == CONFIG_PROPERTIES:
            with open(self.path, "r") as file:
                properties = Properties()
                properties.load(file)
                properties_dict = {}

                for item in properties.items():
                    properties_dict[item[0]] = item[1].data
                self.config = properties_dict

    def save(self):
        data = ""
        if self.type == CONFIG_JSON:
            data = json.dumps(self.config)
        if self.type == CONFIG_YAML:
            if len(self.config) > 0:
                data = yaml.dump(self.config)
        if self.type == CONFIG_PROPERTIES:
            properties = Properties()
            for index, value in self.config:
                properties[index] = value

            with open(self.path, "wb") as file:
                file.seek(0)
                file.truncate(0)
                properties.store(file, encoding="utf-8")
            return

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

    def setAll(self, value: dict):
        self.config = value

    def getAll(self):
        return self.config
