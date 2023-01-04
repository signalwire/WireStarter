#!/usr/bin/env python3
import base64
import requests
import os,sys
import json
from pygments import highlight, lexers, formatters
####

env_var_dict = {}

########################################
########### SPACE  FUNCTIONS ###########
########################################
def project_func( query_params="", req_type="GET", headers={}, payload={} ):
    # Uses compatibility API
    signalwire_space, project_id, rest_api_token = get_environment()
    destination = "Accounts" + query_params
    if req_type == "POST":
        http_basic_auth = str(encode_auth(project_id, rest_api_token))
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
          'Authorization': 'Basic %s' % http_basic_auth
        }
    url = "https://%s.signalwire.com/api/laml/2010-04-01/" % signalwire_space
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload, url=url )
    return (response.text, response.status_code)

########################################
######## PHONE NUMBER FUNCTIONS ########
########################################
def phone_number_func( query_params="", req_type="GET", headers={}, payload={} ):
    signalwire_space, project_id, rest_api_token =  get_environment()
    destination = "phone_numbers" + query_params
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload )
    return (response.text, response.status_code)

def phone_number_lookup(query_params):
    signalwire_space, project_id, rest_api_token =  get_environment()
    destination = "lookup/phone_number/" + query_params
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "GET")
    json_response = json.loads(response.text)
    json_formatted_response = json.dumps(json_response, indent=2)
    print (json_formatted_response)

########################################
######## SIP ENDPOINT FUNCTIONS ########
########################################
def sip_endpoint_func( query_params="", req_type="GET", headers={}, payload={} ):
    signalwire_space, project_id, rest_api_token =  get_environment()
    destination = "endpoints/sip" + query_params
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload )
    return (response.text, response.status_code)

########################################
############ SIP PROFILE ###############
########################################
def sip_profile_func( query_params="", req_type="GET", headers={}, payload={} ):
    signalwire_space, project_id, rest_api_token =  get_environment()
    destination = "sip_profile" + query_params
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload )
    return (response.text, response.status_code)

########################################
############# LAML BINS ################
########################################
def laml_bin_func( query_params="", req_type="GET", headers={}, payload = {} ):
    # Uses the Compatibility API
    signalwire_space, project_id, rest_api_token =  get_environment()
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
    return (response.text, response.status_code)

########################################
############# LAML APPS ################
########################################
def laml_app_func( query_params="", req_type="GET", headers={}, payload = {} ):
    # Uses the Compatibility API
    signalwire_space, project_id, rest_api_token =  get_environment()
    destination = "Accounts/" + project_id + "/Applications" + query_params
    url = "https://%s.signalwire.com/api/laml/2010-04-01/" % signalwire_space
    if req_type == "POST":
        http_basic_auth = str(encode_auth(project_id, rest_api_token))
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
          'Authorization': 'Basic %s' % http_basic_auth
        }
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload, url=url )
    return (response.text, response.status_code)

########################################
########### NUMBER GROUPS ##############
########################################
def number_group_func( query_params = "", req_type="GET", headers={}, payload={} ):
    signalwire_space, project_id, rest_api_token =  get_environment()
    destination = "number_groups" + query_params
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload )
    return (response.text, response.status_code)

########################################
######### DOMAIN APPLICATIONS ##########
########################################
def domain_application_func( query_params = "", req_type="GET", headers={}, payload={} ):
    signalwire_space, project_id, rest_api_token =  get_environment()
    destination = "domain_applications" + query_params
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload )
    return (response.text, response.status_code)

########################################
############# FIFO QUEUES ##############
########################################
def fifo_queue_func( query_params="", req_type="GET", headers={}, payload={} ):
    # Uses compatibility API
    signalwire_space, project_id, rest_api_token = get_environment()
    destination = "Accounts/" + project_id + query_params
    if req_type == "POST":
        http_basic_auth = str(encode_auth(project_id, rest_api_token))
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
          'Authorization': 'Basic %s' % http_basic_auth
        }
    url = "https://%s.signalwire.com/api/laml/2010-04-01/" % signalwire_space
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload, url=url )
    return (response.text, response.status_code)

