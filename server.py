import serial, socket, sys
from threading import Timer

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
    execute_commands([("left", 1000), ("right", speed*1000), ("right", 2000)])

timer = None
current_commands = []

def send_next():
    global current_commands, timer
    if len(current_commands) > 0:
        (cmd, timeout) = current_commands.pop(0)
        print "send_next", cmd, timeout
        timeout = timeout/1000.0
        if cmd == "left":
            left()
        elif cmd == "right":
            right()
        elif cmd == "up":
            up()
        elif cmd == "down":
            up()
        timer = Timer(timeout, send_next)
        timer.start()

def execute_commands(commands):
    global current_commands, timer
    current_commands = commands
    if timer and not timer.finished:
        timer.cancel()
    send_next()

def process_data(data):
    try:
        params = data.split(",")
        cmd = params.pop(0)
        if cmd == "G":
            if len(params) > 0:
                go(int(params[0]), int(params[1]))
            else:
                go()
        elif cmd == "S":
            execute_commands([])
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
    process_data(data)
client.close()
s.close()