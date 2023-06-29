from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class OnlinePing(Packet):
    packet_id = BedrockType.ONLINE_PING

    client_timestamp = None
    def decode_payload(self) -> None:
        self.client_timestamp: int = self.readUnsignedlong()

    def encode_payload(self) -> None:
        self.putUnsignedlong(self.client_timestamp)