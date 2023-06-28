from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class ClientTestConnection1(Packet):
    packet_id = BedrockType.CLIENT_TESTCONNECTION1

    magic = None
    raknet_null_padding = None
    raknet_protocol_version = None

    def decodePayload(self):
        self.magic = self.read_magic()
        self.raknet_protocol_version = int(self.readByte())
        self.raknet_null_padding = self.getRemaining()
