from minepy.src.player import Player


class PlayerManager:
    server = None

    players = []

    def __init__(self, Server: server):
        self.server = Server

    def getPlayers(self):
        return self.players

    def getPlayerById(self, id: int) -> Player:
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
