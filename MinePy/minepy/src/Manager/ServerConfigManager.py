import os.path
from minepy.src.Utils import Config


class ServerConfigManager:
    config = None

    def getConfig(self) -> Config.config:
        return self.config

    def __init__(self, datapath):
        config = Config.config(datapath + "/server-settings.properties", Config.CONFIG_PROPERTIES)
        if not os.path.exists(datapath + "/server-settings.properties"):
            config.setAll({
                "server-ip": '127.0.0.1',
                "server-port": 19132,
                "server-motd": 'MinePy: Bedrock Server'
            })
            config.save()
        self.config = config

        print(self.getMotd())

    def getMotd(self):
        return self.getConfig().get("server-motd")
