import os.path

from minepy.src.Utils import Config


class ServerConfigManager:

    config = None

    def getConfig(self):
        return self.config
    def __init__(self, datapath):
        if not os.path.exists(datapath + "/server-settings.yml"):
            config = Config.config(datapath + "/server-settings.yml", Config.CONFIG_YAML)
            config.setAll({
                "server-ip": "127.0.0.1",
                "server-port": "19132",
                "server-motd": "MinePy: Bedrock Server"
            })
            config.save()

test = ServerConfigManager("")