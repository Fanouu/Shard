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

    def getPlayerByName(self, value: str) -> Player:
        for id in self.players:
            player = self.getPlayerById(id)
            if player is None:
                continue

            if player.getName() == value:
                return player
        return None
