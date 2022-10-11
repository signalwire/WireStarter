#!/usr/bin/env python3
import cmd2
from dotenv import load_dotenv
import os
import argparse
from functions import *
import json
import time
## This is temporary ##
#from signalwire.voice_response import *
#from twilio.twiml.messaging_response import Message, MessagingResponse
from signalwire.rest import Client as signalwire_client


### SET ENVIRONMENT ###
load_dotenv()

signalwire_space = os.getenv('SIGNALWIRE_SPACE')
project_id = os.getenv('PROJECT_ID')
rest_api_token = os.getenv('REST_API_TOKEN')
#######################

## Local Functions ##
## TODO: make the json formatting a separate function to cut down on duplicate code.
## Format these so that they can be reused, rather than have one function for every single type of call
def list_space_projects(query_params):
    destination = "Accounts" + query_params
    url = "https://%s.signalwire.com/api/laml/2010-04-01/" % signalwire_space
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "GET", url=url)
    # format the response into nice JSON
    json_response = json.loads(response.text)
    json_formatted_response = json.dumps(json_response, indent=2)
    print(json_formatted_response)

def get_sip_endpoints():
    response = http_request(signalwire_space, project_id, rest_api_token, "/endpoints/sip", "GET")
    # format the response into JSON
    json_response = json.loads(response.text)
    json_formatted_response = json.dumps(json_response, indent=2)
    print (json_formatted_response)

def create_sip_endpoint(payload):
    http_basic_auth = str(encode_auth(project_id, rest_api_token))
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Basic %s' % http_basic_auth
    }
    response = http_request(signalwire_space, project_id, rest_api_token, "endpoints/sip", "POST", payload=payload, headers=headers)
    # TODO:  Need some legitimate checking here to make sure it was actually completed successfully
    print ("Complete")

def update_sip_endpoint(endpoint_sid, payload):
    destination = "endpoints/sip/" + endpoint_sid
    http_basic_auth = str(encode_auth(project_id, rest_api_token))
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Basic %s' % http_basic_auth
    }
    # TODO: Need some legitimate checking here to make sure it was actually completed successfully
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "PUT", payload=payload, headers=headers)

def delete_sip_endpoint(endpoint_sid):
    destination = "endpoints/sip/" + endpoint_sid
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "DELETE" )
    # TODO: Need some legitimate checking here to make sure the delete operation was successful
    print ("Complete")


## SIP PROFILES ##
def get_sip_profiles():
    response = http_request(signalwire_space, project_id, rest_api_token, "/sip_profile", "GET")
    # format the response into JSON
    json_response = json.loads(response.text)
    json_formatted_response = json.dumps(json_response, indent=2)
    print (json_formatted_response)

def update_sip_profiles(payload):
    http_basic_auth = str(encode_auth(project_id, rest_api_token))
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Basic %s' % http_basic_auth
    }
    # TODO: Need some legitimate checking here to make sure it was actually completed successfully
    response = http_request(signalwire_space, project_id, rest_api_token, "/sip_profile", "PUT", payload=payload, headers=headers)



##
def get_phone_numbers():
    response = http_request(signalwire_space, project_id, rest_api_token, "phone_numbers", "GET")
    # format the response into JSON
    json_response = json.loads(response.text)
    json_formatted_response = json.dumps(json_response, indent=2)
    print (json_formatted_response)

def get_phone_numbers_lookup(e164_number):
    destination = "phone_numbers/%s" % e164_number
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "GET")
    # format the response into JSON
    json_response = json.loads(response.text)
    json_formatted_response = json.dumps(json_response, indent=2)
    print (json_formatted_response)

def get_laml_bins(query_params):
    destination = "Accounts/" + project_id + query_params
    url = "https://%s.signalwire.com/api/laml/2010-04-01/" % signalwire_space
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "GET", url=url)
    # format the response into JSON
    json_response = json.loads(response.text)
    json_formatted_response = json.dumps(json_response, indent=2)
    print (json_formatted_response)


## DOMAIN APPLICATIONS ##
def list_domain_applications(query_params):
    destination = "domain_applications/" + query_params
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "GET")
    # format the response into JSON
    json_response = json.loads(response.text)
    json_formatted_response = json.dumps(json_response, indent=2)
    print (json_formatted_response)

