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
                "server-name": "Test",
                "server-ip": '127.0.0.1',
                "server-port": 19132,
                "server-motd": 'MinePy: Bedrock Server',
                "max-players": 10,
                "default-gamemode": 0
            })
            config.save()
        self.config = config

        print(self.getMotd())

    def getMotd(self):
        return self.getConfig().get("server-motd")

    def getServerIp(self):
        return self.getConfig().get("server-ip")

    def getServerPort(self) -> str:
        return self.getConfig().get("server-port")

    def getServerName(self):
        return self.getConfig().get("server-name")

    def getMaxPlayers(self):
        return self.getConfig().get("max-players")

    def getDefaultGameMode(self):
        return self.getConfig().get("default-gamemode")
