# Uses the free API key from Here (here.com) and a list of WLAN MAC addresses to 
# retreive a location in lattitude and longitude and an accuracy score. Accuracy
# is the radius of "uncertainty circle" (that blue ring around your dot on a phone map) 
# from location in meters.


# we will need these two libraries for handling the API request, and parsing the resultant JSON
import requests
import json

# Define the things we need for our API call - this is unique to each API
data = ""
url = 'http://192.168.80.248:9080'
headers = {'Content-type': 'application/xml'}

#include 192.168.7.208:9080/library/whatever.xx


response = requests.post(url, data="Hello!", headers=headers)
# And load the returned JSON into a dict object:


# I can quickly check if I goofed up by looking for a 404 error (I can expand this to include
# all 400 and 500 series errors and even respond with the error)
if '404' in str(response):
    # got an error so print the full payload returned from the API for troubleshooting
    print("you messed up the json, or it got a bad result:")
    print(response)
else:
    # Didn't get an error! Print out the returned values:
    print(response)
    # and then as a nice touch - format them into something more human readable:


# from here, it is most likely that you would want to assign at a minimum the accuracy, but likely
# also the lat and lng data to a variable for further processing - something like 
# "thelat = str(jData['location']['lat'])"  as an example (you may want them to be int values though
# if you intend to do any maths against them)

