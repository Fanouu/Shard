import random
import socketserver
import sys
import uuid
from threading import Thread

from colorama import Style, Fore

from minepy.src import Logger, ServerSocket
from minepy.src.Utils import Color
from minepy.src.manager import ServerConfigManager
from minepy.src.manager.PlayerManager import PlayerManager


class server:
    logger = None
    server_datapath = None
    server_configManager = None
    playerManager = None

    BEDROCK_PROTOCOL_VERSION = 11
    VERSION = '1.20.0'
    SERVER_UUID = None

    ip = None
    port = None

    dev = False

    socketServer: ServerSocket = None

    def getPlayerManager(self) -> PlayerManager:
        return self.playerManager

    def getServerConfigManager(self) -> ServerConfigManager.ServerConfigManager:
        return self.server_configManager

    def getServerDataPath(self):
        return self.server_datapath

    def getServerLogger(self):
        return self.logger

    def getPort(self):
        return self.port

    def getIp(self):
        return self.ip

    def getPlayers(self):
        return self.getPlayerManager().getPlayers()

    def isDev(self) -> bool:
        return self.dev

    def __init__(self, datapath):
        self.server_datapath = datapath
        self.logger = Logger.Logger(["Server"])
        self.server_configManager = ServerConfigManager.ServerConfigManager(self.server_datapath)
        self.dev = self.getServerConfigManager().getDeveloppement()
        self.playerManager = PlayerManager(self)
        self.SERVER_UUID = random.randint(1, 99999999)

        self.ip = self.getServerConfigManager().getServerIp()
        self.port = self.getServerConfigManager().getServerPort()

        self.getServerLogger().notice("Creating Server Socket..")
        self.socketServer = ServerSocket.ServerSocket(self, self.ip, self.port)
        self.getServerLogger().notice("Connecting Server Socket...")
        self.socketServer.start()
        self.getServerLogger().info(f"Server Socket listening on: {Fore.RED}{self.ip}:{self.port} {Style.RESET_ALL}")

    def getServerDataForPonPacket(self):
        return ";".join([
            "MCPE",
            self.getServerConfigManager().getMotd(),
            str(self.BEDROCK_PROTOCOL_VERSION),
            self.VERSION,
            str(len(self.getPlayers())),
            str(self.getServerConfigManager().getMaxPlayers()),
            str(self.SERVER_UUID),
            self.getServerConfigManager().getMotd(),
            str('Survival'),
            str(1),
            str(self.port),
            str(self.getServerConfigManager().getServerPortV6())
        ])

    def stop(self):
        if self.socketServer.isAlive():
            self.socketServer.stop()
        sys.exit()
