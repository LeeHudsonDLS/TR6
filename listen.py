import asyncio
import socket
import struct

# Format of the UDP datagrams
DATA_PACKAGE = struct.Struct("<IIIQQff")

# Format of the TCP event packaged
EVENT_PACKAGE = struct.Struct("<IIQII")

# Name to send to controller for host identification
NAME = "DLS"
# Version of the controller protocol
VERSION = "1.00"
# Magic code, as set in the web interface
CODE = "1234"


class PCS8000UDPProtocol:
    def __init__(self):
        self.transport = None
        self.counter = 0

    def connection_made(self, transport):
        self.transport = transport
        print("UDP Connection made")

    def datagram_received(self, data, addr):
        code, slave, nData, pkgIndex, ts, minDrag, maxDrag = \
              DATA_PACKAGE.unpack_from(data, offset=0)
        print(f"Got {code}, {slave}, {nData}, {pkgIndex}, {ts}, {minDrag}, {maxDrag}")
        data = struct.unpack("f" * nData, data[DATA_PACKAGE.size:])
        self.counter+=1
        #print(f"{self.counter}{data[0]}\n")

class PCS8000TCPProtocol:
    def __init__(self):
        self.transport = None
        self.remaining = {b'1,1.00,1234', b'0,1.00,1234'}

    def connection_made(self, transport):
        print("TCP Connection made")
        self.transport = transport
        self.transport.write(b"HELLO")

    def data_received(self, data):
        if data in self.remaining:
            # Controller registering
            self.remaining.remove(data)
            self.transport.write(b"OK")
        else:
            ev_code, slave, ts, ev_value, num_data = \
                     EVENT_PACKAGE.unpack_from(data)
            print(f"Got {ev_code}, {slave}, {ts}, {ev_value}, {num_data}")
            if num_data:
                extra_data = data[EVENT_PACKAGE.size:]
                assert len(extra_data) == num_data
                    

class PCS8000:
    def __init__(self, ip):
        self.ip = ip
        self.reader, self.writer = None, None
        self.transport, self.protocol = None, None
        self.event_server = None
        self.event_server_f = None

    async def connect(self):
        loop = asyncio.get_running_loop()
        # Bring up UDP server
        self.transport, self.protocol = await loop.create_datagram_endpoint(
            PCS8000UDPProtocol, local_addr=("192.168.113.12", 51513))

        await asyncio.sleep(6000.0)


#DLS1.001234
#1,1.00
pcs = PCS8000("192.168.113.10")
asyncio.run(pcs.connect())
        
