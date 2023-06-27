import socket

from minepy.src.packets.BedrockProtocol import type
from minepy.src.packets.Packet import Packet
from minepy.src.packets.UnconnectedPing import UnconnectedPing


class ServerSocket:
    socket = None
    ip = None
    port = None

    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.port = int(port)

    def sendPacketTo(self, packet: Packet, address):
        packet.encode()
        self.socket.sendto(packet.data, address)
    def start(self):
        self.socket.bind((self.ip, self.port))

        while True:
            data, clientAddress = self.socket.recvfrom(4096)
            self.onRun(data, clientAddress)

    def onRun(self, data, clientAddress):
        print(data)
        print(clientAddress)
        packetId = data[0]

        print(packetId)
        print(type.UNCONNECTED_PING)
        if packetId == type.UNCONNECTED_PING:
            packet = UnconnectedPing(data)
            packet.decode()
            print(packet.toDict())
            print("succes")
