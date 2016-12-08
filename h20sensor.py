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
sensor_pin = 7
loops = 0

# Setup GPIO commands and power pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(power_pin, GPIO.OUT)

# Make sure the power starts as off
GPIO.output(power_pin, GPIO.LOW)

# Opens and preps the data file for the first time. Will remove anything it
# finds in the file and prep it with this default. :
data_file = "/data/h20lvl.csv"
with open(data_file + '.new', 'a') as f_output:



# So the act of getting the moisture level is pretty simple, but there are some technical
# reasons that are explained in the blog video about this project (linkedin.com/chrisharrold)
# that means that it makes sense to check the water level as infrequently as possible.
#
# The main monitoring loop will simply power on the sensor, read the voltage, and record 
# it to the data file. From there it 
# can be used for comparison to observed plant performance over time to gauge the right 
# level for the water for that plant. I plan to expand this in the future with temperature
# and light sensing data so that the watering schedule can be established for the plants 
# based on the environmentals as well as observed performance.

# Main try block to handle the exception conditions
try:	

    # Primary monitor is a "while" loop that will keep the monitor running 
	# indefinitely as a soft service.
	
	while True:
		print('Preparing to monitor soil moisture level')
		
		# turn on the soil monitor sensor - done to avoid premature burnout due to
		# electrolysis corrosion
		GPIO.output(power_pin, GPIO.HIGH)
		
		# Read the voltage from the sensor via the ADC chip
		voltage_lvl = mcp.read_adc(sensor_pin)
		
		# Get the timestamp for the log entry
		localtime = time.asctime( time.localtime(time.time()) )
		
		# Write out to the log file
		f_output.write("" + localtime + "," + str(voltage_lvl) + "")
		
		# Print to the stdout for debug
		print"" + localtime + "," + str(voltage_lvl) + ""
		
		# Increment the loop counter
		loops = loops + 1
		
		# Turn the sensor off
		GPIO.output(power_pin, GPIO.LOW)
		
		# settle in and sleep until the next time to poll the sensor
		time.sleep(14400)
			

except (KeyboardInterrupt, SystemExit):
	
	f_output.close()
	GPIO.cleanup()
	
	# You can remove this entire block once you go to "production" mode
	# but these values are useful for the initial tuning phase.
    print "-------------------------------------------"
    print " "
    print "System Reset on Keyboard Command or SysExit"
    print " "
    print "-------------------------------------------"

else:
	
	f_output.close()
	GPIO.cleanup()
