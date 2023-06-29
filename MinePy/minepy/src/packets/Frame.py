from minepy.src.packets.Buffer import Buffer
from minepy.src.packets.ReliabilityTool import ReliabilityTool


class Frame(Buffer):
    body = b''
    fragmented = False
    reliable_frame_index = None
    reliability = None
    sequenced_frame_index = None
    ordered_frame_index = None
    order_channel = None
    compound_size = None
    index = None
    compound_id = None

    def decode(self) -> None:
        flags = self.readUnsignedbyte()
        self.reliability = (flags & 0xf4) >> 5
        self.fragmented = (flags & 0x10) > 0
        body_length = self.readUnsignedShort() >> 3
        if ReliabilityTool.reliable(self.reliability):
            self.reliable_frame_index = self.readUnsignedTriad_le()
        if ReliabilityTool.sequenced(self.reliability):
            self.sequenced_frame_index = self.readUnsignedTriad_le()
        if ReliabilityTool.ordered(self.reliability):
            self.ordered_frame_index: int = self.readUnsignedTriad_le()
            self.order_channel = self.readUnsignedbyte()
        if self.fragmented:
            self.compound_size = self.readUnsignedInt()
            self.compound_id = self.readUnsignedShort()
            self.index = self.readUnsignedInt()
        self.body = self.get(body_length)

    def encode(self) -> None:
        self.putUnsignedByte(self.reliability | 0x10 if self.fragmented else self.reliability)
        self.putUnsignedShort(len(self.body) << 3)
        if ReliabilityTool.reliable(self.reliability):
            self.putUnsignedTriad_le(self.reliable_frame_index)
        if ReliabilityTool.sequenced(self.reliability):
            self.putUnsignedTriad_le(self.sequenced_frame_index)
        if ReliabilityTool.ordered(self.reliability):
            self.putUnsignedTriad_le(self.ordered_frame_index)
            self.putUnsignedByte(self.order_channel)
        if self.fragmented:
            self.putUnsignedInt(self.compound_size)
            self.putUnsignedShort(self.compound_id)
            self.putUnsignedInt(self.index)
        self.add(self.body)

    def get_size(self):
        length = 3
        if ReliabilityTool.reliable(self.reliability):
            length += 3
        if ReliabilityTool.sequenced(self.reliability):
            length += 3
        if ReliabilityTool.ordered(self.reliability):
            length += 4
        if self.fragmented:
            length += 10
        length += len(self.body)
        return length
