from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class ServerAcceptConnectionRequest(Packet):
    packet_id = BedrockType.CONNECTION_REQUEST_ACCEPTED

    client_address = None
    pong = None
    ping = None
    system_addresses = None
    system_index = None

    def decodePayload(self) -> None:
        self.client_address = self.read_address()
        self.system_index = self.readUnsignedShort()
        self.system_addresses = []
        for i in range(0, 20):
            self.system_addresses.append(self.read_address())
        self.ping = self.readUnsignedlong()
        self.pong = self.readUnsignedlong()

    def encodePayload(self) -> None:
        self.putAddress(self.client_address[0], self.client_address[1])
        print(self.client_address)
        self.putShort(0)
        for address in self.system_addresses:
            self.putAddress(address[0], address[1])
        self.putLong(self.ping)
        self.putLong(self.pong)
