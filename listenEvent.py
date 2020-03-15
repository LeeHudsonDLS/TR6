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

mainControlDMOV="""
<sequencer>
    <slave>1</slave>
    <get>
        <seq_state></seq_state>
    </get>
</sequencer>"""

mainControlGetSensor="""
<maincontrol>
    <slave>1</slave>
    <get_sensor>
        <sensor>0</sensor>
    </get_sensor>
</maincontrol> 
"""
#Get negative limit
getDriveReady="""
<digital_io>
    <slave>1</slave>
    <get>
        <input>1</input>
    </get>
</digital_io> 
"""


#Get negative limit
getNLimit="""
<digital_io>
    <slave>1</slave>
    <get>
        <input>3</input>
    </get>
</digital_io> 
"""

#Get positive limit
getPLimit="""
<digital_io>
    <slave>1</slave>
    <get>
        <input>2</input>
    </get>
</digital_io> 
"""

mainControlGet="""
<maincontrol>
    <slave>1</slave>
    <get></get>
</maincontrol> 
"""
mainControlSet0="""
<maincontrol>
    <slave>1</slave>
    <set>
        <sys_state>Ready</sys_state>
    </set>
</maincontrol> """

mainControlSet1="""
<maincontrol>
    <slave>1</slave>
    <set>
        <sys_state>Ready</sys_state>
    </set>
</maincontrol> """

clearUDP0="""
<udpxmit>
    <slave>0</slave>
    <clear></clear>
</udpxmit>"""

clearUDP1="""
<udpxmit>
    <slave>1</slave>
    <clear></clear>
</udpxmit>"""

register0="""
<udpxmit>
    <slave>0</slave>
    <register>
        <stream>phys14</stream>
    </register>
</udpxmit>"""

register1="""
<udpxmit>
    <slave>1</slave>
    <register>
        <stream>phys14</stream>
    </register>
</udpxmit>"""

start0="""
<udpxmit>
    <slave>0</slave>
    <start></start>
</udpxmit>"""

start1="""
<udpxmit>
    <slave>1</slave>
    <start></start>
</udpxmit>"""

startSeq0="""
<sequencer>
    <slave>1</slave>
    <set>
        <seq_state>program</seq_state>
        </set>
</sequencer>"""

startSeq1="""
<sequencer>
    <slave>1</slave>
    <set>
        <seq_state>program</seq_state>
        </set>
</sequencer>"""

class PCS8000UDPProtocol:
    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("UDP Connection made")

    def datagram_received(self, data, addr):
        code, slave, num_data, pkg_index, ts, min_drag, max_drag = \
              DATA_PACKAGE.unpack_from(data, offset=0)
        #print(f"Got {code}, {slave}, {num_data}, {pkg_index}, {ts}, {min_drag}, {max_drag}")
        data = struct.unpack("f" * num_data, data[DATA_PACKAGE.size:])

        print(data[0])

class PCS8000TCPProtocol:
    def __init__(self):
        self.transport = None
        self.remaining = {b'1,1.00,1234', b'0,1.00,1234'}

    def connection_made(self, transport):
        print("TCP Connection made")
        self.transport = transport
        print("Sending HELLO")
        self.transport.write(b"HELLO")

    def data_received(self, data):
        if data in self.remaining:
            # Controller registering
            self.remaining.remove(data)
            print("Sending OK")
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
        # Bring up event TCP server
        self.event_server = await loop.create_server(
            PCS8000TCPProtocol, "192.168.113.12", 51515)
        self.event_server_f = self.event_server.serve_forever()

        await asyncio.sleep(6000.0)
        

#DLS1.001234
#1,1.00
pcs = PCS8000("192.168.113.10")
asyncio.run(pcs.connect())
        
