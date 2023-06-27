import random
import socketserver
import uuid

from minepy.src import Logger, ServerSocket
from minepy.src.Manager import ServerConfigManager

class server:
    logger = None
    server_datapath = None
    server_configManager = None

    BEDROCK_PROTOCOL_VERSION = 589
    VERSION = '1.20.0'
    SERVER_UUID = None

    ip = None
    port = None

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
        self.SERVER_UUID = random.randint(20, 40)

        self.ip = self.getServerConfigManager().getServerIp()
        self.port = self.getServerConfigManager().getServerPort()

        socketServer = ServerSocket.ServerSocket(self, self.ip, self.port)
        socketServer.start()

    def getServerDataForPonPacket(self):
        return ";".join([
            "MCPE",
            self.getServerConfigManager().getMotd(),
            str(self.BEDROCK_PROTOCOL_VERSION),
            self.VERSION,
            str(1),
            str(self.getServerConfigManager().getMaxPlayers()),
            str(self.SERVER_UUID),
            self.getServerConfigManager().getMotd(),
            str(0),
            str(0),
            str(self.port),
            str(19133)
        ])