def delete_domain_application(sid):
    destination = "domain_applications/" + sid
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "DELETE" )
    # TODO: Need some legitimate checking here to make sure the delete operation was successful
    print ("Complete")


## NUMBER GROUPS ##
def list_number_groups(query_params):
    destination = "number_groups" + query_params
    print (destination)
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "GET" )
    json_response = json.loads(response.text)
    json_formatted_response = json.dumps(json_response, indent=2)
    print (json_formatted_response)

def create_number_group(payload):
    http_basic_auth = str(encode_auth(project_id, rest_api_token))
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Basic %s' % http_basic_auth
    }
    # TODO: Need some legitimate checking here to make sure it was actually completed successfully
    response = http_request(signalwire_space, project_id, rest_api_token, "/number_groups", "POST", payload=payload, headers=headers)
    print(response.text)
    #print ('Complete')

def update_number_group(sid, payload):
    destination = "/number_groups/" + sid
    http_basic_auth = str(encode_auth(project_id, rest_api_token))
    headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': 'Basic %s' % http_basic_auth
    }
    # TODO: Need some legitimate checking here to make sure it was actually completed successfully
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "PUT", payload=payload, headers=headers)
    #print(response.text)
    print ('Complete')

def delete_number_group(sid):
    destination = "/number_groups/" + sid
    response = http_request(signalwire_space, project_id, rest_api_token, destination, "DELETE" )
    # TODO: Need some legitimate checking here to make sure the delete operation was successful
    print ("Complete")


############################
class MyPrompt(cmd2.Cmd):

    # Remove CMD2 default commands.
    delattr(cmd2.Cmd, 'do_shell')
    #delattr(cmd2.Cmd, 'do_macro')
    delattr(cmd2.Cmd, 'do_shortcuts')
    delattr(cmd2.Cmd, 'do_run_script')
    delattr(cmd2.Cmd, 'do_run_pyscript')
    delattr(cmd2.Cmd, 'do_edit')  # This may be something to work back in, since it allows editing of files.
    delattr(cmd2.Cmd, 'do_set')   # This may be something to work back in.  Would allow user to set different editors and turn on debugging.
    delattr(cmd2.Cmd, 'do_ipy')
    delattr(cmd2.Cmd, 'do_py')


    prompt = 'swsh> '
    intro = '''
####################################################################
#                                                                  #
#       _______.____    __    ____  __       _______. __    __     #
#      /       |\   \  /  \  /   / |  |     /       ||  |  |  |    #
#     |   (----` \   \/    \/   /  |  |    |   (----`|  |__|  |    #
#      \   \      \            /   |  |     \   \    |   __   |    #
#  .----)   |      \    /\    /    |  | .----)   |   |  |  |  |    #
#  |_______/        \__/  \__/     |__| |_______/    |__|  |__|    #
#                                                                  #
#      Welcome to SWiSH: The SignalWire interactive Shell          #
####################################################################
'''

    def do_exit(self, inp):
        print("Thanks for using SignalWire")
        return True

    def help_exit(self):
        print('exit the application. Shorthand: Ctrl-D.')

    do_quit = do_exit
    help_quit = help_exit

