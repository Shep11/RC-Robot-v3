import cv2
import socket
import pickle

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
IMGTEXT = "!IMG"
DISCONNECT_MESSAGE = "!DISCONNECT"
GO_VAL = "!GO"
STEER_VAL = "!STEER"
SERVER = "192.168.7.56"
ADDR = (SERVER, PORT)

#these are the motors I will be using for the robot
motorS = Motor(24, 23)
motorG = Motor(17, 27)

go = 0.0
steer = 0.0

cap = cv2.VideoCapture(0)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg, conn):
    message = msg
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def recieve(conn):
    msg_length = conn.recv(HEADER).decode(FORMAT)
    if msg_length:
        if msg_length > 4096:
            msgb = b""
            while msg_length > 4096:
                pack = conn.recv(4096)
                msg_length -= 4096
                msgb += pack
            pack = conn.recv(msg_length)
            msgb += pack
            return msgb
        else:
            msg = conn.recv(msg_length)
            return msg

def update(msg):
    send(IMGTEXT, client)
    send(msg, client)
    
    msg = recieve(client)
    if msg == GO_VAL:
        msg = recieve(client)
        go = float(msg)
        if go > 0:
            if go > 1:
                motorG.backward(1)
            else:
                motorG.backward(go)
        elif go < 0:
            if go < -1:
                motorG.forward(1)
            else:
                motorG.forward(-go)
        else:
            motorG.stop()
    
    msg = recieve(client)
    if msg == STEER_VAL:
        msg = recieve(client)
        steer = float(msg)
        if steer > 0:
            if steer > 1:
                motorS.backward(1)
            else:
                motorS.backward(steer)
        elif steer < 0:
            if steer < -1:
                motorS.forward(1)
            else:
                motorS.forward(-steer)
        else:
            motorS.stop()


ret, frame = cap.read()
update(pickle.dumps(frame))
input()
while cap.isOpened():
    ret, frame = cap.read()
    update(pickle.dumps(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        send(DISCONNECT_MESSAGE, client)
        break
cap.release()