from socket import *
import time
import RPi.GPIO as GPIO

# read server IP from file
file = open('server_ip.txt','r') 
serverIP = file.read() 
file.close()


GPIO.setwarnings(False)

# create a socket and bind socket to the host
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((serverIP, 8002))

def measure():
  GPIO.output(GPIO_TRIGGER, True)
  time.sleep(0.00001)
  GPIO.output(GPIO_TRIGGER, False)
  start = time.time()

  while GPIO.input(GPIO_ECHO)==0:
    start = time.time()

  while GPIO.input(GPIO_ECHO)==1:
    stop = time.time()

  elapsed = stop-start
  distance = (elapsed * 34300)/2

  return distance

# referring to the pins by GPIO numbers
GPIO.setmode(GPIO.BCM)

# define pi GPIO
GPIO_TRIGGER = 23
GPIO_ECHO    = 24

# output pin: Trigger
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
# input pin: Echo
GPIO.setup(GPIO_ECHO,GPIO.IN)
# initialize trigger pin to low
GPIO.output(GPIO_TRIGGER, False)

try:
    while True:
        distance = measure()
        print "Distance : %.1f cm" % distance
        # send data to the host every 0.5 sec
        client_socket.send(str(distance))
        time.sleep(0.05)
finally:
    client_socket.close()
    GPIO.cleanup()
