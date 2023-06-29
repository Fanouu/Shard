from time import time

from minepy.src.packets.Ack import Ack
from minepy.src.packets.BedrockProtocolInfo import BedrockType
from minepy.src.packets.Frame import Frame
from minepy.src.packets.FrameSet import FrameSet
from minepy.src.packets.Nack import Nack
from minepy.src.packets.OnlinePing import OnlinePing
from minepy.src.packets.OnlinePong import OnlinePong
from minepy.src.packets.Packet import Packet
from minepy.src.packets.ReliabilityTool import ReliabilityTool
from minepy.src.packets.client.ClientIncomingConnection import ClientIncomingConnection
from minepy.src.packets.client.ClientRequestConnection import ClientRequestConnection
from minepy.src.packets.server.ServerAcceptConnectionRequest import ServerAcceptConnectionRequest


class Client:
    address = None

    server = None
    serverSocket = None

    def __init__(self, server, address, mtu_size):
        self.address = address
        self.serverSocket = server.socketServer
        self.mtu_size: int = mtu_size
        self.server = server
        self.connected: bool = False
        self.recovery_queue: dict = {}
        self.ack_queue: list = []
        self.nack_queue: list = []
        self.fragmented_packets: dict = {}
        self.compound_id: int = 0
        self.client_sequence_numbers: list = []
        self.server_sequence_number: int = 0
        self.client_sequence_number: int = 0
        self.server_reliable_frame_index: int = 0
        self.client_reliable_frame_index: int = 0
        self.queue: FrameSet = FrameSet()
        self.channel_index: list = [0] * 32
        self.last_receive_time: float = time()

    def update(self):
        if (time() - self.last_receive_time) >= 10:
            self.disconnect()
        self.send_ack_queue()
        self.send_nack_queue()
        self.send_queue()

    def sendPacket(self, packet: Packet):
        self.server.getServerLogger().debug("Packet ID: " + str(packet.packet_id))
        self.server.socketServer.sendPacketTo(packet, self.address)

    def onRun(self, data):
        if data[0] == BedrockType.ACK:
            self.handle_ack(data)
        elif data[0] == BedrockType.NACK:
            self.handle_ack(data)
        elif BedrockType.frame_set_0 <= data[0] <= BedrockType.frame_set_f:
            self.handle_frame_set(data)

    def handle_ack(self, data: bytes) -> None:
        packet: Ack = Ack(data)
        packet.decode()
        for sequence_number in packet.sequence_numbers:
            if sequence_number in self.recovery_queue:
                del self.recovery_queue[sequence_number]

    def handle_nack(self, data: bytes) -> None:
        packet: Nack = Nack(data)
        packet.decode()
        for sequence_number in packet.sequence_numbers:
            if sequence_number in self.recovery_queue:
                lost_packet: Packet = self.recovery_queue[sequence_number]
                lost_packet.sequence_number = self.server_sequence_number
                self.server_sequence_number += 1
                lost_packet.encode()
                self.sendPacket(lost_packet)
                del self.recovery_queue[sequence_number]

    def handle_frame_set(self, data: bytes) -> None:
        packet: FrameSet = FrameSet(data)
        packet.decode()
        if packet.sequence_number not in self.client_sequence_numbers:
            if packet.sequence_number in self.nack_queue:
                self.nack_queue.remove(packet.sequence_number)
            self.client_sequence_numbers.append(packet.sequence_number)
            self.ack_queue.append(packet.sequence_number)
            hole_size = packet.sequence_number - self.client_sequence_number
            if hole_size > 0:
                for sequence_number in range(self.client_sequence_number + 1, hole_size):
                    if sequence_number not in self.client_sequence_numbers:
                        self.nack_queue.append(sequence_number)
            self.client_sequence_number: int = packet.sequence_number
            for frame_1 in packet.frames:
                if not ReliabilityTool.reliable(frame_1.reliability):
                    self.handle_frame(frame_1)
                else:
                    hole_size = frame_1.reliable_frame_index - self.client_reliable_frame_index
                    if hole_size == 0:
                        self.handle_frame(frame_1)
                        self.client_reliable_frame_index += 1

    def handle_fragmented_frame(self, packet: Frame) -> None:
        if packet.compound_id not in self.fragmented_packets:
            self.fragmented_packets[packet.compound_id]: dict = {packet.index: packet}
        else:
            self.fragmented_packets[packet.compound_id][packet.index]: int = packet
        if len(self.fragmented_packets[packet.compound_id]) == packet.compound_size:
            new_frame: Frame = Frame()
            for i in range(0, packet.compound_size):
                new_frame.body += self.fragmented_packets[packet.compound_id][i].body
            del self.fragmented_packets[packet.compound_id]
            self.handle_frame(new_frame)

    def handle_frame(self, packet: Frame) -> None:
        if packet.fragmented:
            self.server.getServerLogger().debug("FRAGMENTED")
            self.handle_fragmented_frame(packet)
        else:
            packetId = packet.body[0]
            if not self.connected:
                if packetId == ServerAcceptConnectionRequest.packet_id:
                    connectionRequestAccepted = ServerAcceptConnectionRequest(packet.body)
                    connectionRequestAccepted.decode()
                    clientIncoming = ClientIncomingConnection()
                    clientIncoming.server_address = self.serverSocket.getAddress()
                    clientIncoming.system_addresses = connectionRequestAccepted.system_addresses
                    clientIncoming.request_timestamp = connectionRequestAccepted.pong
                    clientIncoming.accepted_timestamp = self.serverSocket.getTime()
                    clientIncoming.encode()

                    new_frame: Frame = Frame()
                    new_frame.reliability = 0
                    new_frame.body = clientIncoming.data
                    self.add_to_queue(new_frame)
                    self.connected = True
                if packetId == BedrockType.CONNECTION_REQUEST:
                    connectionRequest = ClientRequestConnection(packet.body)
                    connectionRequest.decode()

                    serverAcceptRequest = ServerAcceptConnectionRequest()
                    serverAcceptRequest.client_address = self.address
                    serverAcceptRequest.system_index = 0
                    system_addresses = [("127.0.0.1", 0, 4)]
                    for i in range(0, 20):
                        system_addresses.append(("0.0.0.0", 0, 4))
                    serverAcceptRequest.system_addresses = system_addresses
                    serverAcceptRequest.ping = connectionRequest.ping
                    serverAcceptRequest.pong = self.serverSocket.getTime()
                    serverAcceptRequest.encode()

                    new_frame: Frame = Frame()
                    new_frame.reliability = 0
                    new_frame.body = serverAcceptRequest.data
                    self.add_to_queue(new_frame)
                elif packetId == BedrockType.NEW_INCOMING_CONNECTION:
                    self.server.getServerLogger().debug("INCOMING CONNECTION")
                    packet_1: ClientIncomingConnection = ClientIncomingConnection(packet.body)
                    packet_1.decode()
                    print(int(packet_1.server_address[1]))
                    print(int(self.server.getPort()))
                    if int(packet_1.server_address[1]) == int(self.server.getPort()):
                        self.connected: bool = True
                        # TODO: add attribute to player
            elif packetId == BedrockType.ONLINE_PING:
                onlinePing = OnlinePing(packet.body)
                onlinePing.decode()
                onlinePong = OnlinePong()
                onlinePong.client_timestamp = onlinePing.client_timestamp
                onlinePong.server_timestamp = int(time())
                onlinePong.encode()

                new_frame: Frame = Frame()
                new_frame.reliability = 0
                new_frame.body = onlinePong.data
                self.add_to_queue(new_frame, False)
            elif packetId == BedrockType.DISCONNECT:
                self.disconnect()
                print("DISCONNECTION ?")
            else:
                self.serverSocket.onFrameReceive(packet, self)
    def receivePacket(self, packet: Packet):
        data = packet.data
        packetId = data[0]
        self.server.getServerLogger().debug("Client receive packet")
        self.server.getServerLogger().debug("Packet ID: " + str(packetId))

    def disconnect(self):
        self.serverSocket.getClientManager().removeClient(self.address)

    def send_queue(self) -> None:
        if len(self.queue.frames) > 0:
            self.queue.sequence_number = self.server_sequence_number
            self.server_sequence_number += 1
            self.recovery_queue[self.queue.sequence_number]: object = self.queue
            self.queue.encode()
            self.sendPacket(self.queue)
            self.queue: FrameSet = FrameSet()

    def add_to_queue(self, packet: Frame, is_imediate: bool = True) -> None:
        if ReliabilityTool.reliable(packet.reliability):
            packet.reliable_frame_index = self.server_reliable_frame_index
            self.server_reliable_frame_index += 1
            if packet.reliability == 3:
                packet.ordered_frame_index = self.channel_index[packet.order_channel]
                self.channel_index[packet.order_channel] += 1
        if packet.get_size() > self.mtu_size:
            fragmented_body = []
            for i in range(0, len(packet.body), self.mtu_size):
                fragmented_body.append(packet.body[i:i + self.mtu_size])
            for index, body in enumerate(fragmented_body):
                new_packet: Frame = Frame()
                new_packet.fragmented = True
                new_packet.reliability = packet.reliability
                new_packet.compound_id = self.compound_id
                new_packet.compound_size = len(fragmented_body)
                new_packet.index = index
                new_packet.body = body
                if index != 0:
                    new_packet.reliable_frame_index = self.server_reliable_frame_index
                    self.server_reliable_frame_index += 1
                if new_packet.reliability == 3:
                    new_packet.ordered_frame_index = packet.ordered_frame_index
                    new_packet.order_channel = packet.order_channel
                if is_imediate:
                    self.queue.frames.append(new_packet)
                    self.send_queue()
                else:
                    frame_size = new_packet.get_size()
                    queue_size = self.queue.get_size()
                    if frame_size + queue_size >= self.mtu_size:
                        self.send_queue()
                    self.queue.frames.append(new_packet)
            self.compound_id += 1
        else:
            if is_imediate:
                self.queue.frames.append(packet)
                self.send_queue()
            else:
                frame_size = packet.get_size()
                queue_size = self.queue.get_size()
                if frame_size + queue_size >= self.mtu_size:
                    self.send_queue()
                self.queue.frames.append(packet)

    def send_ack_queue(self) -> None:
        if len(self.ack_queue) > 0:
            packet: Ack = Ack()
            packet.sequence_numbers = self.ack_queue
            self.ack_queue = []
            packet.encode()
            self.sendPacket(packet)

    def send_nack_queue(self) -> None:
        if len(self.nack_queue) > 0:
            packet: Nack = Nack()
            packet.sequence_numbers = self.nack_queue
            self.nack_queue = []
            packet.encode()
            self.sendPacket(packet)
