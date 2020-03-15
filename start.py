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
    <slave>0</slave>
    <get>
        <seq_state></seq_state>
    </get>
</sequencer>"""

mainControlGetSensor="""
<maincontrol>
    <slave>0</slave>
    <get_sensor>
        <sensor>0</sensor>
    </get_sensor>
</maincontrol> 
"""
#Get negative limit
getDriveReady="""
<digital_io>
    <slave>0</slave>
    <get>
        <input>1</input>
    </get>
</digital_io> 
"""


#Get negative limit
getNLimit="""
<digital_io>
    <slave>0</slave>
    <get>
        <input>3</input>
    </get>
</digital_io> 
"""

#Get positive limit
getPLimit="""
<digital_io>
    <slave>0</slave>
    <get>
        <input>2</input>
    </get>
</digital_io> 
"""

mainControlGet="""
<maincontrol>
    <slave>0</slave>
    <get></get>
</maincontrol> 
"""

mainControlSet="""
<maincontrol>
    <slave>0</slave>
    <set>
        <sys_state>Ready</sys_state>
    </set>
</maincontrol> """

clearUDP1="""
<udpxmit>
    <slave>1</slave>
    <clear></clear>
</udpxmit>"""

clearUDP="""
<udpxmit>
    <slave>0</slave>
    <clear></clear>
</udpxmit>"""

register1="""
<udpxmit>
    <slave>1</slave>
    <register>
        <stream>phys14</stream>
    </register>
</udpxmit>"""

register="""
<udpxmit>
    <slave>0</slave>
    <register>
        <stream>phys14</stream>
    </register>
</udpxmit>"""
start1="""
<udpxmit>
    <slave>1</slave>
    <start></start>
</udpxmit>"""
start="""
<udpxmit>
    <slave>0</slave>
    <start></start>
</udpxmit>"""

startSeq="""
<sequencer>
    <slave>0</slave>
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
        #self.transport, self.protocol = await loop.create_datagram_endpoint(
            #PCS8000UDPProtocol, local_addr=("192.168.113.12", 51513))
        # Bring up event TCP server
        #self.event_server_f = self.event_server.serve_forever()
        # Make connection
        self.reader, self.writer = await asyncio.open_connection(self.ip, 51512)
        # Initial handshake
        data = await self.reader.readline()
        print(data)
        assert data.rstrip() == b"HELLO", "Controller sent %s" % data
        self.writer.write(f"{NAME},{VERSION},{CODE}".encode())
        data = await self.reader.readline()
        print(data)
        assert data.rstrip() == b"OK", "Controller sent %s" % data
        # Check what mode it is in


        #print(await self.send_recv_xml(mainControlGet))
        # Set to Ready
        #await self.xml_cmd("maincontrol", "set", "sys_state", "Ready")
        # Setup streaming

        #print(await self.send_recv_xml(mainControlGetSensor))
        #await self.xml_cmd("udpxmit", "clear", "")
        #print(await self.send_recv_xml(mainControlSet))

        #print(await self.send_recv_xml(getNLimit))
        #print(await self.send_recv_xml(getPLimit))
        print(await self.send_recv_xml(clearUDP))
        print(await self.send_recv_xml(clearUDP1))
        await self.send_recv_xml(register)
        await self.send_recv_xml(register1)
        await self.send_recv_xml(start)
        await self.send_recv_xml(start1)

        #Enable drive

        #print(await self.send_recv_xml(mainControlDMOV))
        #await asyncio.sleep(1.0)
        #await self.send_recv_xml(mainControlSet)
        #print("Drive Enabled\n")
        #await asyncio.sleep(5.0)
        #print(await self.send_recv_xml(mainControlDMOV))
        #await self.xml_cmd("udpxmit", "register", "stream", "phys14")
        #await self.xml_cmd("udpxmit", "register", "stream", "phys1")
        #await self.xml_cmd("udpxmit", "start", "")
        # Setup events
        #await self.xml_cmd("eventcom", "start", "")
        # Wait for a bit
        #await asyncio.sleep(5.0)

        # Send a sequencer program down
        #xml = open(r"/dls/home/jjc62351/work/BL11K/TR6/doin7Base/RelativeMove.xml").read()
        #print("Sending XML\n")
        #await self.send_recv_xml(xml)
        #await self.send_recv_xml(startSeq)
        # Start the sequencer
        #await self.xml_cmd("sequencer", "set", "seq_state", "program")
        await asyncio.sleep(600.0)

    async def xml_cmd(self, *args):
        xml = ""
        for a in args[:-1]:
            xml += f"<{a}>"
        xml += args[-1]
        for a in reversed(args[:-1]):
            xml += f"</{a}>"
        #print(xml)
        return await self.send_recv_xml(xml)

    async def send_recv_xml(self, xml):
        xml = xml.rstrip()
        self.writer.write(xml.encode())
        marker = "</" + xml.rsplit("</", 1)[1]
        print(f"Marker = {marker}\n")
        try:
            data = await asyncio.wait_for(self.reader.readuntil(marker.encode()), timeout=1.0)
        except asyncio.TimeoutError:
            print("***\n" + self.reader._buffer.decode() + "\n***" + marker)
            raise
        ret = data.decode() + marker
        if "<ackn>OK</ackn>" not in ret:
            print("---\n" + ret)
        return ret

    def disconnect(self):
        self.reader.close()
        self.writer.close()

#DLS1.001234
#1,1.00
pcs = PCS8000("192.168.113.10")
asyncio.run(pcs.connect())
        
