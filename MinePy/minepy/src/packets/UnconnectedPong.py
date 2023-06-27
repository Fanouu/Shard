from minepy.src.packets.BedrockProtocol import BedrockType
from minepy.src.packets.Packet import Packet


class UnconnectedPong(Packet):
    packet_id = BedrockType.UNCONNECTED_PONG

    client_timestamp: int = None
    magic: bytes = None
    serverGUID: int = None
    serverData: str = None

    def encodePayload(self):
        self.putLong(self.client_timestamp)
        self.putLong(self.serverGUID)
        if not isinstance(self.magic, bytes):
            self.magic = self.magic.encode('utf-8')
        self.putMagic(self.magic)
        self.putString(self.serverData)
