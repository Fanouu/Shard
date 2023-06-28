from minepy.src.packets.Packet import Packet


class ClientTestConnection1Reply(Packet):
    packet_id = 0x06

    magic = None
    server_uid = None
    raknet_null_padding = None

    def encodePayload(self):
        if not isinstance(self.magic, bytes):
            self.magic = self.magic.encode('utf-8')
        self.putMagic(self.magic)
        self.putLong(self.server_uid)
        self.putBool(False)
        self.putShort(self.raknet_null_padding)
