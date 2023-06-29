from minepy.src.packets.Acknowledgement import Acknowledgement
from minepy.src.packets.BedrockProtocolInfo import BedrockType


class Ack(Acknowledgement):
    packet_id = BedrockType.ACK
