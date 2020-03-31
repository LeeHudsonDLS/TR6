# This script simulates the laserPuckPointer hardware to allow testing of the support module and
# streamDevice. Run this on a local machine and point the AsynIP port to localhost:8000.

import socket
from Pcs8000Controller import Pcs8000Controller
from threading import *


class tcpServer(Thread):
    def __init__(self, ipAddress, portNumber,masterController):
        Thread.__init__(self)
        self.masterController = masterController
        self.ipAddress = ipAddress
        self.portNumber = portNumber
        self.buffer = ""
        self.start()
        self.data = {
            "P":101,
            "T":102,
            "M":'R',
            "L":0
        }

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
                print("Got xml:")
                print(self.buffer)
                self.buffer=""



# Ports:
tcpCommandPort = 51512
udpStreamPort = 51513
tcpEventPort = 51515

# Create controller objects:
masterController = Pcs8000Controller(0)

# Create main TCP command server
tcpServer("localhost",tcpCommandPort,masterController)