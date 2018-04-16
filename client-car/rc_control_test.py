__author__ = 'Kamal, Mike, Mochan'

import time
import serial
import pygame
from pygame.locals import *
from ports import get_serial_ports
import ultrasonic_stop

class RCTest(object):

    def __init__(self):
        ports = get_serial_ports()
        self.ser = self.select_port(ports)
        pygame.init()
        screen = pygame.display.set_mode((400, 300))
        self.send_inst = True
        self.steer()
        self.stopping = False

    def select_port(self, port_list):
        # remove known ports that might get in the way
        for p in port_list:
            if 'bluetooth' in p.lower():
                port_list.remove(p)

        if len(port_list) == 1:
            print("connecting to", port_list[0])
            return serial.Serial(port_list[0], 115200, timeout=1)
        else:
            print(port_list)

        print("Multiple ports detected:")
        i = 0
        for port in port_list:
            print(i,port)
            i+=1
        selected = int(input("please select the port you would like: "))
        print("you selected",selected, "(",port_list[selected],")")
        return serial.Serial(port_list[selected], 115200, timeout=1)


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
                else:
                    stopping = False
                    move_car_auto(self.ser, stopping)

                time.sleep(1)

def move_car_auto(ser, stopping):
    sensor = ultrasonic_stop.SensorStreamingTest()

    for val in sensor.streaming():
        if val < 100:
            # stopping = True

            if stopping == False:
                stopping = True
                stop_time = time.time()
            if time.time() - stop_time < 0.5:

                ser.write(b'2')
            else:
                ser.write(b'0')

            # print("stopped")
            # continue
        else:
            stopping = False
            ser.write(b'1')

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
