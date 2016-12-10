#import all the usual suspects - GPIO, time, math just in case and the MCP3008 interface code
import RPi.GPIO as GPIO
import dht11
import time
import datetime
from decimal import *
import math
getcontext().prec = 4
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

#I have chosen to use the hardware configuration for this project so this is here in case you choose
#to go the software-based route:

#CLK  = 18
#MISO = 23
#MOSI = 24
#CS   = 25
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#These lines are for the hardware SPI config: 
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# The DHT11 Temp/humidity sensor apparently isn't great so retrying the reading can be required
# this variable says how many times to try and get the reading
retries = 5
# This is the pin that will turn on the soil moisture probe (SMP)
power_pin = 18
#This is the pin on the MCP3008 that will get the analog reading from the SMP
h20_pin = 7
# This is the pin on the MCP3008 that will get the light level reading
light_pin = 0
# This is the pin on the RPi GPIO that will get the reading from the DHT11 module
temp_pin = 4
#This is the overall loop counter variable - really just a debug tool
loops = 0

# Setup GPIO commands and enable the power pin, and DHT11 pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(power_pin, GPIO.OUT)
GPIO.setup(temp_pin, GPIO.IN)

# Make sure the power starts as off
GPIO.output(power_pin, GPIO.LOW)

# Opens and preps the data file for the first time. Will remove anything it
# finds in the file and prep it with this default. :
data_file = "/data/h20lvl.csv"
with open(data_file + '.new', 'a') as f_output:
	f_output.write("timestamp,h20_value,temp-C,humidity\n")

# So the act of getting the moisture level is pretty simple, but there are some technical
# reasons that are explained in the blog video about this project (linkedin.com/chrisharrold)
# that means that it makes sense to check the water level as infrequently as possible. This
# will then turn on the sensor pack and then run the collect
# code if the light level is bright enough to be considered "daytime" 

# Primary monitor is a "while" loop that will keep the monitor running 
# indefinitely as a soft service.
print('Preparing to monitor soil moisture level')
try:

	while True:
		
		# turn on the sensor pack - done to avoid premature burnout due to
		# electrolysis corrosion
		GPIO.output(power_pin, GPIO.HIGH)
		
		# I noticed that trying to read the voltage right after turning on the juice created
		# really variable readings that were obviously caused by the "bounce" of the power
		# coming on to the sensors, so I have it turn on and wait so that it can normalize
		time.sleep(10)
		
		# We need to check if it is dark out. The rationale is that overnight the evaporation
		# rate is slowed due to the cooler temp so it is not as important to check the level
		# which also means that we spare the sensor from additional electrolysis effect
		light_lvl = mcp.read_adc(light_pin)
		print "" + str(light_lvl) + ""
		
		# The voltage from the light sensor is lower the more light that hits the sensor
		# the lower the voltage read will be. Around 800 seems to be the sweet spot for
		# dark enough to be considered "night".
		if (light_lvl < 800):
		
			print "Sun's out! Checking H20 Level:"
			# Gave up on the thermistor because none of the math I found worked after 3 days
			# and because the DHT11 returns humidity and temp natively with no BS formulas
			# so I am using that now.


			# read data using pin 14
			instance = dht11.DHT11(pin=temp_pin)
			
			reading = 0
			while reading == 0:
				result = instance.read()
   				if result.is_valid():
        			print("Temperature: %d C" % result.temperature)
        			temp = result.temperature
        			print("Humidity: %d %%" % result.humidity)
        			humid = result.humidity
        			reading = 1
        		else:
        			reading = 0
			
			# Get the timestamp for the log entry
			localtime = time.asctime( time.localtime(time.time()) )
		
			# Write out to the log file
			with open(data_file + '.new', 'a') as f_output:
				f_output.write("" + localtime + "," + str(voltage_lvl) + "," + str(temp) + "," + str(humid) + "\n")
		
			# Print to the stdout for debug
			print "On " + localtime + " The H20 Level is: " + str(voltage_lvl) + ", the temp is: " + str(temp) + ", and the Humidity is " + str(humid) + "%%"
		
			# Increment the loop counter
			loops = loops + 1
		
		# Turn the sensor off
		GPIO.output(power_pin, GPIO.LOW)
		
		# settle in and sleep until the next time to poll the sensor
		print "sleeping for 1 seconds"
		time.sleep(1)
			

except (KeyboardInterrupt, SystemExit):
	
	# If the system is interrupted (ctrl-c) this will print the final values
	# so that you have at least some idea of what happened
	print "-------------------------------------------"
	print " "
	print "System Reset on Keyboard Command or SysExit"
	print " "
	print "-------------------------------------------"
	GPIO.cleanup()
	
else:
	
	GPIO.cleanup()
