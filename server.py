import serial, socket, sys

ser = None
try:
    ser = serial.Serial("/dev/tty.usbserial-A700emuZ", 9600)
except:
    print "no serial connection"
    ser = sys.stdout


def up():
    ser.write("U")

def down():
    ser.write("D")

def left():
    ser.write("L")

def right():
    ser.write("R")

def stop():
    ser.write("S")

def go(speed=5, direction=0):
    if not (0 <= speed <= 10 and -90 <= direction <= 90):
        return

    pass

def process_command(data):
    try:
        params = data.split(",")
        cmd = params.pop(0)
        if cmd == "U":
            up()
        elif cmd == "D":
            down()
        elif cmd == "L":
            left()
        elif cmd == "R":
            right()
        elif cmd == "G":
            if len(params) > 0:
                go(int(params[0]), int(params[1]))
            else:
                go()
    except Exception, e:
        print "error when processing", e

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
    process_command(data)
client.close()
s.close()