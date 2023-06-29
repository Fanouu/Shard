from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class ClientIncomingConnection(Packet):
    packet_id = BedrockType.NEW_INCOMING_CONNECTION

    server_address = None
    system_addresses = None
    accepted_timestamp = None
    request_timestamp = None

    def decodePayload(self) -> None:
        self.server_address = self.read_address()
        self.system_addresses = []
        for i in range(0, 20):
            self.system_addresses.append(self.read_address())
        self.request_timestamp = self.readUnsignedlong()
        self.accepted_timestamp = self.readUnsignedlong()

    def encodePayload(self) -> None:
        self.putAddress(self.server_address[0], self.server_address[1])
        for address in self.system_addresses:
            self.putAddress(address[0], address[1])
        self.putUnsignedlong(self.request_timestamp)
        self.putUnsignedlong(self.accepted_timestamp)
