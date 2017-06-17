import RPi.GPIO as GPIO
import time
import sys
import numpy as np
GPIO.setmode(GPIO.BCM)

TRIG = 23 
ECHO = 24

print ("Distance Measurement In Progress")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print ("Waiting For Sensor To Settle")
time.sleep(2)

data = [0,0,0]

while (True):
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
	  pulse_start = time.time()

	while GPIO.input(ECHO)==1:
	  pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150
	
	flength = 40
	fmax = 400

	distance = round(distance, 2)
	
	data.pop(0)
	data.append(distance)
	filtered = min(data)
	
	if filtered > fmax:
		dist = flength
	else:
		dist = int(filtered/(fmax/flength))

	#print ("Distance:",distance,"cm")
	sys.stdout.write("\r Distance {0:^8} [{1:.40}]".format(filtered ,'#'*(dist)+" "*flength))
	sys.stdout.flush()
	
	time.sleep(0.1)

GPIO.cleanup()
