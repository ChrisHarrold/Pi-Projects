#Libraries
import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
	#allow sensor to settle
	
    # set Trigger to HIGH
    print("Turning on Sensor")
    GPIO.output(GPIO_TRIGGER, True)
    
    # set Trigger after 0.01ms to LOW
    time.sleep(0.05)
    print("Turning Off Sensor")
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    print("Waiting for starttime")
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    print("Waiting for end time")
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    print(distance)
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
        	print ("Waiting to settle sensor")
        	GPIO.output(GPIO_TRIGGER, False)
        	time.sleep(2)
        	dist = distance()
        	print ("Measured Distance = %.1f cm" % dist)
        	time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()