## SIP ENDPOINT
    # Create the top level parser for sip endpoints: sip_endpoint
    base_sip_endpoint_parser = cmd2.Cmd2ArgumentParser()
    base_sip_endpoint_subparsers = base_sip_endpoint_parser.add_subparsers(title='subcommands',help='subcommand help') # TODO: Fix help text

    # create the sip_endpoint list subcommand
    sip_endpoint_parser_list = base_sip_endpoint_subparsers.add_parser('list', help='List SIP Endpoints')

    # create the sip_endpoint update subcommand
    sip_endpoint_parser_update = base_sip_endpoint_subparsers.add_parser('update', help='Update a SIP Endpoint')
    sip_endpoint_parser_update.add_argument('-u', '--username', help='update username of the sip endpoint')
    sip_endpoint_parser_update.add_argument('-p', '--password', help='update password of the sip endpoint')
    sip_endpoint_parser_update.add_argument('-s', '--send-as',  help='default caller id for sip endpoint (Must belong to the Project!)')
    sip_endpoint_parser_update.add_argument('-c', '--caller-id',  help='Friendly Caller ID Name (SIP to SIP only)' )
    sip_endpoint_parser_update.add_argument('-i', '--id', help='Unique id of the SIP Endpoint to be deleted', required=True)
    sip_endpoint_parser_update.add_argument('-e', '--encryption', type=str, help='Default Codecs', choices=['default', 'required', 'optional'])
    sip_endpoint_parser_update.add_argument('--codecs', type=str, nargs='+', help='Default Codecs', choices=['OPUS', 'G722', 'PCMU', 'PCMA', 'VP8', 'H264'])
    sip_endpoint_parser_update.add_argument('--ciphers', type=str, nargs='+',  help='Default Ciphers', choices=['AEAD_AES_256_GCM_8','AES_256_CM_HMAC_SHA1_80','AES_CM_128_HMAC_SHA1_80','AES_256_CM_HMAC_SHA1_32','AES_CM_128_HMAC_SHA1_32'])

    # create the sip_endpoint create subcommand
    sip_endpoint_parser_create = base_sip_endpoint_subparsers.add_parser('create', help='Create a SIP Endpoint')
    sip_endpoint_parser_create.add_argument('-u', '--username', help='username of the sip endpoint', required=True)
    sip_endpoint_parser_create.add_argument('-p', '--password', help='password of the sip endpoint', required=True)
    sip_endpoint_parser_create.add_argument('-s', '--send-as',  help='default caller id for sip endpoint (Must belong to the Project!)', required=True )
    sip_endpoint_parser_create.add_argument('-n', '--caller-id',  help='Friendly Caller ID Name (SIP to SIP only)', required=True )
    sip_endpoint_parser_create.add_argument('-e', '--encryption', type=str, help='Default Codecs', choices=['default', 'required', 'optional'])
    sip_endpoint_parser_create.add_argument('--codecs', type=str, nargs='+', help='Default Codecs', choices=['OPUS', 'G722', 'PCMU', 'PCMA', 'VP8', 'H264'])
    sip_endpoint_parser_create.add_argument('--ciphers', type=str, nargs='+',  help='Default Ciphers', choices=['AEAD_AES_256_GCM_8','AES_256_CM_HMAC_SHA1_80','AES_CM_128_HMAC_SHA1_80','AES_256_CM_HMAC_SHA1_32','AES_CM_128_HMAC_SHA1_32'])

    # create the sip_endpoint delete subcommand
    sip_endpoint_parser_delete = base_sip_endpoint_subparsers.add_parser('delete', help='Delete a SIP Endpoint')
    # API takes the ID, Would be nice to do this by looking up by friendly name and return the ID,
    # but that may return multiple results.  Would need to write some guardrails around that.
    # For now just leaving with having provide the SID.
    sip_endpoint_parser_delete.add_argument('-i', '--id', help='Unique id of the SIP Endpoint', required=True)

    ## subcommand functions for sip_endpoint
    def sip_endpoint_list(self, args):
        '''list subcommand of sip_endpoint'''
        get_sip_endpoints()

    def sip_endpoint_create(self, args):
        '''create subcommand of sip_endpoint'''
        # TODO: Add Codecs and Ciphers
        sip_endpoint_dictionary = {
          "username": args.username,
          "password": args.password,
          "caller_id": args.caller_id,
          "send_as": args.send_as,
          "codecs": args.codecs,
          "ciphers": args.ciphers,
          "encryption": args.encryption
        }

        payload = json.dumps(sip_endpoint_dictionary)
        create_sip_endpoint(payload)

    def sip_endpoint_update(self, args):
        '''update subcommand of sip_endpoint'''
        sid = args.id
        sip_endpoint_dictionary = {
          "username": args.username,
          "password": args.password,
          "caller_id": args.caller_id,
          "send_as": args.send_as,
          "codecs": args.codecs,
          "ciphers": args.ciphers,
          "encryption": args.encryption
        }
        update_sip_endpoint_dictionary = {}
        #print (sip_endpoint_dictionary)
        for x, y in sip_endpoint_dictionary.items():
            if y is not None:
              update_sip_endpoint_dictionary[x] = y

        payload = json.dumps (update_sip_endpoint_dictionary)
        update_sip_endpoint(sid, payload)

    def sip_endpoint_delete(self, args):
        '''delete subcommand of sip_endpoint'''
        sid = args.id
        if sid is not None:
            confirm = input("Remove SIP Endpoint " + sid + "? This cannot be undone! (y/n): " )
            if (confirm == "Y" or confirm == "y"):
                delete_sip_endpoint(sid)
            else:
                print ("Aborting.")
        else:
            print ("ERROR")

    # Set default handlers for each sub command
    sip_endpoint_parser_list.set_defaults(func=sip_endpoint_list)
    sip_endpoint_parser_create.set_defaults(func=sip_endpoint_create)
    sip_endpoint_parser_update.set_defaults(func=sip_endpoint_update)
    sip_endpoint_parser_delete.set_defaults(func=sip_endpoint_delete)

    @cmd2.with_argparser(base_sip_endpoint_parser)
    def do_sip_endpoint(self, args: argparse.Namespace):
        '''List, Update, and Create SIP Endpoint configurations'''
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('sip_endpoint')

