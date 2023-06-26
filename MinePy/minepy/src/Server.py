import Logger

class server:
    logger = None

    def __init__(self):
        self.logger = Logger.Logger(["Server"])

    def getServerLogger(self):
        return self.logger


server = server()
