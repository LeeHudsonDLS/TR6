import asyncio
import socket
import struct

async def send_recv_xml(xml):
    xml = xml.rstrip()
    print(xml.encode())
    marker = "</" + xml.rsplit("</", 1)[1]
    #try:
        #data = await asyncio.wait_for(self.reader.readuntil(marker.encode()), timeout=1.0)
    #except asyncio.TimeoutError:
        #print("***\n" + self.reader._buffer.decode() + "\n***" + marker)
        #raise
    #ret = data.decode() + marker
    if "<ackn>OK</ackn>" not in ret:
        print("---\n" + ret)
    return ret

xml = open(r"/home/jjc62351/work/BL11K/TR6/cutdown.xml").read()
send_recv_xml(xml)
