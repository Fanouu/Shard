from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class OnlinePong(Packet):
    packet_id = BedrockType.ONLINE_PONG

    client_timestamp = None
    server_timestamp = None

    def decodePayload(self) -> None:
        self.client_timestamp: int = self.readUnsignedlong()
        self.server_timestamp: int = self.readUnsignedlong()

    def encodePayload(self) -> None:
        self.putUnsignedlong(self.client_timestamp)
        self.putUnsignedlong(self.server_timestamp)