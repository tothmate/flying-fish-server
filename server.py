import serial, socket

ser = None
try:
    ser = serial.Serial("/dev/tty.usbserial-A700emuZ", 9600)
except:
    print "no serial connection"


def up(length=100):
    ser.write("U %d\n" % length)

def down(length=100):
    ser.write("D %d\n" % length)

def left(length=100):
    ser.write("L %d\n" % length)

def right(length=100):
    ser.write("R %d\n" % length)

def swim(length=10):
    for i in xrange(0, length):
        left(80)
        right(160)
        left(80)

def process_command(data):
    if data == "U":
        up()
    elif data == "D":
        down()
    elif data == "L":
        left()
    elif data == "R":
        right()
    elif data == "S":
        swim()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = socket.gethostbyname(socket.gethostname())
port = 6767
print "listening on", host, port
s.bind((host, port)) 
s.listen(1)
client, address = s.accept()
print "connected"
while True: 
    data = client.recv(1024)
    if data == '': break
    data = data.strip()
    print "got", data
    if ser is not None:
        process_command(data)
client.close()
s.close()