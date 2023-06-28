from minepy.src.client.Client import Client


class PlayerManager:
    server = None

    clients = []

    def __init__(self, Server: server):
        self.server = Server

    def getClients(self):
        return self.clients

    def getClient(self, address) -> Client:
        if id in self.players:
            return self.players[id]
        else:
            return None