## SIP PROFILES ##
    # Create the top level parser for sip profiles: sip_profile
    base_sip_profile_parser = cmd2.Cmd2ArgumentParser()
    base_sip_profile_subparsers = base_sip_profile_parser.add_subparsers(title='subcommands',help='subcommand help') # TODO: Fix help text

    # create the sip_profile list subcommand
    sip_profile_parser_list = base_sip_profile_subparsers.add_parser('list', help='List SIP Profiles')

    # create the sip_profile update subcommand
    sip_profile_parser_update = base_sip_profile_subparsers.add_parser('update', help='Update a SIP profile')
    sip_profile_parser_update.add_argument('-d', '--domain-identifier', help='Domain Identifier of the SIP profile')
    sip_profile_parser_update.add_argument('-s', '--send-as',  help='Default sendas for SIP Endpoints ')
    sip_profile_parser_update.add_argument('-e', '--encryption', type=str, help='Set Default encryption option for SIP Profiles', choices=['required', 'optional'])
    sip_profile_parser_update.add_argument('--codecs', type=str, nargs='+', help='Set Default Codecs for SIP Endpoints', choices=['OPUS', 'G722', 'PCMU', 'PCMA', 'VP8', 'H264'])
    sip_profile_parser_update.add_argument('--ciphers', type=str, nargs='+',  help='Set Default Ciphers for SIP Endpoints', choices=['AEAD_AES_256_GCM_8','AES_256_CM_HMAC_SHA1_80','AES_CM_128_HMAC_SHA1_80','AES_256_CM_HMAC_SHA1_32','AES_CM_128_HMAC_SHA1_32'])

    ## subcommand functions for sip_profile
    def sip_profile_list(self, args):
        '''list subcommand of sip_profile'''
        get_sip_profiles()

    def sip_profile_update(self, args):
        '''update subcommand of sip_profile'''
        sip_profile_dictionary = {
          "domain_identifier": args.domain_identifier,
          "default_send_asas": args.send_as,
          "default_codecs": args.codecs,
          "default_ciphers": args.ciphers,
          "default_encryption": args.encryption
        }
        update_sip_profile_dictionary = {}
        for x, y in sip_profile_dictionary.items():
            if y is not None:
              update_sip_profile_dictionary[x] = y

        payload = json.dumps (update_sip_profile_dictionary)
        update_sip_profiles(payload)

    # Set default handlers for each sub command
    sip_profile_parser_list.set_defaults(func=sip_profile_list)
    sip_profile_parser_update.set_defaults(func=sip_profile_update)

    @cmd2.with_argparser(base_sip_profile_parser)
    def do_sip_profile(self, args: argparse.Namespace):
        '''List, Update, SIP profile configurations'''
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('sip_profile')


