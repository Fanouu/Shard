import json
def getConfig(name):
    with open('config.json', 'r') as f:
        data = json.load(f)
        for value in data:
            if value == name:
                return data[value]

        vars = name.split(".")
        base = data
        for value in vars:
            if value in base:
                base = base[value]
            else:
                return None
        return base