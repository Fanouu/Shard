from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class packet(Packet):
    packet_id = BedrockType.SERVER_HANDSHAKE