## PHONE NUMBERS ##
    # Create the top level parser for phone numbers: phone_numbers
    base_phone_numbers_parser = cmd2.Cmd2ArgumentParser()
    base_phone_numbers_subparsers = base_phone_numbers_parser.add_subparsers(title='subcommands',help='subcommand help') # TODO: Fix help text

    # create the list subcommand
    phone_numbers_parser_list = base_phone_numbers_subparsers.add_parser('list', help='List Phone Numbers for a Projects')
    phone_numbers_parser_list.add_argument('-j', '--json', action='store_true', help='List Phone Numbers for project JSON')
    # TODO:  add lookup for single number
    # phone_numbers_parser.add_argument('lookup', action='store_false',  help='Lookup a specific number.  Mut be formatted in E.164')

    # create the update subcommand
    phone_numbers_parser_update = base_phone_numbers_subparsers.add_parser('update', help='Update a Phone Number')

    # create the delete subcommand
    phone_numbers_parser_delete = base_phone_numbers_subparsers.add_parser('delete', help='Delete/Remove a Phone Number')

    ## subcommand functions for phone numbers
    def phone_numbers_list(self, args):
        '''list subcommand of phone_numbers'''
        if args.json:
            get_phone_numbers()
        else:
            output = os.system(" python3 /usr/lib/cgi-bin/sig-get_phone_numbers_for_space.py | jq '.data[].number' | sed 's/\"//g' ")

    def phone_numbers_update(self, args):
        '''create subcommand of sip_endpoint'''
        print('Update a Phone Number')

    def phone_numbers_delete(self, args):
        '''create subcommand of sip_endpoint'''
        print('Delete/Remove a Phone Number')

    # Set default handlers for each sub command
    phone_numbers_parser_list.set_defaults(func=phone_numbers_list)
    phone_numbers_parser_update.set_defaults(func=phone_numbers_update)
    phone_numbers_parser_delete.set_defaults(func=phone_numbers_delete)

    @cmd2.with_argparser(base_phone_numbers_parser)
    def do_phone_numbers(self, args: argparse.Namespace):
        '''List, Update, and Buy Phone numbers'''
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('phone_numbers')

## LaML BINS
    # Create the top level parser for laml bins: laml_bins
    base_laml_bins_parser = cmd2.Cmd2ArgumentParser()
    base_laml_bins_subparsers = base_laml_bins_parser.add_subparsers(title='subcommands',help='subcommand help') # TODO: Fix help text

    # create the laml_bin list subcommand
    laml_bins_parser_list = base_laml_bins_subparsers.add_parser('list', help='List LaML Bins for a Projects')
    laml_bins_parser_list.add_argument('-f', '--friendly-name', type=str, nargs='+', help='List Single LaML Bin by name')

    # create the laml_bin update subcommand
    laml_bins_parser_update = base_laml_bins_subparsers.add_parser('update', help='Update a LaML Bins')

    # create the laml_bin update subcommand
    laml_bins_parser_create = base_laml_bins_subparsers.add_parser('create', help='Create a LaML Bins')

    # create the laml_bin delete subcommand
    laml_bins_parser_delete = base_laml_bins_subparsers.add_parser('delete', help='Delete/Remove a LaML Bin')

    ## subcommand functions for laml bins
    def laml_bins_list(self, args):
        '''list subcommand of laml_bins'''
        if args.friendly_name:
            if len(args.friendly_name) == 1:
                friendly_name = args.friendly_name[0]
            elif len(args.friendly_name) > 1:
                friendly_name = "%20".join(args.friendly_name)
            else:
                print ("ERROR: Not valid arguments")
            query_params="/LamlBins?Name=%s" % friendly_name
            get_laml_bins(query_params)
        else:
            query_params = "/LamlBins"
            get_laml_bins(query_params)

    def laml_bins_create(self, args):
        '''create subcommand of laml_bins'''
        print('Create a LamL Bin')

    def laml_bins_update(self, args):
        '''create subcommand of laml_bins'''
        print('Create a LaML Bin')

    def laml_bins_delete(self, args):
        '''create subcommand of laml_bins'''
        print('Delete/Remove a Phone Number')

    # Set default handlers for each sub command
    laml_bins_parser_list.set_defaults(func=laml_bins_list)
    laml_bins_parser_create.set_defaults(func=laml_bins_create)
    laml_bins_parser_update.set_defaults(func=laml_bins_update)
    laml_bins_parser_delete.set_defaults(func=laml_bins_delete)

    @cmd2.with_argparser(base_laml_bins_parser)
    def do_laml_bin(self, args: argparse.Namespace):
        '''List, Update, and LaML Bins'''
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('laml_bin')


