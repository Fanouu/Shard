import socketserver
from minepy.src import Logger
from minepy.src.Manager import ServerConfigManager

class server:
    logger = None
    server_datapath = None

    server_configManager = None

    def getServerConfigManager(self):
        return self.server_configManager

    def getServerDataPath(self):
        return self.server_datapath

    def getServerLogger(self):
        return self.logger

    def __init__(self):
        self.logger = Logger.Logger(["Server"])
        self.server_configManager = ServerConfigManager.ServerConfigManager("")
