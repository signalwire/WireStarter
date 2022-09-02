#!/usr/bin/env python3
import requests
import os
from dotenv import load_dotenv
from functions import *

### SET ENVIRONMENT ###

load_dotenv()

signalwire_space = os.getenv('SIGNALWIRE_SPACE')
project_id = os.getenv('PROJECT_ID')
rest_api_token = os.getenv('REST_API_TOKEN')

#######################

def get_sip_endpoints():
    response = http_request(signalwire_space, project_id, rest_api_token, "/endpoints/sip", "GET")
    print(response.text)

get_sip_endpoints()
