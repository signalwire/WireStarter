#!/usr/bin/env python3
import json
import re
import sys,os
from functions import *


if len(sys.argv) >= 2:
  new_ngrok_url = str(sys.argv[1])
else:
  sys.exit("ERROR: There is no incoming NGROK url.  Please provide a URL and try again")

def get_phone_numbers():
    response, status_code = phone_number_func()
    response_json = json.loads(response)
    return response_json

def post_phone_numbers(response_json):
    # Find and Update each number that is assigned to a url
    signalwire_space, project_id, rest_api_token = get_environment()

    for number in response_json['data']:
      number_uuid = str(number['id'])
      phone_number = str(number['number'])
      call_url = str(number['call_request_url'])
      message_url = str(number['message_request_url'])

      call_match = re.search(r'ngrok.io', call_url)
      message_match = re.search(r'ngrok.io', message_url)
      old_call_ngrok_url = str(call_url[0:36])
      old_message_ngrok_url = str(message_url[0:36])

      new_call_url = ""
      new_message_url = ""

      if call_match:
          new_call_url = call_url.replace(old_call_ngrok_url,new_ngrok_url)
      else:
          # Nothing changed, keep things the same
          new_call_url = call_url

      if message_match:
          new_message_url = message_url.replace(old_message_ngrok_url,new_ngrok_url)
      else:
          # Nothing changed, keep things the same
          new_message_url = message_url

      payload = json.dumps({
          "call_request_url": new_call_url,
          "message_request_url": new_message_url,
      })

      query_params = "/" + number_uuid

      output, status_code = phone_number_func(query_params=query_params, req_type="PUT", payload=payload)
      valid = validate_http(status_code)
      if valid:
          output_data = json.loads(output)
          # Print statements commented out below.
          # Since this script runs automatically at start, keeping it quiet. We can remove the comments if needed/wanted
          # print (output_data)
          # print (phone_number + ' has had its webhooks changed successfully')
      else:
          is_json = validate_json(output)
          if is_json:
              print_error_json(output)
          else:
              print ("Error: " + output + "\n")

def update_phone_number_urls():
    response_json = get_phone_numbers()
    post_phone_numbers(response_json)
    


update_phone_number_urls()
