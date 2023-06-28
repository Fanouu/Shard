from minepy.src.client.Client import Client


class PlayerManager:
    server = None

    clients = {}

    def __init__(self, Server: server):
        self.server = Server

    def getClients(self):
        return self.clients

    def getClient(self, address) -> Client | None:
        addressSTR = ":".join(address)
        if addressSTR in self.clients:
            return self.clients[addressSTR]
        else:
            return None
