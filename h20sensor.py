#import all the usual suspects - GPIO, time, math just in case and the MCP3008 interface code
import RPi.GPIO as GPIO
import time
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

power_pin = 18
h20_pin = 7
light_pin = 0
temp_pin = 3
loops = 0

# Setup GPIO commands, cleanup just in case, and enable the power pin
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(power_pin, GPIO.OUT)

# Make sure the power starts as off
GPIO.output(power_pin, GPIO.LOW)

# Opens and preps the data file for the first time. Will remove anything it
# finds in the file and prep it with this default. :
data_file = "/data/h20lvl.csv"
with open(data_file + '.new', 'a') as f_output:
	f_output.write("timestamp,h20_value,temp_value\n")



# So the act of getting the moisture level is pretty simple, but there are some technical
# reasons that are explained in the blog video about this project (linkedin.com/chrisharrold)
# that means that it makes sense to check the water level as infrequently as possible. This
# will then turn on the entire sensor pack (temp, light, and water) and then run the collect
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
		time.sleep(5)
		
		# We need to check if it is dark out. The rationale is that overnight the evaporation
		# rate is slowed due to the cooler temp so it is not as important to check the level
		# which also means that we spare the sensor from additional electrolysis effect
		light_lvl = mcp.read_adc(light_pin)
		
		# The voltage from the light sensor is lower the more light that hits the sensor
		# the lower the voltage read will be. Around 800 seems to be the sweet spot for
		# dark enough to be considered "night".
		if light_lvl < 800:
		
			# Read the voltage from the H20 and temp sensor via the ADC chip
			voltage_lvl = mcp.read_adc(h20_pin)
			temp = mcp.read_adc(temp_pin)
			
			# Now we convert the voltage to a temperature
			temp = (temp * (5000/1024))
			temp = ((temp - 500) / 10)
			
			# Get the timestamp for the log entry
			localtime = time.asctime( time.localtime(time.time()) )
		
			# Write out to the log file
			with open(data_file + '.new', 'a') as f_output:
				f_output.write("" + localtime + "," + str(voltage_lvl) + "," + str(temp) + "\n")
		
			# Print to the stdout for debug
			print "Date and time: " + localtime + " H20 Level: " + str(voltage_lvl) + " Temp: " + str(temp) + ""
		
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