## SIGNALWIRE SPACES / PROJECTs
    # Create the top level parser for space: space
    base_space_parser = cmd2.Cmd2ArgumentParser()
    base_space_subparsers = base_space_parser.add_subparsers(title='subcommands', help='subcommand help') # TODO: Fix help text

    # Create the space cd subcommand
    space_parser_change = base_space_subparsers.add_parser('cd', help='change to a different space')
    space_parser_change.add_argument('-n', '--hostname', help = 'Domain Hostname of the Space', required=True)
    space_parser_change.add_argument('-t', '--token', help='API token for the Space', required=True)
    space_parser_change.add_argument('-p', '--project-id', help='Project ID to connect to within the space', required=True)

    # Create the space show subcommand
    space_parser_show = base_space_subparsers.add_parser('show', help='show the Current working space and project')
    space_parser_show.add_argument('-t', '--token', help='Include the API token', action='store_true')

    # Subcommand functions for space
    def space_cd(self, args):
        '''change directory subcommand of space'''

        #
        # This will write out the new config to the .env file and be set for restart.
        # Not sure this is really the way I'd like to go.  Maybe it makes sense to just keep what the image was built with as the default.
        # Leaving the code in commented out, just in case its needed later.
        #
        # f = open(".env", "w")
        # f.write("SIGNALWIRE_SPACE=" + args.hostname + "\nPROJECT_ID=" + args.project_id + "\nREST_API_TOKEN=" + args.token)
        # f.close()

        # Not sure if there is a better way to accomplish this, but using global was the only way I could get the variables to persist.
        global signalwire_space
        global project_id
        global rest_api_token

        signalwire_space = args.hostname
        project_id = args.project_id
        rest_api_token = args.token

    def space_show(self, args):
        '''show the working space and project configuration'''
        if args.token:
            output = "SignalWire Space: " + signalwire_space + "\nProject ID: " + project_id + "\nToken: " + rest_api_token + "\n"
        else:
            output = "SignalWire Space: " + signalwire_space + "\nProject ID: " + project_id + "\n"

        print (output)

    # Set default handlers for each sub command
    space_parser_change.set_defaults(func=space_cd)
    space_parser_show.set_defaults(func=space_show)

    @cmd2.with_argparser(base_space_parser)
    def do_space(self, args: argparse.Namespace):
        '''set a new working space'''
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('space_help')

    # Create the top level parser for projects: project
    base_project_parser = cmd2.Cmd2ArgumentParser()
    base_project_subparsers = base_project_parser.add_subparsers(title='subcommands',help='subcommand help') # TODO: Fix help text

    # Create the project list subcommand
    project_parser_list = base_project_subparsers.add_parser('list', help='List LaML Bins for a Projects')
    project_parser_list.add_argument('-f', '--friendly-name', type=str, nargs='+', help='List Single Project by Friendly Name')
    project_parser_list.add_argument('-s', '--sid', type=str, help='List SignalWire Space or Subspace with given SID')

    # Create the project update subcommand
    project_parser_update = base_project_subparsers.add_parser('update', help='Update a project')

    # Create the project update subcommand
    project_parser_create = base_project_subparsers.add_parser('create', help='Create a subproject')

    # Create the project delete subcommand
    project_parser_delete = base_project_subparsers.add_parser('delete', help='Delete/Remove a subproject')

    # Subcommand functions for project
    def project_list(self, args):
        '''list subcommand of project'''
        if args.friendly_name:
            if len(args.friendly_name) == 1:
                friendly_name = args.friendly_name[0]
            elif len(args.friendly_name) > 1:
                friendly_name = "%20".join(args.friendly_name)
            query_params ="?FriendlyName=%s" % friendly_name
        elif args.sid:
             sid = args.sid
             query_params = "/%s" % sid
        else:
            query_params=""

        list_space_projects(query_params=query_params)

    def project_create(self, args):
        '''create subcommand of project'''
        print('Create a project')

    def project_update(self, args):
        '''create subcommand of project'''
        print('Create a project')

    def project_delete(self, args):
        '''create subcommand of project'''
        print('Delete/Remove a project')

    # Set default handlers for each sub command
    project_parser_list.set_defaults(func=project_list)
    project_parser_create.set_defaults(func=project_create)
    project_parser_update.set_defaults(func=project_update)
    project_parser_delete.set_defaults(func=project_delete)

    @cmd2.with_argparser(base_project_parser)
    def do_project(self, args: argparse.Namespace):
        '''get or set a new working space'''
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('project_help')


