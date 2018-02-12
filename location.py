# Uses the free API key from Here (here.com) and a list of WLAN MAC addresses to 
# retreive a location in lattitude and longitude and an accuracy score. Accuracy
# is the radius of "uncertainty circle" (that blue ring around your dot on a phone map) 
# from location in meters.


# we will need these two libraries for handling the API request, and parsing the resultant JSON
import requests
import json
# this one is for getting the wifi mac addresses
#from wifi import Cell, Scheme
#thedata = str(Cell.all('wlan0'))
#print(thedata)
    

# Define the things we need for our API call - this is unique to each API
data = ""
url = 'https://pos.cit.api.here.com/positioning/v1/locate?app_id={GET A KEY AT HERE.COM}&app_code={GET A CODE AT HERE.COM}'
headers = {'Content-type': 'application/json'}

# grab our list of wifi networks and split them into the JSON data format

# will add r-pi python for collecting and stripping MAC addresses to a file here

# first open the JSON format
theString = """{
 "wlan": ["""

# Now read in the list of MAC address values
with open("list.csv") as f: # list.csv is a list of mac addresses, 1 per line
    lines = f.readlines()
    last = lines[-1]
    for line in lines:
        line = line.rstrip("\n")
        if line is last:
            #print id(line),id(last)
            a = line
            stra = '"mac": "{}"'.format(a)
            theString = theString + """   {""" + stra + """}"""
        else:
            a = line
            stra = '"mac": "{}"'.format(a)
            theString = theString + """   {""" + stra + """},"""

# lastly close the JSON
theString = theString + """]
}"""

# This last replace makes sure there are no linefeeds in our string (took a while to 
# troubleshoot that one!)
theString = theString.replace("\n", "")

# Now we make our API call:
response = requests.post(url, data=theString, headers=headers)
# And load the returned JSON into a dict object:
jData = json.loads(response.content)

# I can quickly check if I goofed up by looking for a 404 error (I can expand this to include
# all 400 and 500 series errors and even respond with the error)
if '404' in str(jData):
    # got an error so print the full payload returned from the API for troubleshooting
    print("you messed up the json, or it got a bad result:")
    print(jData)
else:
    # Didn't get an error! Print out the returned values:
    print(jData)
    # and then as a nice touch - format them into something more human readable:
    for key in jData:
        print ("Latitude = " + str(jData['location']['lat']))
        print ("Longitude = " + str(jData['location']['lng']))
        print ("Accuracy = " + str(jData['location']['accuracy']))

# from here, it is most likely that you would want to assign at a minimum the accuracy, but likely
# also the lat and lng data to a variable for further processing - something like 
# "thelat = str(jData['location']['lat'])"  as an example (you may want them to be int values though
# if you intend to do any maths against them)

