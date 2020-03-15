
fin = open("force.xml","r")
data = fin.read()
data = data.replace(" ","")
data = data.replace("\r","")
data = data.replace("\n","")
fin.close
fin = open("seqDownload.txt","w")
fin.write(data)
fin.close
