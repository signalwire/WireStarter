#!/usr/bin/env python3
from functions import *
import json
import os,sys
from dotenv import load_dotenv


### SET ENVIRONMENT ###
load_dotenv()

signalwire_space = os.getenv('SIGNALWIRE_SPACE')
project_id = os.getenv('PROJECT_ID')
rest_api_token = os.getenv('REST_API_TOKEN')
#######################

selection = input ( "How would you like to filter\n 1) Begins With\n 2) Contains\n 3) Ends With\n 4) No Filter\n\nPlease make a selection: " )

if selection == "1":
    filter = "starts_with"
    value = input( "Number begins with: " )
elif selection == "2":
    filter = "contains"
    value = input ( "Number Contains: " )
elif selection == "3":
    filter = "ends_with"
    value = input ( "Number ends With: " )
else:
    print ( "ERROR: That is not a valid selection" )
    quit()

destination = "phone_numbers/search?max_results=10&{f}={v}".format(f=filter, v=value)

response = http_request( signalwire_space, project_id, rest_api_token, destination, "GET" )
jsonify_data = json.loads(response.text)
tn_data = jsonify_data["data"]
#print (jsonify_data)

for index, value in enumerate(tn_data):
    # Create a temporary dictionary for each number
    temp_d = value
    index_val = str(index + 1)           # Change the indexes into something human readable.  AKA start at 1 not 0.

    print (index_val + ")")
    print ("  Number:\t" + temp_d["e164"])
    print ("  US Formatted:\t" + temp_d["national_number_formatted"])
    print ("  Rate Center:\t" + temp_d["rate_center"])
    print ("  Region:\t" + temp_d["region"])
    print ("  Country Code:\t" + temp_d["country_code"])
    print ("")

# TODO: Do better validation on this to have a graceful error message if not an INT
tn_selection_val = int(input ("Which number would you like to buy? " ))
tn_selection_index = int(tn_selection_val - 1)  # Decriment the index back by 1 to account for the list starting at 0
tn_selected = tn_data[tn_selection_index]["e164"]

confirm = input ("\nPlease confirm the purchase of " + tn_selected + ".  This will charge your account (Y/n): ")
if confirm.lower() == "y" or confirm.lower == "yes":
    #payload = '{"number": "%s"}' % tn_selected
    payload = '{"number": "%s" }' % tn_selected
    print (payload)
    destination = "phone_numbers"
    http_basic_auth = str(encode_auth(project_id, rest_api_token))
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Basic %s' % http_basic_auth
    }

    response = http_request(signalwire_space, project_id, rest_api_token, destination, "POST", payload=payload, headers=headers)
    # TODO: validate a legit response here.
    response_json = json.loads(response.text)
    sid = (response_json["id"])
    print ("Congratulations!  You have just added " + tn_selected + " to your SignalWire project!")
    print ("The SignalWire ID of that number is " + sid + ".  Use it to start building cool stuff!")
else:
    print ("Cancelling!\n")