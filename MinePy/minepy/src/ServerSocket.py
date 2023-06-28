import socket
from threading import Thread

from minepy.src import Server
from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Packet import Packet
from minepy.src.packets.UnconnectedPing import UnconnectedPing
from minepy.src.packets.UnconnectedPong import UnconnectedPong
from minepy.src.packets.client.ClientOpenConnection import ClientOpenConnection
from minepy.src.packets.client.ClientTestConnection1 import ClientTestConnection1
from minepy.src.packets.client.IncompatibleRaknetProtocolVersion import IncompatibleRaknetProtocolVersion
from minepy.src.packets.server.ClientOpenConnectionReply import ClientOpenConnectionReply
from minepy.src.packets.server.ClientTestConnection1Reply import ClientTestConnection1Reply


class ServerSocket(Thread):
    socket = None

    ip = None
    port = None

    server = None

    clients = []

    def __init__(self, server, ip, port):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.SOL_UDP)
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
            data, clientAddress = self.socket.recvfrom(65535)
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
        if packetId == BedrockType.CLIENT_TESTCONNECTION1:
            packet = ClientTestConnection1(data)
            packet.decode()

            self.server.getServerLogger().debug("Opening Connection on: " + str(clientAddress[0]) + ":" + str(clientAddress[1]) + "\nRaknet Version: " + str(packet.raknet_protocol_version))
            if int(packet.raknet_protocol_version) == int(self.server.BEDROCK_PROTOCOL_VERSION):
                replyPacket = ClientTestConnection1Reply()
                replyPacket.magic = packet.magic
                replyPacket.server_uid = self.server.SERVER_UUID
                replyPacket.raknet_null_padding = packet.raknet_null_padding

                self.sendPacketTo(replyPacket, clientAddress)
            else:
                incompatiblePacket = IncompatibleRaknetProtocolVersion()
                incompatiblePacket.server_uid = self.server.SERVER_UUID
                incompatiblePacket.raknet_protocol_version = self.server.BEDROCK_PROTOCOL_VERSION
                incompatiblePacket.magic = packet.magic

                self.sendPacketTo(incompatiblePacket, clientAddress)
        if packetId == BedrockType.CLIENT_OPENCONNECTION:
            packet = ClientOpenConnection(data)
            packet.decode()

            replyPacket = ClientOpenConnectionReply()
            replyPacket.magic = packet.magic
            replyPacket.server_uid = self.server.SERVER_UUID
            replyPacket.client_address = clientAddress
            replyPacket.mtu = packet.mtu

            self.sendPacketTo(replyPacket, clientAddress)
