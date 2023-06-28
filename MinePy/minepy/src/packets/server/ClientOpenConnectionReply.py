from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class ClientOpenConnectionReply(Packet):
    packet_id = BedrockType.CLIENT_OPENCONNECTIONREPLY

    magic = None
    server_uid = None
    client_address = None
    mtu = None
    encryption = False

    def encodePayload(self):
        self.putMagic(self.magic)
        self.putLong(self.server_uid)
        self.write_address(self.client_address)
        self.putShort(self.mtu)
        self.putBool(self.encryption)
