import logging
from Pcs8000Controller import Pcs8000Controller
from Pcs8000ControllerMaster import Pcs8000ControllerMaster
from threading import *
import socket



class TCPCommandServer(Thread):
    def __init__(self, ipAddress, portNumber,masterController):
        Thread.__init__(self)
        self.masterController = masterController
        self.ipAddress = ipAddress
        self.portNumber = portNumber
        self.buffer = ""
        self.start()

    def handShake(self):
        # Send "HELLO\r\n"
        self.serverSocket.send(f"HELLO\r\n".encode())

        # Wait for response code and check it's correct
        data = self.serverSocket.recv(4096)
        assert data.rstrip()==b"DLS,1.00,1234","Driver sent %s" % data

        # Send "OK\r\n"
        self.serverSocket.send(f"OK\r\n".encode())

    def run(self):

        # Configure the socket
        tcpCommandServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpCommandServer.bind((self.ipAddress, self.portNumber))
        tcpCommandServer.listen()
        print(f"Listening on {self.ipAddress}:{self.portNumber}")

        self.serverSocket, address = tcpCommandServer.accept()
        print("Client connected")

        self.handShake()
        while True:
            self.buffer+=self.serverSocket.recv(4096).decode()
            if(self.buffer.count("</") == self.buffer.count("<")/2):
                response = self.masterController.parseCommand(self.buffer)
                self.serverSocket.send(response.encode())
                self.buffer=""