#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from functions import *

### SET ENVIRONMENT ###

load_dotenv()

signalwire_space = os.getenv('SIGNALWIRE_SPACE')
project_id = os.getenv('PROJECT_ID')
rest_api_token = os.getenv('REST_API_TOKEN')

#######################

def get_phone_numbers():
    response = http_request(signalwire_space, project_id, rest_api_token, "phone_numbers", "GET")
    print(response.text)

get_phone_numbers()

