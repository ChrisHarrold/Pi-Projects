import time
import datadog
#Setup API call key
options = {
    'api_key':'9829798b06436a2388037168ef6fe801',
    'app_key':'4ac5e95f906e705fe44f1abf74522a9fc7497501'
}
datadog.initialize(**options)

# Intitalize log values - if you get "init" as a value in your logs, this can also help troubleshoot later
title = "INIT"
text = "INIT"
tags = "[startup:INIT]"

#other variables
i = 0


# Log to an event function - additional logging can occur in the same function call (like local file or DB as well)
def logevent(title, text, tags):
	datadog.api.Event.create(title=title, text=text, tags=tags)



try:
	print("Starting up")
	logevent('ProgramStart', 'Program is starting up', '[deviceID:1234, sev:INFO, something:interesting]')
	while True:
		#Normally this would do something here, but in the interest of time - it actually doesn't do anything...
		#now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		print("Motion detected!")
		logevent('MOTION', 'Motion Sensor triggered', '[deviceID:1234, sev:WARN, do:something]')
		
		time.sleep(5000)
		i = i + 1

except KeyboardInterrupt:
	print("")
	print("Stopped by User")
	logevent('ProgramStopped', 'Program terminated', '[deviceID:1234, sev:INFO, something:interesting]')