## DOMAIN APPLICATIONS ##
    # Create the top level parser for domain application: domain_application
    base_domain_application_parser = cmd2.Cmd2ArgumentParser()
    base_domain_application_subparsers = base_domain_application_parser.add_subparsers(title='subcommands',help='subcommand help') # TODO: Fix help text

    # create the domain application list subcommand
    domain_application_parser_list = base_domain_application_subparsers.add_parser('list', help='List Domain Applications for the Project')
    domain_application_parser_list.add_argument('-d', '--domain', type=str, nargs='+', help='Return all values for given domain of Domain App')
    domain_application_parser_list.add_argument('-n', '--name', type=str, nargs='+', help='Return all values for the given name of Domain App')

    # create the domain application create command
    domain_application_parser_create = base_domain_application_subparsers.add_parser('create', help='List Domain Applications for the Project')
    domain_application_parser_create.add_argument('-n', '--name', help='Friendly name for the domain application')
    domain_application_parser_create.add_argument('-i', '--identifier', help='Identifier of the domain.  Must be unique accross the project.')
    domain_application_parser_create.add_argument('--ip-auth-enabled',  help='Whether the domain application will enforce IP authentication (Boolean)', choices=['true','false'] )
    domain_application_parser_create.add_argument('--ip-auth',  help='A List of whitelisted / allowed IPs when --ip-auth-enabled is true ' )
    domain_application_parser_create.add_argument('-c', '--call-handler', help='How the domain Application handles calls', choices=['relay_context','laml_webhooks','laml_application','video_room'] )
    domain_application_parser_create.add_argument('-e', '--encryption', type=str, help='Default Codecs', choices=['default', 'required', 'optional'])
    domain_application_parser_create.add_argument('--codecs', type=str, nargs='+', help='Default Codecs', choices=['OPUS', 'G722', 'PCMU', 'PCMA', 'VP8', 'H264'])
    domain_application_parser_create.add_argument('--ciphers', type=str, nargs='+',  help='Default Ciphers', choices=['AEAD_AES_256_GCM_8','AES_256_CM_HMAC_SHA1_80','AES_CM_128_HMAC_SHA1_80','AES_256_CM_HMAC_SHA1_32','AES_CM_128_HMAC_SHA1_32'])

    # create the domain application update command
    domain_application_parser_update = base_domain_application_subparsers.add_parser('update', help='List Domain Applications for the Project')

    # create the domain application delete command
    domain_application_parser_delete = base_domain_application_subparsers.add_parser('delete', help='List Domain Applications for the Project')
    # API takes the ID, Would be nice to do this by looking up by friendly name and return the ID,
    # but that may return multiple results.  Would need to write some guardrails around that.
    # For now just leaving with having provide the SID.
    domain_application_parser_delete.add_argument('-i', '--id', help='Unique id of the SIP Endpoint', required=True)

    def domain_application_list(self, args):
        '''list subcommand of domain_application'''
        if args.domain:
            if len(args.domain) == 1:
                domain = args.domain[0]
            elif len(args.domain) > 1:
                domain = "%20".join(args.domain)
            query_params ="?filter_domain=%s" % domain
        elif args.name:
             if len(args.name) == 1:
                 name = args.name[0]
             elif len(args.name) > 1:
                 name = "%20".join(args.name)
             query_params = "?filter_name=%s" % name
        else:
            query_params=""

        list_domain_applications(query_params=query_params)

    def domain_application_delete(self, args):
        '''delete subcommand of domain_application'''
        sid = args.id
        if sid is not None:
            confirm = input("Remove Domain Application " + sid + "? This cannot be undone! (y/n): " )
            if (confirm == "Y" or confirm == "y"):
                delete_domain_application(sid)
            else:
                print ("Aborting.")
        else:
            print ("ERROR")

    # Set default handlers for each sub command
    domain_application_parser_list.set_defaults(func=domain_application_list)
    domain_application_parser_delete.set_defaults(func=domain_application_delete)

    @cmd2.with_argparser(base_domain_application_parser)
    def do_domain_application(self, args: argparse.Namespace):
        '''List, Create, Update, or Delete domain applications'''
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('domain_application')


