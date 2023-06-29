from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Frame import Frame
from minepy.src.packets.Packet import Packet


class FrameSet(Packet):
    packet_id: int = BedrockType.frame_set_0
    frames: list = []

    def decodePayload(self) -> None:
        self.sequence_number: int = self.readUnsignedTriad_le()
        while not bool(len(self.data) <= self.offset):
            frame_packet: Frame = Frame(self.data[self.offset:])
            frame_packet.decode()
            self.frames.append(frame_packet)
            self.offset += frame_packet.get_size()

    def encodePayload(self) -> None:
        self.putUnsignedTriad_le(self.sequence_number)
        for frame_packet in self.frames:
            frame_packet.encode()
            self.add(frame_packet.data)

    def get_size(self) -> int:
        length: int = 4
        for frame_packet in self.frames:
            length += frame_packet.get_size()
        return length