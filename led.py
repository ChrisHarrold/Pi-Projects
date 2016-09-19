import RPi.GPIO as GPIO
import time

#Define the pin we are going to use to power the LED
# the number of times it will blink
# and the time between blinks
pina = 6
interations = 10
interval = .50

#Turn on the GPIO commands and prepare the ports
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pina, GPIO.OUT)

#Create our loop to blink the LED based on our iterations value
for x in range(1, interations+1):

	#Turn on the LED and wait for the sleep interval
	print "Loop %d: LED on" % (x)
	GPIO.output(pina, GPIO.HIGH)
	time.sleep(interval)

	#Turn off the LED and wait for the sleep interval
	print "Loop %d: LED off" % (x)
	GPIO.output(pina, GPIO.LOW)
	time.sleep(interval)

#after all the blinks this command is important for resetting the GPIO board
GPIO.cleanup()
