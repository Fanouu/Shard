from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet


class ServerAcceptConnectionRequest(Packet):
    packet_id = BedrockType.CONNECTION_REQUEST_ACCEPTED

    client_address = None
    accepted_timestamp = None
    request_timestamp = None
    system_addresses = None
    system_index = None

    def decodePayload(self) -> None:
        self.client_address = self.read_address()
        self.system_index = self.readUnsignedShort()
        self.system_addresses = []
        for i in range(0, 10):
            print("Addresses: " + str(i))
            self.system_addresses.append(self.read_address())
        self.request_timestamp = self.readUnsignedlong()
        self.accepted_timestamp = self.readUnsignedlong()

    def encodePayload(self) -> None:
        self.putAddress(self.client_address[0], self.client_address[1])
        print(self.client_address)
        self.putUnsignedShort(self.system_index)
        for address in self.system_addresses:
            print(address)
            self.putAddress(address[0], address[1])
        self.putUnsignedlong(self.request_timestamp)
        self.putUnsignedlong(self.accepted_timestamp)
