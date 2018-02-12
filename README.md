# Pi-Projects
Code related to My IoT projects and blog series - Comments in code guide you

Current Files:

led.py - python for blinking an LED with Raspberry pi

led2.py - same as above but with two lights

sound.py - sound sensor detector code - debug version, non-service

sound_svc.py - runs the sound detection as a service in fully auto loop mode

location.py - using the Here (here.com) service API and a list of MAC addresses to return a location in lat/lng

level.html - google guage HTML page for displaying the output of the sound detector project (copy to /var/www/html on your Pi)

simpletest.py - a simple analog to digital reader test script for the MCP3008 ADC chip

h20sensor.py - code for monitoring soil moisture levels using the elego analog soil moisture sensor and MCP3008 ADC

dht11.py - python library for reading the ourput from the DHT11 temp and humidity sensor - used by the H20 sensor code

dht11test.py - a quick simple script to verify you are able to get data from the DHT11 sensor - check the code comments in the H20 sensor code for the why

I have extensively commented the code such that you can figure out what each one does by reading the comments.
The file list here just tells you what each one does, not the how.
