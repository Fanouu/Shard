from minepy.src.packets.Acknowledgement import Acknowledgement
from minepy.src.packets.BedrockProtocolInfo import BedrockType


class Nack(Acknowledgement):
    packet_id = BedrockType.NACK