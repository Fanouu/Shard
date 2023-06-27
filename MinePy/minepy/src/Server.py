import socketserver
from minepy.src import Logger, ServerSocket
from minepy.src.Manager import ServerConfigManager

class server:
    logger = None
    server_datapath = None

    server_configManager = None

    def getServerConfigManager(self) -> ServerConfigManager.ServerConfigManager:
        return self.server_configManager

    def getServerDataPath(self):
        return self.server_datapath

    def getServerLogger(self):
        return self.logger

    def __init__(self, datapath):
        print("initing...")
        self.server_datapath = datapath
        self.logger = Logger.Logger(["Server"])
        self.server_configManager = ServerConfigManager.ServerConfigManager(self.server_datapath)

        ip = self.getServerConfigManager().getServerIp()
        print(ip)
        port = self.getServerConfigManager().getServerPort()
        print(port)
        server = ServerSocket.ServerSocket(ip, port)
        server.start()
