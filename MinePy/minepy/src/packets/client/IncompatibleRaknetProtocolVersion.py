from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class IncompatibleRaknetProtocolVersion(Packet):
    packet_id = BedrockType.INCOMPATIBLE_RANKETPROTOCOL_VERSION

    magic = None
    raknet_protocol_version = None
    server_uid: int = None

    def encodePayload(self):
        self.putByte(self.raknet_protocol_version)
        self.putMagic(self.magic)
        self.putLong(self.server_uid)
