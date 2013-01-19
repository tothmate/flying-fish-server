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
    ser.flush()

def down():
    ser.write("D")
    ser.flush()

def left():
    ser.write("L")
    ser.flush()

def right():
    ser.write("R")
    ser.flush()

def stop():
    ser.write("S")
    ser.flush()

def go(speed=5, direction=0):
    if not (1 <= speed <= 10 and -90 <= direction <= 90):
        return

    cmd_length = 3000
    cmd_queue = []

    while cmd_length > 0:
        movement_length = 1200 - speed*60
        right_movement_length = int(movement_length/2 + (movement_length*4/10)*(direction/90.0))
        left_movement_length = movement_length - right_movement_length
        cmd_queue.append(("right", right_movement_length))
        cmd_queue.append(("left", left_movement_length))
        cmd_length -= movement_length

    execute_commands(cmd_queue)

timer = None
current_commands = []

def send_next():
    global current_commands, timer
    if len(current_commands) > 0:
        (cmd, timeout) = current_commands.pop(0)
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
    else:
        stop()

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
print "client connected"
while True: 
    data = client.recv(1024)
    if data == '': break
    data = data.strip()
    print "\ngot", data
    process_data(data)
print "client disconnected"
client.close()
s.close()
