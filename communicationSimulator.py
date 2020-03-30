# This script simulates the laserPuckPointer hardware to allow testing of the support module and
# streamDevice. Run this on a local machine and point the AsynIP port to localhost:8000.

import socket
from threading import *


class server(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
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
        self.sock.send(f"HELLO\r\n".encode())

        # Wait for response code and check it's correct
        data = self.sock.recv(4096)
        assert data.rstrip()==b"DLS,1.00,1234","Driver sent %s" % data

        # Send "OK\r\n"
        self.sock.send(f"OK\r\n".encode())

    def run(self):
        self.handShake()
        while(1==1):
            self.buffer+=self.sock.recv(4096).decode()
            if(self.buffer.count("</") == self.buffer.count("<")/2):
                print("Got xml:")
                print(self.buffer)
                self.buffer=""


# Ports:
tcpCommandPort = 51512
udpStreamPort = 51513
tcpEventPort = 51515


# Server for main TCP comms. Server is controller
tcpCommandServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpCommandServer.bind(("localhost", tcpCommandPort))


tcpCommandServer.listen()
print ('TCP command server started and listening')
while 1:
    print ('Waiting for connection')
    serverSocket, address = tcpCommandServer.accept()
    print ('Connection received')
    server(serverSocket, address)
