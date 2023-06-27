import socket


class ServerSocket:
    socket = None
    ip = None
    port = None

    def __init__(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ip = ip
        self.port = port

    def start(self):
        self.socket.bind((self.ip, self.port))

        while True:
            data, serverAddress = self.socket.recvfrom(4096)
            self.onRun(data, serverAddress)

    def onRun(self, data, serverAddr):
        print(data)
        print(serverAddr)
