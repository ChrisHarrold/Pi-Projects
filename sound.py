# Import libraries used in this program
import RPi.GPIO as GPIO
import time
from decimal import *
import math
getcontext().prec = 4

# I will be outputting to a website for a real-time view of noise detection events
# This is the placeholder code for that
#with open('/var/www/html/sound.html', 'w') as the_file:
#	the_file.write('<H1>This is more usefull stuff</H1>\n')

# Startup message
print "Preparing to monitor sound levels"

# Set our variables and pin assignments
input_digital = 18
red_led = 21
green_led = 20
Is_Loud = "No"
Loud_Count = 0
loop_count = 0
per_detected = 0
time_loop = 15

# This value is the final threshold where the system will take action
# it is the value of the number of times loud sound was detected
# versus the number of times the sensor was polled. Unless
# you are looking for spikes amidst loud noise, this number will be
# likely be .01 or even significantly less
a_threshold = .01

# How long between sound level checks - not required, but you 
# can slow it down if needed for debuging or just for funsies
interval = .5

# Setup GPIO commands and pins and cleanup pins in case of errors
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(input_digital, GPIO.IN)

# Make sure the pins start off in the LOW state
GPIO.output(green_led, GPIO.LOW)
GPIO.output(red_led, GPIO.LOW)

# Then turn on the green - no noise light - and confirm system is online.
GPIO.output(green_led, GPIO.HIGH)
GPIO.output(red_led, GPIO.LOW)
print "GPIO set. Service starting. Press ctrl-c to break"

# Main try block to handle the exception conditions
try:	

	# Primary monitor is a "while" loop that will keep the monitor running 
	# indefinitely as a soft service.
	#
	# This first syntax will lock the loop into a time window, 5 seconds 
	# by default as definied by the time_loop variable.
	# This is extremely useful for debugging, and for threshold detection.
	#
	# The microphone sensor is notoriously hard to tune for threshold
	# and having this will allow you to figure out the number of events
	# in a fixed window of time. This means you can divide by the number
	# of events versus the number of times the monitor looked for an event,
	# to define the sensitivity in software and not rely solely on the
	# sensor itself.
	#	
	# You can remove this version once the sensitivity is reliable:

	t_end = time.time() + time_loop
	while time.time() < t_end:
	
	# This version simply loops for eternity unless ctrl-c is pressed
	# or the threshold value is exceeded
	# and should be your "production" version of the loop:
	
	# while per_detected < a_threshold:

	# Now we get to the actual loop and start detecting sound
		
		# Count the number of iterations - important for determining 
		# sustained detection versus flutter in the sensor
		loop_count = loop_count + 1
		
		# If sound is loud enough, the GPIO PIN will switch state to HIGH
		# record the occurance and add it to the count for computation
		if GPIO.input(input_digital) == GPIO.HIGH:
			Is_Loud = "Loudness Detected"
			Loud_Count = Loud_Count + 1

		
		# have we hit our threshold yet?		 
		per_detected = Decimal(Loud_Count) / Decimal(loop_count)
		print "Detect vs Threshold: " + str(per_detected) + " / " + str(a_threshold) 
		
		# Lets see if we have actually detected a sound that meets the
		# threshold? If so, we will turn on the red light and it will stay on
		# until the sound drops under the threshold again.
		if per_detected > a_threshold:
			GPIO.output(red_led, GPIO.HIGH)

		else:
			GPIO.output(red_led, GPIO.LOW)

except (KeyboardInterrupt, SystemExit):
	
	#If the system is interrupted (ctrl-c) this will print the final values
	#so that you have at least some idea of what happened
	print "-------------------------------------------"
	print " "
	print "System Reset on Keyboard Command or SysExit"
	print " "
	print "Final Detection was " + str(Is_Loud)
	print " "
	print "Total Noises Detected: " + str(Loud_Count)
	print " "
	print " "
	print "Total loops run: " + str(loop_count)
	print " "
	print "-------------------------------------------"
	GPIO.cleanup()

else:
	
	GPIO.cleanup()

        # You can remove this entire block once you go to "production" mode
	# but these values are critical for the initial tuning phase.
        print "-------------------------------------------"
        print " "
        print "System Reset on Keyboard Command or SysExit"
        print " "
        print "Final Detection was " + str(Is_Loud)
        print " "
        print "Total Noises Detected: " + str(Loud_Count)
        print " "
        print " "
        print "Total loops run: " + str(loop_count)
        print " "
        print "-------------------------------------------"
