import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN) #PIR
GPIO.setup(21, GPIO.OUT) #LED

try:
    time.sleep(2) # to stabilize sensor
    while True:
        if GPIO.input(23):
        	strTime = str(time.time())
        	print("Motion Detected at time " + strTime)
            GPIO.output(21, True)
            time.sleep(1) #Buzzer turns on for 1 sec
            GPIO.output(24, False)
            time.sleep(5) #to avoid multiple detection
        time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()