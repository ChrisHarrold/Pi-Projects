# Uses the free API key from Here (here.com) and a list of WLAN MAC addresses to 
# retreive a location in lattitude and longitude and an accuracy score. Accuracy
# is the radius of "uncertainty circle" (that blue ring around your dot on a phone map) 
# from location in meters.


# we will need these two libraries for handling the API request, and parsing the resultant JSON
import requests
import json
# this one is for getting the wifi mac addresses
from subprocess import PIPE, Popen
import re

# counters and variables just for completness:
thecount = 0
theString = ""

# grab our list of wifi networks and split them into the JSON data format
# Scan using wlan0 and the new python.process for running shell commands:
def cmdline(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0]

# These two commands get the list of networks and put them in a decoded UTF-8 string:
sLANs = cmdline('wpa_cli -i wlan0 scan_results')
sLANs = sLANs.decode('utf-8')
# you can see the raw string below if you remove the comment it is formatted with \t and \n
# if you decide to change it to do other things, make sure you use a strip or replace:
#print(sLANs)

# Now take that string, and pull out just the MAC addresses - this took me many days to find
# and figure out. Special thanks to the French guy from Thalys on StackOverflow. Not for the answer, 
# but because he was a douche (that's French for asshat), he pushed me to find the answer on my own.
p = re.compile(r'(?:[0-9a-fA-F]:?){12}')
test_str = sLANs
sLANs = re.findall(p, test_str)
# Another debug print if you need it (should be a list of MAC addrs with a "," between:
#print (sLANs)

# Now we need to prep this for sending to the API.
# first let's get this into the JSON format so we can send it:
theString = """{
 "wlan": ["""

# Now we insert the MAC values into the string in the expected format
# This will iterate the list that came back from the command above, and format it per the JSON
# that the API requires:
for macs in sLANs:
    last = len(sLANs)
    thecount = thecount + 1
    # If this is the last entry in the list of MAC addresses we need to change the format of the JSON a bit
    #print (repr(macs))
    if thecount == last:
        macs = macs.lstrip()
        macs = macs.rstrip()
        stra = '"mac": "{}"'.format(macs)
        theString = theString + """   {""" + stra + """}"""
    # All the internal lines have a "," between them except the very last one (handled above)
    else:
        macs = macs.lstrip()
        macs = macs.rstrip()
        stra = '"mac": "{}"'.format(macs)
        theString = theString + """   {""" + stra + """},"""


# last thing is to close the JSON so it is properly formatted
theString = theString + """]
}"""

# This last replace makes sure there are no linefeeds in our string (took a while to 
# troubleshoot that one!)
theString = theString.replace("\n", "")
#You can display the complete and debugged string below by removing the comment:
#print(theString)

# Now we make our API call:
# Define the things we need for our API call - this is unique to each API
data = ""
url = 'https://pos.cit.api.here.com/positioning/v1/locate?app_id=MmLlTteK7aj3zF6eA0Tn&app_code=6-zloMGtPyAgc12gkQVzrA'
headers = {'Content-type': 'application/json'}
# using the python response library, we make our request by sending the properly formatted JSON string,
# the URL, and the header info to the API
response = requests.post(url, data=theString, headers=headers)
# And load the returned JSON into a dict type object:
jData = json.loads(response.content.decode('utf-8'))
# the debug below is EXTREMELY useful for debigging the JSON returned by the API. If you get
# "key" errors when you try and do the print below, it is highly likely that the JSON string is borked
# and you are getting errors back from the API - this will tell you what it is:
#print(jData)

# Now before I print out the results, let's make sure I do not try and print bogus info!
# the word "decription" will be returned in the error code, but not in a good response
# by looking for that keyword in the JSON string I can determine if there is an error:
if 'description' in str(jData):
    # got an error so print the full payload returned from the API for troubleshooting
    print("you messed up the json, or it got a bad result, or the API is busted:")
    print(jData)
else:
    # Didn't get an error! removing the comment below prints the "raw" API return:
    #print(jData)
    # and then as a nice touch - this formats them into something more human readable:
    for key in jData:
        print ("Latitude = " + str(jData['location']['lat']))
        print ("Longitude = " + str(jData['location']['lng']))
        print ("Accuracy = " + str(jData['location']['accuracy']))

# from here, it is most likely that you would want to assign at a minimum the accuracy, but likely
# also the lat and lng data to a variable for further processing - something like 
# "thelat = str(jData['location']['lat'])"  as an example (you may want them to be int values though
# if you intend to do any maths against them)

