import serial, socket

ser = serial.Serial("/dev/tty.usbserial-A700emuZ", 9600)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(("10.0.2.20", 6767)) 
s.listen(1)
client, address = s.accept()
print "connected"
while True: 
    data = client.recv(1).strip()
    print "got", data
    if data in ("L", "R", "U", "D"):
        ser.write(data)