import xml.dom.minidom
from subprocess import Popen, PIPE

stdout = Popen('ls | grep .txt', shell=True, stdout=PIPE).stdout
xmlFiles = stdout.read().split()
print(xmlFiles)

for a in xmlFiles:
    print(f"Converting {a}")
    doc = xml.dom.minidom.parse(a.decode())
    pretty_xml_as_string= doc.toprettyxml()
    fin = open(a.decode().replace(".txt",".xml"),"w")
    fin.write(pretty_xml_as_string)
    fin.close()
