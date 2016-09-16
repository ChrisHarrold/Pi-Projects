import RPi.GPIO as GPIO
import time

pina = 21
pinb = 20
interations = 10
interval = .50

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pina, GPIO.OUT)
GPIO.setup(pinb, GPIO.OUT)

for x in range(1, interations+1):

	print "Loop %d: LED on" % (x)
	GPIO.output(pina, GPIO.HIGH)
	time.sleep(interval)
	GPIO.output(pinb, GPIO.HIGH)
	time.sleep(interval)

	print "Loop %d: LED off" % (x)
	GPIO.output(pina, GPIO.LOW)
	time.sleep(interval)
	GPIO.output(pinb, GPIO.LOW)
	time.sleep(interval)

GPIO.cleanup()
