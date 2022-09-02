#!/usr/bin/env python3
import json
import re
import sys,os
from dotenv import load_dotenv
from functions import *


### SET ENVIRONMENT ###

load_dotenv()

signalwire_space = os.getenv('SIGNALWIRE_SPACE')
project_id = os.getenv('PROJECT_ID')
rest_api_token = os.getenv('REST_API_TOKEN')

#######################

if len(sys.argv) >= 2:
  new_ngrok_url = str(sys.argv[1])
else:
  sys.exit("ERROR: There is no incoming NGROK url.  Please provide a URL and try again")

def get_phone_numbers():
    payload={}
    response = http_request(signalwire_space, project_id, rest_api_token, "phone_numbers", "GET")
    response_json = json.loads(response.text)
    return response_json

def post_phone_numbers(response_json):
    # Find and Update each number that is assigned to a url
    for number in response_json['data']:
      number_uuid = str(number['id'])
      phone_number = str(number['number'])
      call_url = str(number['call_request_url'])
      message_url = str(number['message_request_url'])

      if call_url == "None" or message_url == "None" or call_url == "" or message_url == "":
        continue
      else:
        # example url: https://62bb-24-239-215-106.ngrok.io/cgi-bin/sms_1.py
        # TODO:  Need to break that into pieces and then replace

        call_match = re.search(r'ngrok.io', call_url)
        message_match = re.search(r'ngrok.io', message_url)
        old_call_ngrok_url = str(call_url[8:36])               # Only replace the random generated part.  Everything else should be kept, to keep file location consistent.
        old_message_ngrok_url = str(message_url[8:36])         # Only replace the random generated part.  Everything else should be kept, to keep file location consistent.
                                                           # Need to store the old values for both call and message separately, becasue they shouldn't be, but can be different.
        new_call_url = ""
        new_message_url = ""

        if call_match:
            new_call_url = call_url.replace(old_call_ngrok_url,new_ngrok_url)

        if message_match:
            new_message_url = message_url.replace(old_message_ngrok_url,new_ngrok_url)

        print (new_message_url)
        print (new_call_url)
        payload = json.dumps({
            "call_request_url": new_call_url,
            "message_request_url": new_message_url,
        })

        # TODO: just have this so that it adds to the default dictionary in the other script.
        # That should get rid of 5-6 lines of this redundant code.
        http_basic_auth = str(encode_auth(project_id, rest_api_token))
        headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Authorization': 'Basic %s' % http_basic_auth
        }

        destination = 'phone_numbers/%s' % number_uuid
        print (headers)
        response = http_request(signalwire_space, project_id, rest_api_token, destination, "PUT", payload=payload, headers=headers)
        print(response.text)

def update_phone_number_urls():
    response_json = get_phone_numbers()
    post_phone_numbers(response_json)






update_phone_number_urls()
