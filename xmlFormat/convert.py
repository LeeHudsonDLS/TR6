
fin = open("test.xml","r")
data = fin.read()
data = data.replace(" ","")
data = data.replace("\r","")
data = data.replace("\n","")
data = data.replace("\t","")
fin.close
fin = open("test.txt","w")
fin.write(data)
fin.close
