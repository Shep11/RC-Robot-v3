import socket
import pygame
import pickle
import car
import cv2
from pygame.locals import *

# the message lenght length
HEADER = 64

# the port I chose for the robot I chose it because there shouldn't be anything on it
PORT = 5500
#puts the server on the host ip adress
SERVER = socket.gethostbyname(socket.gethostname())
#the address of the server
ADDR = (SERVER, PORT)
#the encoding format
FORMAT = 'utf-8'
#the text for reciving an image
IMGTEXT = "!IMG"
#the text to disconnect from the server
DISCONNECT_MESSAGE = "!DISCONNECT"
#the fps of the video feed
FPS = 60

#the forward vector
go = 0
#the steering vector negative is left positive is right
steer = 0

#initializes the joysticks
pygame.init()
pygame.joystick.init()

#gets a list of joysticks connected to the pc
joysticks = []
for i in range (pygame.joystick.get_count()):
    
    joysticks.append(pygame.joystick.Joystick(i))
    
    print("detected joystick " + joysticks[-1].get_name())


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def controler_MSG(conn, addr):
    global go
    global steer

    for event in pygame.event.get():
        if event.type == JOYAXISMOTION:
            print("AXISb : " + str(event.axis))
            if event.axis == 0:
                if event.value > 0.2 or event.value < -0.2:
                    print(event.value)
                    steer = -round((event.value), 2)
                else:
                    steer = 0
            if event.axis == 5:
                print(round((event.value * -1) - 2 * 0.5, 2))
                if round((event.value * -1) - 2 * 0.5, 2) > 0.1 or round((event.value * -1) - 2 * 0.5, 2) + 1 < -0.1:
                    go = round((event.value * -1) - 1 * 0.25, 2)
                else:
                    go = 0
            if event.axis == 4:
                print(round((event.value) + 2 * 0.5, 2))
                if (round((event.value) + 2 * 0.5, 2)) > 0.1 or (round((event.value) + 2 * 0.5, 2)) < -0.1:
                    go = round((event.value) + 1 * 0.25, 2)
                else:
                    go = 0
        if event.type == QUIT:
            pygame.quit()
    msg = str(go).encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(msg)

    msg = str(steer).encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(msg)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            if msg_length > 4096:
                msgb = b""
                while msg_length > 4096:
                    pack = conn.recv(4096)
                    msg_length -= 4096
                    msgb += pack
                pack = conn.recv(msg_length)
                msgb += pack
                msg = pickle.loads(msgb)
            else:
                msg =  pickle.loads(conn.recv(msg_length))
            controler_MSG(conn, addr)
            cv2.imshow("result.jpg", msg)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        pygame.time.Clock().tick(FPS)
        
    conn.close()

def createCar(conn, addr):
    cool = 0
    print("joysticks: ")
    for i in joysticks:
        print(str(cool) + " " + i.get_name())
        cool += 1
    
    while True:
        next = int(input("whitch joystick?"))
        if (next >= 0 and next < cool):
            stick = joysticks[next]
            break
        else:
            print("invalid joystick")

    stick.init()

    name = input("Enter a name: ")

    return car(conn, addr, stick, name)

def start():
    server.listen()
    print(f"[LISTENTING] Server is listenting on {SERVER}")
    cars = []
    while True:
        conn, addr = server.accept()
        cars.append(createCar(conn, addr))
        check = input("connected everyone? ")
        if (check[0] == 'y'):
            break
    while True:
        for c in cars:
            c.update()

print("[Starring] starting the server ...")
start()