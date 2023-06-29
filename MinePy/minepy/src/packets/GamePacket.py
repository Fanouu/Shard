from minepy.src.packets.Buffer import Buffer
from minepy.src.packets.Packet import Packet
import zlib

class GamePacket(Packet):
    packet_id = 0xfe

    def decode_payload(self):
        self.body: bytes = zlib.decompress(self.getRemaining(), -zlib.MAX_WBITS, 1024 * 1024 * 8)

    def encodePayload(self):
        compress = zlib.compressobj(1, zlib.DEFLATED, -zlib.MAX_WBITS)
        compressed_data = compress.compress(self.body)
        compressed_data += compress.flush()
        self.add(compressed_data)

    def write_packet_data(self, data):
        buffer = Buffer()
        buffer.putVarInt(len(data))
        buffer.add(data)
        if hasattr(self, "body"):
            self.body += buffer.data
        else:
            self.body = buffer.data

    def read_packets_data(self):
        buffer = Buffer(self.body)
        packets_data = []
        while not buffer.feos():
            packets_data.append(buffer.get(buffer.readVarInt()))
        return packets_data
