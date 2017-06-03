__author__ = 'zhengwang'

import time
import serial
import pygame
from pygame.locals import *


class RCTest(object):

    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        self.ser = serial.Serial('/dev/cu.usbmodem1421', 115200, timeout=1)
        self.send_inst = True
        self.steer()

    def steer(self):

        # yeah = False;
        # while True:
        #     print("printing char:", chr(1))
        #     time.sleep(1)
        #     if yeah:
        #         ser.write(chr(1))    
        #     else:
        #         ser.write(chr(0))   
        #     yeah = not yeah
        # return
        while self.send_inst:
            for event in pygame.event.get():
                # print("hi")
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()
                    move_car(key_input, self.ser)
                    

                elif event.type == pygame.KEYUP:
                    key_input = pygame.key.get_pressed()
                    move_car(key_input, self.ser)
                    # ser.write(b'0')

                time.sleep(.001)

def move_car(key_input, ser):
    # complex orders
    if key_input[pygame.K_UP] and key_input[pygame.K_RIGHT]:
        print("Forward Right")
        ser.write(b'6')

    elif key_input[pygame.K_UP] and key_input[pygame.K_LEFT]:
        print("Forward Left")
        ser.write(b'7')

    elif key_input[pygame.K_DOWN] and key_input[pygame.K_RIGHT]:
        print("Reverse Right")
        ser.write(b'8')

    elif key_input[pygame.K_DOWN] and key_input[pygame.K_LEFT]:
        print("Reverse Left")
        ser.write(b'9')

    # simple orders
    elif key_input[pygame.K_UP]:
        print("Forward")
        ser.write(b'1')

    elif key_input[pygame.K_DOWN]:
        print("Reverse")
        ser.write(b'2')

    elif key_input[pygame.K_RIGHT]:
        print("Right")
        ser.write(b'3')

    elif key_input[pygame.K_LEFT]:
        print("Left")
        ser.write(b'4')

    # exit
    elif key_input[pygame.K_x] or key_input[pygame.K_q]:
        print('Exit')
        self.send_inst = False
        ser.write(b'0')
        self.ser.close()
    else:
        ser.write(b'0')

if __name__ == '__main__':
    RCTest()
