import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

i = 0
GPIO.setup(23, GPIO.IN) #PIR
GPIO.setup(21, GPIO.OUT) #LED
GPIO.output(21, False)

try:
	print("Starting up")
	time.sleep(2) # to stabilize sensor
	while True:
		if GPIO.input(23):
			GPIO.output(21, True)
			now = time.strftime("%H:%M", time.localtime(time.time()))
			print("Motion detected ") + str(now)
			time.sleep(2) #to avoid multiple detection
			GPIO.output(21, False)
		time.sleep(0.1) #loop delay, should be less than detection delay
		i = i + 1

except KeyboardInterrupt:
	print("")
	print("Stopped by User")
	GPIO.cleanup()