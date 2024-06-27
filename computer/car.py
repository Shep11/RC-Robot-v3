import pygame
import pickle
import cv2
from pygame.locals import *

IMGTEXT = "!IMG"
DISCONNECT_MESSAGE = "!DISCONNECT"
GO_VAL = "!GO"
STEER_VAL = "!STEER"
FORMAT = 'utf-8'
HEADER = 64

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
        else:
            msg = conn.recv(msg_length)




class car:
    def __init__(self, conn, addr, controler, name):
        self.conn = conn
        self.addr = addr
        self.controler = controler
        self.name = name
    
    def update(self):
        msg = recieve(self.conn).decode(FORMAT)

        if msg == IMGTEXT:
            img = pickle.loads(recieve(self.conn))
            cv2.imshow(f"car {self.name}", img)
        
        elif msg == DISCONNECT_MESSAGE:
            self.conn.close()
            return False
        
        for event in pygame.event.get():
            if event.type == JOYAXISMOTION:
                print("AXISb : " + str(event.axis))
                if event.axis == 0:
                    if event.value > 0.2 or event.value < -0.2:
                        print(event.value)
                        self.steer = -round((event.value), 2)
                    else:
                        self.steer = 0
                if event.axis == 5:
                    print(round((event.value * -1) - 2 * 0.5, 2))
                    if round((event.value * -1) - 2 * 0.5, 2) > 0.1 or round((event.value * -1) - 2 * 0.5, 2) + 1 < -0.1:
                        self.go = round((event.value * -1) - 1 * 0.25, 2)
                    else:
                        self.go = 0
                if event.axis == 4:
                    print(round((event.value) + 2 * 0.5, 2))
                    if (round((event.value) + 2 * 0.5, 2)) > 0.1 or (round((event.value) + 2 * 0.5, 2)) < -0.1:
                        self.go = round((event.value) + 1 * 0.25, 2)
                    else:
                        self.go = 0
            if event.type == QUIT:
                pygame.quit()
        
        send(GO_VAL, self.conn)
        send(self.go, self.conn)
        send(STEER_VAL, self.conn)
        send(self.steer, self.conn)

        return True
        
