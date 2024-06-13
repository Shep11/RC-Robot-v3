import cv2
import socket
import pickle

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
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

def update(msg):
    message = msg
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    msg_length = client.recv(HEADER).decode(FORMAT)
    if msg_length:
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)

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
        msg_length = client.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)

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
        break
cap.release()