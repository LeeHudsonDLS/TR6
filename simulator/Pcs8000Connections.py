import logging
from Pcs8000Controller import Pcs8000Controller
from Pcs8000ControllerMaster import Pcs8000ControllerMaster
from threading import *
import socket

class Pcs8000Connection(Thread):
    def __init__(self, ipAddress, portNumber,masterController):
        Thread.__init__(self)
        self.masterController = masterController
        self.ipAddress = ipAddress
        self.portNumber = portNumber
        self.buffer = ""
        self.start()

    def serverHandShake(self,socket):
        # Send "HELLO\r\n"
        socket.send(f"HELLO\r\n".encode())

        # Wait for response code and check it's correct
        data = socket.recv(4096)
        assert data.rstrip()==b"DLS,1.00,1234","Driver sent %s" % data

        # Send "OK\r\n"
        socket.send(f"OK\r\n".encode())

    def clientHandShake(self,socket):
        # Wait for a "HELLO\r\n"
        data = socket.recv(4096)
        assert data==b"HELLO","Driver sent %s" % data
        print(f"Got : {data}")

        # Send "OK\r\n"
        socket.send(f"OK\r\n".encode())

class TCPCommandServer(Pcs8000Connection):
    def __init__(self,ipAddress,portNumber,masterController):
        Pcs8000Connection.__init__(self,ipAddress,portNumber,masterController)


    def run(self):

        # Configure the socket
        tcpCommandServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpCommandServer.bind((self.ipAddress, self.portNumber))
        tcpCommandServer.listen()
        print(f"Listening on {self.ipAddress}:{self.portNumber}")

        self.serverSocket, address = tcpCommandServer.accept()
        print("Client connected")

        self.serverHandShake(self.serverSocket)
        while True:
            self.buffer+=self.serverSocket.recv(4096).decode()
            if(self.buffer.count("</") == self.buffer.count("<")/2):
                response = self.masterController.parseCommand(self.buffer)
                self.serverSocket.send(response.encode())
                self.buffer=""


class TCPEventClient(Pcs8000Connection):
    def __init__(self,ipAddress,portNumber,masterController):
        Pcs8000Connection.__init__(self,ipAddress,portNumber,masterController)

    def run(self):

        # Configure the socket
        tcpEventClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while not connected:
            try:
                tcpEventClient.connect((self.ipAddress, self.portNumber))
                connected = True
            except Exception as e:
                pass
        self.clientHandShake(tcpEventClient)
        while True:
            data = tcpEventClient.recv(1024)