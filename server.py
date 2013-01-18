import serial, socket

ser = None
try:
    ser = serial.Serial("/dev/tty.usbserial-A700emuZ", 9600)
except:
    print "no serial connection"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
port = 6767
print "listening on", host, port
s.bind((host, port)) 
s.listen(1)
client, address = s.accept()
print "connected"
while True: 
    data = client.recv(1)
    if data == '': break
    print "got", data
    if data in ("L", "R", "U", "D"):
        if ser is not None:
            ser.write(data)
client.close()
s.close()