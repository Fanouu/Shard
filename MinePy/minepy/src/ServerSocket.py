import socket
from threading import Thread

from minepy.src import Server
from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet
from minepy.src.packets.UnconnectedPing import UnconnectedPing
from minepy.src.packets.UnconnectedPong import UnconnectedPong


class ServerSocket(Thread):
    socket = None

    ip = None
    port = None

    server = None

    def __init__(self, server, ip, port):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.port = int(port)
        self.server = server

    def sendPacketTo(self, packet: Packet, address):
        packet.encode()
        if self.server.isDev():
            self.server.getServerLogger().debug("packet sent: " + str(packet.data[1:]))
        self.socket.sendto(packet.data, address)

    def run(self) -> None:
        self.socket.bind((self.ip, self.port))
        while True:
            data, clientAddress = self.socket.recvfrom(4096)
            self.onRun(data, clientAddress)

    def onRun(self, data, clientAddress):
        packetId = data[0]

        if self.server.isDev():
            self.server.getServerLogger().debug("packet receive: " + str(data))

        if packetId == BedrockType.UNCONNECTED_PING:
            packet = UnconnectedPing(data)
            packet.decode()
            pongPacket = UnconnectedPong()
            pongPacket.client_timestamp = packet.client_timestamp
            pongPacket.serverData = self.server.getServerDataForPonPacket()
            pongPacket.serverGUID = self.server.SERVER_UUID
            pongPacket.magic = packet.magic

            self.sendPacketTo(pongPacket, clientAddress)
