from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class ClientRequestConnection(Packet):
    client_guid = None
    ping = None

    packet_id = BedrockType.CONNECTION_REQUEST

    def decodePayload(self) -> None:
        self.client_guid = self.readUnsignedlong()
        self.ping = self.readUnsignedlong()

    def encodePayload(self) -> None:
        self.putUnsignedlong(self.client_guid)
        self.putUnsignedlong(self.ping)