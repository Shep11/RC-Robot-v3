import pygame
from pygame.locals import *


HEADER = 64

class car:
    def __init__(self, conn, addr, controler, name):
        self.conn = conn
        self.addr = addr
        self.controler = controler
        self.name = name
    
    def update(self):
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
