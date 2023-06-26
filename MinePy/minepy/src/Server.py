import Logger

class server:
    logger = None

    def getServerLogger(self):
        return self.logger

    def __init__(self):
        self.logger = Logger.Logger(["Server"])


server = server()
