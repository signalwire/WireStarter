#!/usr/bin/env python3
import os,sys
from dotenv import load_dotenv
from functions import *
import argparse

### SET ENVIRONMENT ###

load_dotenv()

signalwire_space = os.getenv('SIGNALWIRE_SPACE')
project_id = os.getenv('PROJECT_ID')
rest_api_token = os.getenv('REST_API_TOKEN')

#######################

#print (len(sys.argv))

# Look for arguments
parser = argparse.ArgumentParser()
parser.add_argument('--friendly-name', type=str, required=False)
args = parser.parse_args()

if args.friendly_name:
  friendly_name = args.friendly_name
  query_params = "?FriendlyName=%s" % friendly_name
else:
  query_params = ""

def list_space_accounts():
    destination = "Accounts" + query_params
    url = "https://%s.signalwire.com/api/laml/2010-04-01/" % signalwire_space
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "GET", url=url)
    print(response.text)

list_space_accounts()

