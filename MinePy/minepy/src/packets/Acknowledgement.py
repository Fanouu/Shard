from minepy.src.packets.Buffer import Buffer
from minepy.src.packets.Packet import Packet


class Acknowledgement(Packet):
    def decodePayload(self) -> None:
        self.sequence_numbers: list = []
        count: int = self.readUnsignedShort()
        for i in range(0, count):
            single: bool = self.readBool()
            if not single:
                index: int = self.readUnsignedTriad_le()
                end_index: int = self.readUnsignedTriad_le()
                while index <= end_index:
                    self.sequence_numbers.append(index)
                    index += 1
            else:
                self.sequence_numbers.append(self.readUnsignedTriad_le())

    def encodePayload(self) -> None:
        self.sequence_numbers.sort()
        temp_buffer: Buffer = Buffer()
        count: int = 0
        if len(self.sequence_numbers) > 0:
            start_index: int = self.sequence_numbers[0]
            end_index: int = self.sequence_numbers[0]
            for pointer in range(1, len(self.sequence_numbers)):
                current_index: int = self.sequence_numbers[pointer]
                diff: int = current_index - end_index
                if diff == 1:
                    end_index: int = current_index
                elif diff > 1:
                    if start_index == end_index:
                        temp_buffer.putBool(True)
                        temp_buffer.putUnsignedTriad_le(start_index)
                        start_index = end_index = current_index
                    else:
                        temp_buffer.putBool(False)
                        temp_buffer.putUnsignedTriad_le(start_index)
                        temp_buffer.putUnsignedTriad_le(end_index)
                        start_index = end_index = current_index
                    count += 1
            if start_index == end_index:
                temp_buffer.putBool(True)
                temp_buffer.putUnsignedTriad_le(start_index)
            else:
                temp_buffer.putBool(False)
                temp_buffer.putUnsignedTriad_le(start_index)
                temp_buffer.putUnsignedTriad_le(end_index)
            count += 1
            self.putUnsignedShort(count)
            self.add(temp_buffer.data)