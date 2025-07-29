import cv2
import socket
import pickle
import lgpio

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.7.56"
ADDR = (SERVER, PORT)

#these are the motors I will be using for the robot
FORWARD = 17
BACKWARD = 22
LEFT = 23
RIGHT = 24
FREQ = 1000

go = 0.0
steer = 0.0
h = lgpio.gpiochip_open(0)

lgpio.gpio_claim_output(h, FORWARD)
lgpio.gpio_claim_output(h, BACKWARD)
lgpio.gpio_claim_output(h, LEFT)
lgpio.gpio_claim_output(h, RIGHT)

cap = cv2.VideoCapture(0)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
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
                lgpio.gpio_write(h, BACKWARD, 0)
                lgpio.tx_pwm(h, FORWARD, FREQ, 100)
            else:
                lgpio.gpio_write(h, BACKWARD, 0)
                lgpio.tx_pwm(h, FORWARD, FREQ, int(99 * go) )
        elif go < 0:
            if go < -1:
                lgpio.gpio_write(h, FORWARD, 0)
                lgpio.tx_pwm(h, BACKWARD, FREQ, 100)
            else:
                lgpio.gpio_write(h, FORWARD, 0)
                lgpio.tx_pwm(h, BACKWARD, FREQ, int(99 * -go) )
        else:
            lgpio.gpio_write(h, FORWARD, 0)
            lgpio.gpio_write(h, BACKWARD, 0)
        
        msg_length = client.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = client.recv(msg_length).decode(FORMAT)

        steer = float(msg)
        if steer > 0:
            if steer > 1:
                lgpio.gpio_write(h, LEFT, 0)
                lgpio.tx_pwm(h, RIGHT, FREQ, 100)
            else:
                lgpio.gpio_write(h, LEFT, 0)
                lgpio.tx_pwm(h, RIGHT, FREQ, int(99 * steer) )
        elif steer < 0:
            if steer < -1:
                lgpio.gpio_write(h, RIGHT, 0)
                lgpio.tx_pwm(h, LEFT, FREQ, 100)
            else:
                lgpio.gpio_write(h, RIGHT, 0)
                lgpio.tx_pwm(h, LEFT, FREQ, int(99 * -steer) )
        else:
            lgpio.gpio_write(h, RIGHT, 0)
            lgpio.gpio_write(h, LEFT, 0)


ret, frame = cap.read()
send(pickle.dumps(frame))
input()
while cap.isOpened():
    ret, frame = cap.read()
    send(pickle.dumps(frame))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()