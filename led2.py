#This will blink two properly prototyped LED connections in a cascade
import RPi.GPIO as GPIO
import time

# Set which pins we will use (adjust for your settings)
pina = 21
pinb = 6

# How many blinks and how far apart?
interations = 10
interval = .50

# Cleanup and set GPIO options
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pina, GPIO.OUT)
GPIO.setup(pinb, GPIO.OUT)

# Loop through the iterations you specified and blink your LEDS!
for x in range(1, interations+1):

	print "Loop %d: LED on" % (x)
	# This turns the port you specified on:
	GPIO.output(pina, GPIO.HIGH)
	# By removing this "sleep" you can turn on both simultaneously
	# instead of the "cascade" effect
	time.sleep(interval)
	GPIO.output(pinb, GPIO.HIGH)
	time.sleep(interval)

	print "Loop %d: LED off" % (x)
	# This turns it off:
	GPIO.output(pina, GPIO.LOW)
	# As above - remove this to turn off both lights at the same time
	# to prevent the "cascade" effect
	time.sleep(interval)
	GPIO.output(pinb, GPIO.LOW)
	time.sleep(interval)

# This line cleans everything up and makes sure you can do it all again!
GPIO.cleanup()
