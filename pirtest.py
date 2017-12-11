import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

i = 0
GPIO.setup(23, GPIO.IN) #PIR
GPIO.setup(21, GPIO.OUT) #LED

try:
	time.sleep(2) # to stabilize sensor
	while i < 21:
		if GPIO.input(23):
			GPIO.output(21, True)
			time.sleep(1) #LED turns on for 1 sec
			GPIO.output(24, False)
			strTime = str(time.time())
			print("Motion Detected at time " + strTime)
			time.sleep(5) #to avoid multiple detection
		time.sleep(0.1) #loop delay, should be less than detection delay
		i = i + 1

except:
	GPIO.cleanup()