import struct


class BinaryDataException(Exception):
    pass


class Buffer:
    data = b''
    offset = 0

    BYTE_SIZE = 1
    BOOL_SIZE = 1
    SHORT_SIZE = 2
    INT_SIZE = 4
    LONG_SIZE = 8
    FLOAT_SIZE = 4
    DOUBLE_SIZE = 8

    def __init__(self, data=b'', offset: int = 0):
        self.data = data
        self.offset = offset

    def get(self, pos):
        if not len(self.data) <= self.offset:
            self.offset += pos
            return self.data[self.offset - pos:self.offset]
        else:
            raise BinaryDataException(f"Not enough bytes left in buffer: need {pos}, have {len(self.data) - self.offset}")

    def getRemaining(self):
        return self.data[len(self.data) - self.offset]

    def add(self, text):
        self.data += text

    def readByte(self):
        return struct.unpack('b', self.get(self.BYTE_SIZE))[0]

    def putByte(self, value):
        if not isinstance(value, bytes):
            data = str(value).encode()
        self.add(struct.pack('b', int(value)))

    def readBool(self):
        return struct.unpack('?', self.get(self.BOOL_SIZE))[0]

    def putBool(self, value):
        return self.add(struct.pack('?', value))

    def readUnsignedbyte(self):
        return struct.unpack('B', self.get(1))[0]

    def putUnsignedByte(self, value):
        if not isinstance(value, bytes):
            data = value.encode('utf-8')
        self.add(struct.pack('B', value))

    def putShort(self, value):
        self.add(struct.pack('>h', value))

    def readShort(self):
        return struct.unpack('>h', self.get(self.SHORT_SIZE))[0]

    def putUnsignedShort(self, value):
        self.add(struct.pack('>H', value))

    def readUnsignedShort(self):
        return struct.unpack('>H', self.get(self.SHORT_SIZE))[0]

    def putInt(self, value):
        self.add(struct.pack('>i', value))

    def readInt(self):
        return struct.unpack('>i', self.get(self.INT_SIZE))[0]

    def putUnsignedInt(self, value):
        self.add(struct.pack('>I', value))

    def readUnsignedInt(self):
        return struct.unpack('>I', self.get(self.INT_SIZE))[0]

    def readString(self):
        length = self.readShort()
        return self.get(length).decode('utf-8')

    def putString(self, value):
        self.putShort(len(value))
        if not isinstance(value, bytes):
            data = value.encode('utf-8')
        self.add(value)

    def read_magic(self):
        if len(self.data) - self.offset < 16:
            raise BinaryDataException('End of buffer')
        return self.get(16)

    def putMagic(self, value=b'00ffff00fefefefefdfdfdfd12345678'):
        if not isinstance(value, bytes):
            value = value.encode('utf-8')
        self.add(value)

    def readUnsignedInt24le(self):
        return struct.unpack("<I", self.get(3) + b'\x00')[0]

    def putUnsignedInt24le(self, data):
        self.add(struct.pack("<I", data)[:3])

    def read_address(self):
        ipv = self.readByte()
        if ipv == 4:
            hostname_parts = []
            for part in range(4):
                hostname_parts.append(str(~self.readByte() & 0xff))
            hostname = ".".join(hostname_parts)
            port = self.readUnsignedShort()
            return hostname, port, ipv
        else:
            raise BinaryDataException('IP version is not 4')

    def write_address(self, address: tuple):
        if address[2] == 4:
            self.putByte(address[2])
            hostname_parts: list = address[0].split('.')
            for part in hostname_parts:
                self.putByte(~int(part) & 0xff)
            self.putShort(address[1])
        else:
            raise BinaryDataException('IP version is not 4')