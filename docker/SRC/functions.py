#!/usr/bin/env python3
import base64
import requests
import os,sys
from dotenv import load_dotenv
import json
####

### SET ENVIRONMENT ###
load_dotenv()

signalwire_space = os.getenv('SIGNALWIRE_SPACE')
project_id = os.getenv('PROJECT_ID')
rest_api_token = os.getenv('REST_API_TOKEN')
#######################

########################################
######## PHONE NUMBER FUNCTIONS ########
########################################
def phone_number_func( query_params="", req_type="GET", headers={}, payload={} ):
    destination = "phone_numbers" + query_params
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload )
    return (response.text)

def phone_number_lookup(query_params):
    destination = "lookup/phone_number/" + query_params
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "GET")
    json_response = json.loads(response.text)
    json_formatted_response = json.dumps(json_response, indent=2)
    print (json_formatted_response)
########################################


########################################
######## SIP ENDPOINT FUNCTIONS ########
########################################
def sip_endpoint_func( query_params="", req_type="GET", headers={}, payload={} ):
    destination = "endpoints/sip" + query_params
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload )
    return (response.text)
########################################


########################################
############ SIP PROFILE ###############
########################################
def sip_profile_func( query_params="", req_type="GET", headers={}, payload={} ):
    destination = "sip_profile" + query_params
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload )
    return (response.text)
########################################


########################################
############# LAML BINS ################
########################################
def laml_bin_func( query_params="", req_type="GET", headers={}, payload = {} ):
    # Uses the Compatibility API
    destination = "Accounts/" + project_id + "/LamlBins" + query_params
    url = "https://%s.signalwire.com/api/laml/2010-04-01/" % signalwire_space
    if req_type == "POST":
        http_basic_auth = str(encode_auth(project_id, rest_api_token))
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
          'Authorization': 'Basic %s' % http_basic_auth
        }
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload, url=url )
    return (response.text)
########################################


########################################
########### NUMBER GROUPS ##############
########################################
def number_group_func( query_params = "", req_type="GET", headers={}, payload={} ):
    destination = "number_groups" + query_params
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload )
    return (response.text)
########################################




###################################################
def json_nice_print(j):
    if len(j) == 0:
        print("No Results Found!")
    else:
        json_formatted_response = json.dumps(j, indent=2)
        print(json_formatted_response)

def encode_auth(project_id, rest_api_token):
    auth = str(project_id + ":" + rest_api_token)
    auth_bytes = auth.encode('ascii')
    base64_auth_bytes = base64.b64encode(auth_bytes)
    base64_auth = base64_auth_bytes.decode('ascii')

    return base64_auth

def http_request(signalwire_space, project_id, rest_api_token, destination, req_type, payload={}, headers={}, url="", query_params=""):
    http_basic_auth = str(encode_auth(project_id, rest_api_token))

    # if url is blank, then use this as a default
    # this may change in the future if there are many different urls at play.
    # adding this for api/relay/rest vs api/laml/2010-04-01.
    # This makes api/relay/rest the default
    if len(url) == 0:
        url = 'https://%s.signalwire.com/api/relay/rest/' % signalwire_space

    if headers == {}:
        if req_type == "GET":
          headers = {
            'Accept': 'applications/json',
            'Authorization': 'Basic %s' % http_basic_auth
          }
        elif req_type == "POST" or req_type == "PUT" or req_type == "DELETE":
          headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Basic %s' % http_basic_auth
          }
        else:
          print ("Something bad has happened.  That is not a valid HTTP request type!")
          quit()

    fqdn = str(url + destination + query_params)
    ## UNCOMMENT FOR DEBUG PURPOSES
    #print ("DEBUG req_type: " + req_type)
    #print ("DEBUG fqdn: " + fqdn)
    #print ("DEBUG payload: " + payload)
    #print ("DEBUG headers: " + headers)
    response = requests.request(req_type, fqdn, headers=headers, data=payload)
    return (response)
