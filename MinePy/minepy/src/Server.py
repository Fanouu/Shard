import socketserver
import Logger

class server:
    logger = None
    server_datapath = None

    def getServerDataPath(self):
        return self.server_datapath

    def getServerLogger(self):
        return self.logger

    def __init__(self):
        self.logger = Logger.Logger(["Server"])


server = server()