########################################
############### FAXES  #################
########################################
def fax_func( query_params="", req_type="GET", headers={}, payload={} ):
    # Uses compatibility API
    signalwire_space, project_id, rest_api_token = get_environment()
    destination = "Accounts/" + project_id + query_params
    if req_type == "POST":
        http_basic_auth = str(encode_auth(project_id, rest_api_token))
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
          'Authorization': 'Basic %s' % http_basic_auth
        }
    url = "https://%s.signalwire.com/api/laml/2010-04-01/" % signalwire_space
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload, url=url )
    return (response.text, response.status_code)

########################################
############## SEND A CALL #############
########################################
def call_func( query_params = "", req_type="GET", headers={}, payload={} ):
    # Uses compatibility API
    signalwire_space, project_id, rest_api_token = get_environment()
    destination = "Accounts/" + project_id + "/Calls" + query_params
    url = "https://%s.signalwire.com/api/laml/2010-04-01/" % signalwire_space
    if req_type == "POST":
        http_basic_auth = str(encode_auth(project_id, rest_api_token))
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Accept': 'application/json',
          'Authorization': 'Basic %s' % http_basic_auth
        }
    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, headers=headers, payload=payload, url=url )
    return (response.text, response.status_code)

########################################
def get_environment():
    signalwire_space = os.getenv('SIGNALWIRE_SPACE')
    project_id = os.getenv('PROJECT_ID')
    rest_api_token = os.getenv('REST_API_TOKEN')
    return (signalwire_space, project_id, rest_api_token)

def validate_signalwire_creds(signalwire_space, project_id, rest_api_token):
    req_type = "GET"
    destination = "Accounts"
    url = "https://%s.signalwire.com/api/laml/2010-04-01/" % signalwire_space

    response = http_request( signalwire_space, project_id, rest_api_token, destination, req_type, url=url )
    if response.status_code == 200:
        # The creds are legit
        return True
    else:
        return False

def set_shell_env(var):
    global env_var_dict
    env_var_split = var.split("=")
    key = env_var_split[0]
    val = env_var_split[1]
    
    env_var_dict[key] = val

def get_shell_env(var):
    key = var
    if key:
        val = env_var_dict[key]
        if val:
            return (env_var_dict[key])
        else:
            print ("")
    else:
        print("")

def get_shell_env_all():
    if len(env_var_dict.items()) == 0:
        return
    else:
        for k, v in env_var_dict.items():
            print(k + "=" + v)
        print("")

def json_nice_print(j):
    if len(j) == 0:
        print("No Results Found!")
    else:
        json_formatted_response = json.dumps(j, indent=4)
        #print(json_formatted_response)
        colorful_json = highlight(json_formatted_response, lexers.JsonLexer(), formatters.SwishFormatter())
        print (colorful_json)

def encode_auth(project_id, rest_api_token):
    auth = str(project_id + ":" + rest_api_token)
    auth_bytes = auth.encode('ascii')
    base64_auth_bytes = base64.b64encode(auth_bytes)
    base64_auth = base64_auth_bytes.decode('ascii')

    return base64_auth

def validate_http(status_code):
    # Validate an API response, and determine if it is an error
    # Keeping track of 2XX codes I've seen.  Maybe these need to be passed w/ specific calls for validation.
    # For now, if 2XX, then Pass.
    # Seen: 200, 201, 204
    if status_code == 200 or status_code == 201 or status_code == 204:
        return True
    else:
        return False

def validate_json(output):
    # Validate whether or not a string is valid JSON
    try:
        json.loads(output)
        return True
    except ValueError:
        return False

def print_error_json(error_json):
    # Just printing the error code and detail of the error.
    # Down the road, it may make sense to print the entire JSON, but most users probably just want the text
    error_json = json.loads(error_json)
    detail = str(error_json["errors"][0]["detail"])
    code = str(error_json["errors"][0]["code"])

    print ("API ERROR -- " + code + ": " + detail + "\n")

def print_error_json_compatibility(error_json):
    # Print a JSON Error that came from the compatibility API
    # Just printing the error code and detail of the error.
    # Down the road, it may make sense to print the entire JSON, but most users probably just want the text
    # EXAMPLE: {'code': 20404, 'message': 'The requested resource was not found.', 'more_info': 'https://developer.signalwire.com/compatibility-api/reference/error-codes', 'status': 404}
    error_json = json.loads(error_json)
    message = str(error_json["message"])
    status = str(error_json["status"])

    print ("API ERROR -- " + status + ": " + message + "\n")

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
    #print (headers)
    response = requests.request(req_type, fqdn, headers=headers, data=payload)
    return (response)