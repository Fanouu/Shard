from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class ClientOpenConnection(Packet):
    packet_id = BedrockType.CLIENT_OPENCONNECTION

    magic = None
    server_address = None
    mtu = None
    client_guid = None

    def decodePayload(self):
        self.magic = self.read_magic()
        self.server_address = self.read_address()
        self.mtu = self.readShort()
        self.client_guid = self.readLong()
