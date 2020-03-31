from State import State
import xmltodict
import xml.etree.ElementTree as ET

class Pcs8000Controller:
    def __init__(self,slaveNo):
        self.slaveNo = slaveNo

        # List of stream values
        self.streamList = [0]*16
        self.sysState = State({"Busy":0,"Ready":1})
        self.seqState = State({"Setup":0,"Program":1})

    def setSysState(self,stateString):
        self.sysState.setState(stateString)
        print(f'Setting sys_state = "{stateString}" on slave {self.slaveNo}')


class Pcs8000ControllerMaster(Pcs8000Controller):
    def __init__(self):
        Pcs8000Controller.__init__(self,0)
        # Dict containing slaves, slave number is the key
        self.slaves = dict()
        # Set first element to be this object
        self.slaves[0] = self

    def addSlave(self,slave):
        self.slaves[int(slave.slaveNo)] = slave

    def parseCommand(self,command):
        commandRoot = ET.fromstring(command)
        addressedSlave = int(commandRoot[0].text)

        if commandRoot.tag == "udpxmit":
            print("UDP related command")

        if commandRoot.tag == "maincontrol":
            target = commandRoot[1][0].tag
            value = commandRoot[1][0].text.strip('"')
            if target == "sys_state":
                self.slaves[addressedSlave].setSysState(value)



master = Pcs8000ControllerMaster()
slave1 = Pcs8000Controller(1)
slave2 = Pcs8000Controller(2)

master.addSlave(slave1)
master.addSlave(slave2)


sysState = 0

with open("../xmlCommands/setSysState.xml") as xmlCommand:
    command = xmlCommand.read()

master.parseCommand(command)

print("End")







#tree = ET.parse("../xmlCommands/setSysState.xml")
#root = tree.getroot()
#print(root[1][0])