## NUMBER GROUPS ##
    # Create the top level parser for number groups: number_groups
    base_number_group_parser = cmd2.Cmd2ArgumentParser()
    base_number_group_subparsers = base_number_group_parser.add_subparsers(title='subcommands',help='subcommand help') # TODO: Fix help text

    # create the number groups list subcommand
    number_group_parser_list = base_number_group_subparsers.add_parser('list', help='List Number Groups for the Project')
    number_group_parser_list.add_argument('-n', '--name', nargs='+', help='Return all Number Groups containing this value')
    number_group_parser_list.add_argument('-i', '--id',help='Return a Number Group with the given ID')

    # create the number groups create command
    number_group_parser_create = base_number_group_subparsers.add_parser('create', help='Create for the Project')
    number_group_parser_create.add_argument('-n', '--name', nargs='+', help='Name given to a Number Group within the project', required=True)
    number_group_parser_create.add_argument('-s', '--sticky-sender', help='Whether the number group uses the same From number for outbound requests',  choices=['true', 'false'], default='false')

    # create the domain application update command
    number_group_parser_update = base_number_group_subparsers.add_parser('update', help='Update Number Groups for the Project')
    number_group_parser_update.add_argument('-n', '--name', nargs='+', help='Update the name of a Number Group')
    number_group_parser_update.add_argument('-i', '--id', help='ID of the Number Group to be udpated', required=True)
    number_group_parser_update.add_argument('-s', '--sticky-sender', help='Whether the number group uses the same From number for Outbound requests',  choices=['true', 'false'], default='false')

    # create the domain application delete command
    number_group_parser_delete = base_number_group_subparsers.add_parser('delete', help='Delete Number Groups for the Project')
    number_group_parser_delete.add_argument('-i', '--id', help='Unique id of the Number Group to be removed', required=True)

    def number_group_list(self, args):
        '''list subcommand of number_group'''
        query_params=""

        if args.name:
            if len(args.name) == 1:
                name = args.name[0]
            elif len(args.name) > 1:
                name = "%20".join(args.name)
            query_params ="?filter_name=%s" % name
        elif args.id:
            sid = args.id
            query_params = "/%s" % sid
        else:
            query_params=""

        list_number_groups(query_params=query_params)

    def number_group_create(self, args):
        '''create subcommand of number_group'''
        number_group_dictionary = {
          "name": args.name,
          "sticky_sender": args.sticky_sender
        }

        payload = json.dumps(number_group_dictionary)
        create_number_group(payload)

    def number_group_update(self, args):
        '''update subcommand of number_group'''
        sid = args.id
        number_group_dictionary = {
          "name": args.name,
          "sticky_sender": args.sticky_sender
        }

        update_number_group_dictionary = {}
        for x, y in number_group_dictionary.items():
            if y is not None:
              update_number_group_dictionary[x] = y

        payload = json.dumps(update_number_group_dictionary)
        update_number_group(sid, payload)

    def number_group_delete(self, args):
        '''delete subcommand of number_group'''
        sid = args.id
        if sid is not None:
            confirm = input("Remove Number Group " + sid + "? This cannot be undone! (y/n): " )
            if (confirm == "Y" or confirm == "y"):
                delete_number_group(sid)
            else:
                print ("Aborting.")
        else:
            print ("ERROR")

    # Set default handlers for each sub command
    number_group_parser_list.set_defaults(func=number_group_list)
    number_group_parser_create.set_defaults(func=number_group_create)
    number_group_parser_update.set_defaults(func=number_group_update)
    number_group_parser_delete.set_defaults(func=number_group_delete)

    @cmd2.with_argparser(base_number_group_parser)
    def do_number_group(self, args: argparse.Namespace):
        '''List, Create, Update, or Delete domain applications'''
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('number_group')











## SEND TEXT MESSAGE
    sms_parser = cmd2.Cmd2ArgumentParser()
    sms_parser.add_argument('-f', '--from-num', type=str,  help='Send text FROM number -- Must be a signalwire number registered to campaign', required=True)
    sms_parser.add_argument('-t', '--to-num', type=str, help='Send sms text message TO number', required=True)
    sms_parser.add_argument('-b', '--text-body', type=str, nargs='+',  help='Send sms text message TO number', required=True)
    @cmd2.with_argparser(sms_parser)
    def do_send_text(self, args: argparse.Namespace):
        '''Send an SMS Text Message'''
        from_no = args.from_num
        to_no = args.to_num
        text_body = " ".join(args.text_body)
        print ("sending a sms text from " + from_no + " to " + to_no + ": \"" + text_body + "\"" )
        client = signalwire_client(project_id, rest_api_token, signalwire_space_url = '%s.signalwire.com' % signalwire_space)
        message = client.messages.create (
          to=to_no,
          from_=from_no,
          body=text_body
        )

        time.sleep (1)
        print("Complete!")





##
if __name__ == '__main__':
    MyPrompt(completekey='tab').cmdloop()