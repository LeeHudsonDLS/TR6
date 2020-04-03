import logging
from Pcs8000Controller import Pcs8000Controller
from Pcs8000ControllerMaster import Pcs8000ControllerMaster
from threading import *
import socket

class TCPEventClient(Thread):
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
        tcpEventClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connected = False
        while not connected:
            try:
                tcpEventClient.connect((self.ipAddress, self.portNumber))
                connected = True
            except Exception as e:
                pass
        data = tcpEventClient.recv(1024)
        print(f"TCP Event port got {data.decode()}")