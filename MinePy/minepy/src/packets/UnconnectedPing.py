from minepy.src.packets import BedrockProtocol
from minepy.src.packets.Packet import Packet


class UnconnectedPing(Packet):
    packet_id = BedrockProtocol.type.UNCONNECTED_PING

    client_timestamp: int = None
    magic: bytes = None
    ClientGUID: int = None

    def read_long(self):
        if len(self.data) < 8:
            raise ValueError("Insufficient data to read a long value")

        long_value = int.from_bytes(self.data[:8], byteorder='big', signed=False)
        self.data = self.data[8:]

        return long_value

    def decodePayload(self):
        self.client_timestamp = self.read_long()
        self.magic = self.read_magic()
        self.ClientGUID = self.read_long()

    def toDict(self) -> dict:
        dict = super().toDict()
        dict["magic"] = self.magic
        dict["clientGUID"] = self.ClientGUID
        dict["client_timestamp"] = self.client_timestamp

        return dict
