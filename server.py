import socket 
from shark import Sharkduino

#shark = Sharkduino()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(("10.0.2.20", 6767)) 
s.listen(1)
client, address = s.accept()
print "connected"
while True: 
    data = client.recv(1).strip()
    print "got", data
    if data in ("L", "R", "U", "D"):
        pass #shark
    else:
        break
client.close()