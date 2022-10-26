#!/usr/bin/env python3
from typing_extensions import Required
import cmd2
import os
import argparse
from functions import *
import json
import time
import re
import urllib.parse
## This is temporary ##
#from signalwire.voice_response import *
#from twilio.twiml.messaging_response import Message, MessagingResponse
from signalwire.rest import Client as signalwire_client


###########################################################################
class MyPrompt(cmd2.Cmd):

    # Remove CMD2 default commands.
    delattr(cmd2.Cmd, 'do_shell')
    #delattr(cmd2.Cmd, 'do_macro')
    delattr(cmd2.Cmd, 'do_shortcuts')
    delattr(cmd2.Cmd, 'do_run_script')
    delattr(cmd2.Cmd, 'do_run_pyscript')
    delattr(cmd2.Cmd, 'do_edit')  # This may be something to work back in, since it allows editing of files.
    #delattr(cmd2.Cmd, 'do_set')   # This may be something to work back in.  Would allow user to set different editors and turn on debugging.
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

## SIP ENDPOINT COMMAND ##
    # Create the top level parser for sip endpoints: sip_endpoint
    base_sip_endpoint_parser = cmd2.Cmd2ArgumentParser()
    base_sip_endpoint_subparsers = base_sip_endpoint_parser.add_subparsers(title='SIP ENDPOINT',help='sip_endpoint help')

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
        output, status_code =  sip_endpoint_func()
        valid = validate_http(status_code)
        if valid:
            output_data = json.loads(output)
            data_json = output_data["data"]
            json_nice_print(data_json)
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                print ("Error: " + output + "\n")

    def sip_endpoint_create(self, args):
        '''create subcommand of sip_endpoint'''
        query_params = ""
        sip_endpoint_dictionary = {
          "username": args.username,
          "password": args.password,
          "caller_id": args.caller_id,
          "send_as": args.send_as,
          "codecs": args.codecs,
          "ciphers": args.ciphers,
          "encryption": args.encryption
        }

        create_sip_endpoint_dictionary = {}
        for x, y in sip_endpoint_dictionary.items():
            if y is not None:
              create_sip_endpoint_dictionary[x] = y

        payload = json.dumps( create_sip_endpoint_dictionary )
        output, status_code = sip_endpoint_func(query_params, "POST",  payload=payload)
        valid = validate_http(status_code)
        if valid:
            # Grab the New ID and print for the user
            output_json = json.loads(output)
            endpoint_id = output_json["id"]
            print("SIP Endpoint created with ID: " + sid + "\n")
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                print (status_code + ": " + output + "\n" )

    def sip_endpoint_update(self, args):
        '''update subcommand of sip_endpoint'''
        sid = args.id
        query_params = "/" + sid
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
        for x, y in sip_endpoint_dictionary.items():
            if y is not None:
              update_sip_endpoint_dictionary[x] = y

        payload = json.dumps ( update_sip_endpoint_dictionary )
        output, status_code = sip_endpoint_func(query_params, "PUT",  payload=payload)
        valid = validate_http(status_code)
        if valid:
            # TODO: Output the sip endpoint after updated.  Maybe?
            print("SIP Endpoint " + sid + " updated.\n")
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                print (status_code + ": " + output + "\n" )

    def sip_endpoint_delete(self, args):
        '''delete subcommand of sip_endpoint'''
        sid = args.id
        query_params = "/" + sid
        if sid is not None:
            confirm = input("Remove SIP Endpoint " + sid + "? This cannot be undone! (y/n): " )
            if (confirm == "Y" or confirm == "y"):
                output, status_code = sip_endpoint_func(query_params, "DELETE")
                valid = validate_http(status_code)
                if valid:
                    print("Success! SIP Endpoint " + sid + " Removed\n")
                else:
                    is_json = validate_json(output)
                    if is_json:
                        print_error_json(output)
                    else:
                        status_code = str(status_code)
                        print ( status_code + ": " + output + "\n" )
            else:
                print ("OK.  Cancelling...\n")
        else:
            print ("ERROR: Please enter a valid SID\n")

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


## SIP PROFILE COMMAND ##
    # Create the top level parser for sip profiles: sip_profile
    base_sip_profile_parser = cmd2.Cmd2ArgumentParser()
    base_sip_profile_subparsers = base_sip_profile_parser.add_subparsers(title='SIP PROFILE',help='sip_profile help')

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
        output, status_code = sip_profile_func()
        valid = validate_http(status_code)
        if valid:
            output_json = json.loads(output)
            json_nice_print(output_json)
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                print (status_code + ": " + output + "\n" )

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

        payload = json.dumps(update_sip_profile_dictionary)
        output, status_code = sip_profile_func(req_type="PUT", payload=payload)
        valid = validate_http(status_code)
        if valid:
            print("Complete.  The SIP Profile has been updated.\n")
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                print (status_code + ": " + output + "\n" )

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


## PHONE NUMBER COMMAND ##
    # Create the top level parser for phone numbers: phone_number
    base_phone_number_parser = cmd2.Cmd2ArgumentParser()
    base_phone_number_subparsers = base_phone_number_parser.add_subparsers(title='PHONE NUMBER',help='phone_number help')

    # create the phone_number list subcommand
    phone_number_parser_list = base_phone_number_subparsers.add_parser('list', help='List Phone Numbers for a Projects')
    phone_number_parser_list.add_argument('-j', '--json', action='store_true', help='List Phone Numbers for project in JSON Format')
    phone_number_parser_list.add_argument('-n', '--name', help='Find a phone number by object Name')
    phone_number_parser_list.add_argument('-i', '--id', help='Find a phone number by SignalWire ID')
    phone_number_parser_list.add_argument('-b', '--number', help='Return a phone number by number in E164 format')

    # create the phone_number update subcommand
    phone_number_parser_update = base_phone_number_subparsers.add_parser('update', help='Update a Phone Number')
    phone_number_parser_update.add_argument('-i', '--id', help='ID of the SignalWire Phone Number', required=True)
    phone_number_parser_update.add_argument('-n', '--name', help='Update the Friendly Name of a Phone Number')
    phone_number_parser_update.add_argument('--call-handler', help='Type of handlers to use when processing calls to the Number', choices=["relay_context", "laml_webhooks", "laml_application", "dialogflow", "relay_connector", "relay_sip_endpoint", "relay_verto_endpoint", "video_room"])
    phone_number_parser_update.add_argument('--call-receive-mode', help='How to receive the incoming call: Voice or Fax', choices=["voice", "fax"], default="voice")
    phone_number_parser_update.add_argument('--call-request-url', help='URL to make a request when using the laml_webhooks call handler')
    phone_number_parser_update.add_argument('--call-request-method', help='HTTP method type when using laml_webhook call handler', choices=["POST", "GET"], default="POST")
    phone_number_parser_update.add_argument('--call-fallback-url', help='Secondary URL for laml_webhook call handler, in the instance the Primary webhook fails')
    phone_number_parser_update.add_argument('--call-fallback-method', help='HTTP method type when using a fallback laml_webhook message handler', choices=["POST", "GET"], default="POST")
    phone_number_parser_update.add_argument('--call-status-callback-url', help='URL to make status callbacks when using the laml_webhooks call handler')
    phone_number_parser_update.add_argument('--call-status-callback-method', help='HTTP method type when using the call_status_callback_url', choices=["POST", "GET"], default="POST")
    phone_number_parser_update.add_argument('--call-laml-application-id', help='ID of the LaML Webhook Application when using the laml_application call handler')
    phone_number_parser_update.add_argument('--call-dialogflow-id', help='ID of the Dialogflow Agent to start when using the dialogflow call handler')
    phone_number_parser_update.add_argument('--call-relay-context', help='The name of the Relay Context to send this call to when using the relay_context call handler')
    phone_number_parser_update.add_argument('--call-relay-connector-id', help='ID of the Relay Connector to send this call to when using the relay_connector call hanlder')
    phone_number_parser_update.add_argument('--call-sip-endpoint-id', help='ID of the SIP Endpoint to send this call to when using the sip_endpoint call handler')
    phone_number_parser_update.add_argument('--call-verto-resourece', help='The name of the Verto Relay endpoint to send this call to when using the relay_verto_endpoint handler')
    phone_number_parser_update.add_argument('--call-video-room-id', help='The OD of the Video Room to send this call to when using the video_room call handler')
    phone_number_parser_update.add_argument('--message-handler', help='Type of handler to use on inbound text messages', choices=["relay_context", "laml_webhook", "laml_application"])
    phone_number_parser_update.add_argument('--message-request-url', help='URL used to make requests using the laml_webhook message handler')
    phone_number_parser_update.add_argument('--message-request-method', help='HTTP method type when using laml_webhook message handler', choices=["POST", "GET"], default="POST")
    phone_number_parser_update.add_argument('--message-fallback-url', help='Secondary URL for laml_webhook, in the instance the Primary fails')
    phone_number_parser_update.add_argument('--message-fallback-method', help='HTTP method type when using laml_webhook message handler', choices=["POST", "GET"], default="POST")
    phone_number_parser_update.add_argument('--message-laml-application-id', help='The ID of the LamL Application to use when using the laml_application message handler')
    phone_number_parser_update.add_argument('--message-relay-context', help='The name of the relay context to send this message when using the relay_context message handler')

    # create the phone_number release subcommand
    phone_number_parser_release = base_phone_number_subparsers.add_parser('release', help='release/Remove a Phone Number')
    phone_number_parser_release.add_argument('-i', '--id', help='The SignalWire ID of the number that is being Released (removed)')

    # create the phone_number lookup sub
    phone_number_parser_lookup = base_phone_number_subparsers.add_parser('lookup', help='Lookup a Phone Number (in E.164 format)')
    phone_number_parser_lookup.add_argument('--number', help='Number you want to lookup (in E.164 format)', required=True)
    phone_number_parser_lookup.add_argument('--cnam', action='store_true', help='Include carrier lookup')
    phone_number_parser_lookup.add_argument('--carrier', action='store_true', help='Include carrier lookup')

    # create the phone numbers buy command
    phone_number_parser_buy = base_phone_number_subparsers.add_parser('buy', help='Purchase Phone numbers for the Proect')

    ## subcommand functions for phone numbers
    def phone_number_list(self, args):
        '''list subcommand of phone_number'''
        if args.json:
            output, status_code = phone_number_func()
            valid = validate_http(status_code)
            if valid:
                output_json = json.loads(output)
                data_json = output_json["data"]
                json_nice_print(data_json)
            else:
                is_json = validate_json(output)
                if is_json:
                    print_error_json(output)
                else:
                    print (status_code + ": " + output + "\n" )
        elif args.id:
            sid = args.id
            query_params = "/" + sid
            output, status_code = phone_number_func(query_params)
            valid = validate_http(status_code)
            if valid:
                output_json = json.loads(output)
                json_nice_print(output_json)
            else:
                is_json = validate_json(output)
                if is_json:
                    print_error_json(output)
                else:
                    print (status_code + ": " + output + "\n" )
        elif args.name or args.number:
            # TODO: Currently only supporting a single name value AKA "name" as oppsed to "name test".  Try to make this support more (may not actually be supported by API)
            # Keeping code into allow it to be mutiple values just in case.
            #if len(args.name) == 1:
            #    name = args.name[0]
            #elif len(args.name) > 1:
            #    name = "%20".join(args.name)
            query_params = "?"
            if args.name:
                name = urllib.parse.quote(args.name)
                query_params = query_params + "filter_name=%s&" % name
            if args.number:
                number = urllib.parse.quote(args.number)
                query_params = query_params + "filter_number=%s&" % number

            query_params = query_params[:-1] # Removing the final character to clean up dangling &
            output, status_code = phone_number_func(query_params)
            valid = validate_http(status_code)
            if valid:
                output_json = json.loads(output)
                data_json = output_json["data"]
                json_nice_print(data_json)
            else:
                is_json = validate_json(output)
                if is_json:
                    print_error_json(output)
                else:
                    print (status_code + ": " + output + "\n" )
        else:
            output, status_code = phone_number_func()
            valid = validate_http(status_code)
            if valid:
                json_data = json.loads(output)
                tn_data = json_data["data"]
                for index, value in enumerate(tn_data):
                    # Create a temporary dictionary for each number then only return the number value
                    # NOTE: Someday this could be expanded to return the number and the ID or something like that
                    temp_d = value
                    print (temp_d["number"])
            else:
                is_json = validate_json(output)
                if is_json:
                    print_error_json(output)
                else:
                    print (status_code + ": " + output + "\n" )


    def phone_number_update(self, args):
        '''Update subcommand of phone_number'''
        # NOTE: I found that if the number DOES NOT have a name, the API won't allow it to be udpated and will require a name.  After that, it is no longer needed.
        sid = args.id
        query_params = "/" + sid
        phone_number_dictionary = {
          "name": args.name,
          "call_handler": args.call_handler,
          "call_receive_mode": args.call_receive_mode,
          "call_request_url": args.call_request_url,
          "call_request_method": args.call_request_method,
          "call_fallback_url": args.call_fallback_url,
          "call_fallback_method": args.call_fallback_method,
          "call_status_callback_url": args.call_status_callback_url,
          "call_status_callback_method": args.call_status_callback_method,
          "call_laml_application_id": args.call_laml_application_id,
          "call_dialogflow_id": args.call_dialogflow_id,
          "call_relay_context": args.call_relay_context,
          "call_relay_connector_id": args.call_relay_connector_id,
          "call_sip_endpoint_id": args.call_sip_endpoint_id,
          "call_verto_resourece": args.call_verto_resourece,
          "call_video_room_id": args.call_video_room_id,
          "message_handler": args.message_handler,
          "message_request_url": args.message_request_url,
          "message_request_method": args.message_request_method,
          "message_fallback_url": args.message_fallback_url,
          "message_fallback_method": args.message_fallback_method,
          "message_laml_application_id": args.message_laml_application_id,
          "message_relay_context": args.message_relay_context
        }

        update_phone_number_dictionary = {}
        for x, y in phone_number_dictionary.items():
            if y is not None:
                update_phone_number_dictionary[x] = y

        payload = json.dumps(update_phone_number_dictionary)
        output, status_code = phone_number_func(query_params, "PUT",  payload=payload)
        valid = validate_http(status_code)
        if valid:
            output_json = json.loads(output)
            phone_number = output_json["number"]
            print(phone_number + " has been updated successfully\n")
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                is_json = validate_json(output)
                if is_json:
                    print_error_json(output)
                else:
                    print (status_code + ": " + output + "\n" )


    def phone_number_release(self, args):
        '''Release subcommand of phone_number'''
        # TODO: allow the number to be used for release as well
        # We can get the id from the number and then release.
        sid = args.id
        query_params = "/" + sid
        confirm = str(input("Are you sure you want to proceed removing id " + sid + "?  This cannot be undone! (Y/n): " ))
        # Need validation here.  There are times when the number is too new to be released.  Would be nice to be able to relay that.
        if confirm.lower() == "yes" or confirm.lower() == "y":
            print("we are here")
            output, status_code = phone_number_func(query_params, "DELETE")
            valid = validate_http(status_code)
            if valid:
                # TODO: Pull the number from the API first, that way we have all the data here and can output the number correctly, rather than the SID.
                print("Phone number with SID, " + sid + ", has been successfully Removed\n")
            else:
                is_json = validate_json(output)
                if is_json:
                    print_error_json(output)
                else:
                    is_json = validate_json(output)
                    if is_json:
                        print_error_json(output)
                    else:
                        print (status_code + ": " + output + "\n" )
        else:
            print("Cancelling...\n")

    def phone_number_lookup(self, args):
        '''lookup subcommand of phone_number'''
        # TODO: Refactor this command using new(er) functions
        # Verify its a 10 digit US number in e.164 format.
        number = args.number
        phone_num_regex = re.compile(r'^\+1\d{10}$')
        good_num = phone_num_regex.search(number)

        if good_num is not None:
            if args.cnam and args.carrier:
                include = "?include=cnam,carrier"
            elif args.cnam:
                include = "?include=cnam"
            elif args.carrier:
                include = "?include=carrier"
            else:
                include = ""

            query_params = number + include
            phone_number_lookup(query_params=query_params)
        else:
            print('ERROR: That number is not in a valid e.164 format')

    def phone_number_buy(self, args):
        '''buy subcommand of phone_number'''
        # TODO: Make this much more robust.
        # TODO: Add switches to pass in from command line
        # TODO: Buy multiple numbers / bulk numbers
        os.system(" python3 /usr/lib/cgi-bin/buy_a_phone_number.py ")

    # Set default handlers for each sub command
    phone_number_parser_list.set_defaults(func=phone_number_list)
    phone_number_parser_update.set_defaults(func=phone_number_update)
    phone_number_parser_release.set_defaults(func=phone_number_release)
    phone_number_parser_lookup.set_defaults(func=phone_number_lookup)
    phone_number_parser_buy.set_defaults(func=phone_number_buy)

    @cmd2.with_argparser(base_phone_number_parser)
    def do_phone_number(self, args: argparse.Namespace):
        '''List, Update, and Buy Phone numbers'''
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('phone_number')


## LaML BINS ##
    # Create the top level parser for laml bins: laml_bin
    base_laml_bin_parser = cmd2.Cmd2ArgumentParser()
    base_laml_bin_subparsers = base_laml_bin_parser.add_subparsers(title='LaML BINS',help='laml_bin help')

    # create the laml_bin list subcommand
    laml_bin_parser_list = base_laml_bin_subparsers.add_parser('list', help='List LaML Bins for a Projects')
    laml_bin_parser_list.add_argument('-n', '--name', type=str, nargs='+', help='List Single LaML Bin by name')
    laml_bin_parser_list.add_argument('-i', '--id', help='List Single LaML Bin by SignalWire ID')

    # create the laml_bin update subcommand
    laml_bin_parser_create = base_laml_bin_subparsers.add_parser('create', help='Create a LaML Bins')
    laml_bin_parser_create.add_argument('-n', '--name', nargs='+', help='Identifiable name of the LaML Bin', required=True)
    laml_bin_parser_create.add_argument('--contents',  nargs='+', help='XML contents of the LaML Bin.  Put formatted XML in single quotes, or leave blank to use an editor')

    # create the laml_bin update subcommand
    laml_bin_parser_update = base_laml_bin_subparsers.add_parser('update', help='Update a LaML Bins')
    laml_bin_parser_update.add_argument('-i', '--id', help='SignalWire ID of the LaML Bin')
    laml_bin_parser_update.add_argument('-n', '--name', nargs='+', help='Identifiable name of the LaML Bin')
    laml_bin_parser_update.add_argument('--contents', nargs='+', help='XML contents of the LaML Bin.  Put formatted XML in single quotes, or leave blank to use an editor')

    # create the laml_bin delete subcommand
    laml_bin_parser_delete = base_laml_bin_subparsers.add_parser('delete', help='Delete/Remove a LaML Bin')
    laml_bin_parser_delete.add_argument('-i', '--id', help='SignalWire ID of the LaML Bin to be deleted')

    # Note: Adding contents on the command line via create and update isn't quite working right
    # because of character escaping it does on  newlines and tabs.
    # It works, just the formatting is a little strange.  Need to come back to this and clean it up

    ## subcommand functions for laml bins
    def laml_bin_list(self, args):
        '''list subcommand of laml_bin'''
        query_params = ""
        if args.name:
            if len(args.name) == 1:
                name = args.name[0]
            elif len(args.name) > 1:
                name = "%20".join(args.name)
            else:
                print ("ERROR: Not valid arguments")
            query_params="?Name=%s" % name
        if args.id:
            sid = args.id
            query_params="/" + sid

        output, status_code = laml_bin_func(query_params)
        valid = validate_http(status_code)
        if valid:
            output_json = json.loads(output)
            if args.id:
                output_laml_bin = output_json
            else:
                output_laml_bin = output_json["laml_bins"]
            json_nice_print(output_laml_bin)
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json_compatibility(output)
            else:
                print ("Error: " + output + "\n")

    def laml_bin_create(self, args):
        '''create subcommand of laml_bin'''
        # Arg lists Needs to be converted into strings before they can be url encoded.
        if args.contents is None:
            # NOTE: There may be a better way to check whether or not the file was changed, than using system calls to sha1sum.
            # However, just looking for the basic functionality at this point.  If the editor is opened, and nothing changes, don't create anything.
            # IF something DOES change in the XML, then push to the API call.
            laml_sha1_orig = os.popen( "sha1sum /tmp/.foo_laml.xml.orig" ).read()  # the sha1sum of the original template
            os.system( "cp /tmp/.foo_laml.xml.orig /tmp/foo_laml.xml")
            os.system( "vim /tmp/foo_laml.xml" )
            laml_sha1_new = os.popen( "sha1sum /tmp/foo_laml.xml").read()          # sha1sum after any changes
            if laml_sha1_orig != laml_sha1_new:
                with open('/tmp/foo_laml.xml') as f:
                    lines = f.readlines()
                    #print(lines)
                    args.contents = lines
                    # Delete the new file, its no longer needed
                    os.system( "rm /tmp/foo_laml.xml")
            else:
                args.contents=""

        # if contents is still blank, then nothing has changed, and exit gracefully
        if args.contents == "":
            print("LaML Bin XML contents are required!")
        else:
            name = ' '.join(args.name)
            contents = ' '.join(args.contents)
            name_url_encode = urllib.parse.quote(name)
            contents_url_encode = urllib.parse.quote(contents, safe='/')
            payload = "Contents=%s&Name=%s" % (contents_url_encode, name_url_encode)
            output, status_code = laml_bin_func(req_type="POST", payload=payload)
            valid = validate_http(status_code)
            if valid:
                output_json = json.loads(output)
                sid = str(output_json["sid"])
                print ("LaML Bin, " + sid + " has been created successfully\n")
            else:
                is_json = validate_json(output)
                if is_json:
                    print_error_json_compatibility(output)
                else:
                    print ("Error: " + output + "\n")

    def laml_bin_update(self, args):
        '''create subcommand of laml_bin'''
        sid = args.id
        query_params = "/" + sid
        if args.contents is None:
            # Get the LaML bin to Edit and save it to a temp file
            query_params = "/" + sid
            output, status_code =  laml_bin_func(query_params)
            valid = validate_http(status_code)  # We can probably get away without validating here, but may as well
            if valid:
                output_json = json.loads(output)
                output_laml_bin_contents = output_json["contents"]
                filename = '/tmp/%s.xml' % sid
                with open(filename, 'w')  as f:
                    print(output_laml_bin_contents, file=f)
                sha1_hash_orig = os.popen( "sha1sum %s | awk '{print $1}'" % filename ).read()
                os.system( "vim %s" % filename )
                sha1_hash_new = os.popen( "sha1sum %s | awk '{print $1}'" % filename ).read()

                if sha1_hash_orig != sha1_hash_new:
                    with open(filename) as f:
                        lines = f.readlines()
                        args.contents = lines
                        os.system( "rm %s" % filename )
            else:
                print ("Error: Something bad happened")

        # URL Encode the params
        if args.name:
            name = ' '.join(args.name)
            name_url_encode = urllib.parse.quote(name)
        if args.contents:
            contents = ' '.join(args.contents)
            contents_url_encode = urllib.parse.quote(contents, safe='/')

        payload = ""
        if args.name and args.contents:
            payload = "Contents=%s&Name=%s" % (contents_url_encode, name_url_encode)
        elif args.name:
            payload = "Name=%s" % (name_url_encode)
        elif args.contents:
            payload = "Contents=%s" % (contents_url_encode)
        else:
            print("Nothing has changed.  Exiting.\n")

        if payload != "":
            output, status_code = laml_bin_func(query_params, req_type="POST", payload=payload)
            valid = validate_http(status_code)
            if valid:
                output_json = json.loads(output)
                print ("LaML Bin, " + sid + " has been updated successfully\n")
            else:
                is_json = validate_json(output)
                if is_json:
                    print_error_json_compatibility(output)
                else:
                    print ("Error: " + output + "\n")

    def laml_bin_delete(self, args):
        '''create subcommand of laml_bin'''
        sid = args.id
        query_params = '/' + sid
        confirm = str(input("Are you sure you want to proceed removing this LaML Bin?  This cannot be undone (Y/n): "))
        if confirm.lower() == "yes" or confirm.lower() == "y":
            output, status_code = laml_bin_func( query_params, "DELETE" )
            valid = validate_http(status_code)
            if valid:
                print("Success! LaML Bin " + sid + " Removed\n")
            else:
                is_json = validate_json(output)
                if is_json:
                    print_error_json_compatibility(output)
                else:
                    status_code = str(status_code)
                    print ( status_code + ": " + output + "\n" )
        else:
            print("Cancelling...")

    # Set default handlers for each sub command
    laml_bin_parser_list.set_defaults(func=laml_bin_list)
    laml_bin_parser_create.set_defaults(func=laml_bin_create)
    laml_bin_parser_update.set_defaults(func=laml_bin_update)
    laml_bin_parser_delete.set_defaults(func=laml_bin_delete)

    @cmd2.with_argparser(base_laml_bin_parser)
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
    base_space_subparsers = base_space_parser.add_subparsers(title='SPACE', help='space help')

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
        os.environ['SIGNALWIRE_SPACE'] = args.hostname
        os.environ['PROJECT_ID'] = args.project_id
        os.environ['REST_API_TOKEN'] = args.token

        # TODO: Add validation to verify the space and creds added are actually valid.
        # Would also be nice to password validate somehow to make sure only an authorized user for the space has access (Although I guess that is what an API token is designed to do)
        signalwire_space, project_id, rest_api_token = get_environment()

        print ("\nNow working in project, " + project_id + ", in the " + signalwire_space + " SignalWire space")

    def space_show(self, args):
        '''show the working space and project configuration'''
        signalwire_space, project_id, rest_api_token = get_environment()
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
    base_project_subparsers = base_project_parser.add_subparsers(title='PROJECT',help='project help')

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

        output, status_code = project_func(query_params=query_params)
        valid = validate_http(status_code)
        if valid:
            output_json = json.loads(output)
            accounts_json = output_json["accounts"]
            json_nice_print (accounts_json)
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                status_code = str(status_code)
                print ( status_code + ": " + output + "\n" )

    def project_create(self, args):
        '''create subcommand of project'''
        print('Create a project -- Coming Soon')

    def project_update(self, args):
        '''create subcommand of project'''
        print('Create a project -- Coming Soon')

    def project_delete(self, args):
        '''create subcommand of project'''
        print('Delete/Remove a project -- Coming Soon')

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


## LaML APPLICATIONS ##
    # Create the top level parser for domain application: laml_app
    base_laml_app_parser = cmd2.Cmd2ArgumentParser()
    base_laml_app_subparsers = base_laml_app_parser.add_subparsers(title='LaML APP',help='laml_app help')

    # create the domain application list subcommand
    laml_app_parser_list = base_laml_app_subparsers.add_parser('list', help='List LaML Applications for the Project')
    laml_app_parser_list.add_argument('-i', '--id', help='SignalWire ID of the LamL Application')

    # create the domain application create command
    laml_app_parser_create = base_laml_app_subparsers.add_parser('create', help='List Domain Applications for the Project')
    laml_app_parser_create.add_argument('-n', '--name',  nargs='+', help='Friendly name for the domain application', required=True)
    laml_app_parser_create.add_argument('--status-callback', help='URL to pass status updates to the application')
    laml_app_parser_create.add_argument('--status-callback-method',  help='HTTP method for status_callback.  Default is POST.', choices=["POST", "GET"], default="POST" )
    laml_app_parser_create.add_argument('--voice-caller-id-lookup',  help='Look up a callers ID from the database.  Possible values are true or false.  Default is false.', choices=["true", "false"], default="false")
    laml_app_parser_create.add_argument('--voice-url',  help='URL to request when an voice or fax is received')
    laml_app_parser_create.add_argument('--voice-method', help='HTTP method for voice_url.  Default is POST.')
    laml_app_parser_create.add_argument('--voice-fallback-url', help='URL to request if there is an error at primary')
    laml_app_parser_create.add_argument('--voice-fallback-method', help='HTTP method for voice_fallback.  Default is POST.', choices=["POST", "GET"], default="POST")
    laml_app_parser_create.add_argument('--message-status-callback', help='When a message receives a status change, a POST request to this URL with message details')
    laml_app_parser_create.add_argument('--sms-url',  help='URL to request when an SMS is received')
    laml_app_parser_create.add_argument('--sms-method',  help='HTTP method for sms_url.  Default is POST.', choices=["POST", "GET"], default="POST" )
    laml_app_parser_create.add_argument('--sms-fallback-url',  help='URL Signalwire will request if errors occur when fetching the sms_url ' )
    laml_app_parser_create.add_argument('--sms-fallback-method',  help='HTTP method for sms_fallback_url.  Default is POST.', choices=["POST", "GET"], default="POST" )
    laml_app_parser_create.add_argument('--sms-status-callback', help='When a message recevies a status change, a POST request to this URL with message details')

    # create the domain application update command
    laml_app_parser_update = base_laml_app_subparsers.add_parser('update', help='List Domain Applications for the Project')
    laml_app_parser_update.add_argument('-i', '--id', help='ID of the Domain Application to be updated', required=True)
    laml_app_parser_update.add_argument('-n', '--name',  nargs='+', help='Friendly name for the domain application')
    laml_app_parser_update.add_argument('--status-callback', help='URL to pass status updates to the application')
    laml_app_parser_update.add_argument('--status-callback-method',  help='HTTP method for status_callback.  Default is POST.', choices=["POST", "GET"], default="POST" )
    laml_app_parser_update.add_argument('--voice-caller-id-lookup',  help='Look up a callers ID from the database.  Possible values are true or false.  Default is false.', choices=["true", "false"], default="false")
    laml_app_parser_update.add_argument('--voice-url',  help='URL to request when an voice or fax is received')
    laml_app_parser_update.add_argument('--voice-method', help='HTTP method for voice_url.  Default is POST.')
    laml_app_parser_update.add_argument('--voice-fallback-url', help='URL to request if there is an error at primary')
    laml_app_parser_update.add_argument('--voice-fallback-method', help='HTTP method for voice_fallback.  Default is POST.', choices=["POST", "GET"], default="POST")
    laml_app_parser_update.add_argument('--message-status-callback', help='When a message receives a status change, a POST request to this URL with message details')
    laml_app_parser_update.add_argument('--sms-url',  help='URL to request when an SMS is received')
    laml_app_parser_update.add_argument('--sms-method',  help='HTTP method for sms_url.  Default is POST.', choices=["POST", "GET"], default="POST" )
    laml_app_parser_update.add_argument('--sms-fallback-url',  help='URL Signalwire will request if errors occur when fetching the sms_url ' )
    laml_app_parser_update.add_argument('--sms-fallback-method',  help='HTTP method for sms_fallback_url.  Default is POST.', choices=["POST", "GET"], default="POST" )
    laml_app_parser_update.add_argument('--sms-status-callback', help='When a message recevies a status change, a POST request to this URL with message details')


    # create the laml_app delete command
    laml_app_parser_delete = base_laml_app_subparsers.add_parser('delete', help='List Domain Applications for the Project')
    laml_app_parser_delete.add_argument('-i', '--id', help='Unique id of the SIP Endpoint', required=True)

    def laml_app_list(self, args):
        '''list subcommand of laml_app'''
        if args.id:
            sid = args.id
            query_params = "/" + sid
        else:
            query_params=""

        output, status_code = laml_app_func(query_params)
        valid = validate_http(status_code)
        if valid:
            output_json = json.loads(output)
            if args.id:
                json_nice_print(output_json)   # When retrieving just an ID, there is no data json object
            else:
                json_applications = output_json["applications"]
                json_nice_print(json_applications)
        else:
            is_json = validate_json_compatibility(output)
            if is_json:
                 print_error_json(output)
            else:
                 status_code = str(status_code)
                 print ( status_code + ": " + output + "\n" )


    def laml_app_create(self, args):
        '''create subcommand of laml_app'''
        FriendlyName = ""
        MessageStatusCallback = ""
        SmsFallbackMethod = ""
        SmsFallbackUrl = ""
        SmsMethod = ""
        SmsStatusCallback = ""
        SmsUrl = ""
        StatusCallback = ""
        StatusCallbackMethod = ""
        VoiceCallerIdLookup = ""
        VoiceFallbackMethod = ""
        VoiceFallbackUrl = ""
        VoiceMethod = ""
        VoiceUrl = ""

        if args.name:
            args.name = ' '.join(args.name)
            FriendlyName = "&FriendlyName=" + urllib.parse.quote(args.name)
        if args.message_status_callback:
            MessageStatusCallback = "&MessageStatusCallback=" + urllib.parse.quote(args.message_status_callback)
        if args.sms_fallback_method:
            SmsFallbackMethod = "&SmsFallbackMethod=" + urllib.parse.quote(args.sms_fallback_method)
        if args.sms_fallback_url:
            SmsFallbackUrl = "&SmsFallbackUrl=" + urllib.parse.quote(args.sms_fallback_url)
        if args.sms_method:
            SmsMethod = "&SmsMethod=" + urllib.parse.quote(args.sms_method)
        if args.sms_status_callback:
            SmsStatusCallback = "SmsStatusCallback=" + urllib.parse.quote(args.sms_status_callback)
        if args.sms_url:
            SmsUrl = "&SmsUrl=" + urllib.parse.quote(args.sms_url)
        if args.status_callback:
            StatusCallback = "&StatusCallback=" + urllib.parse.quote(args.status_callback)
        if args.status_callback_method:
            StatusCallbackMethod = "&StatusCallbackMethod=" + urllib.parse.quote(args.status_callback_method)
        if args.voice_caller_id_lookup:
            VoiceCallerIdLookup = "&VoiceCallerIdLookup=" + urllib.parse.quote(args.voice_caller_id_lookup)
        if args.voice_fallback_method:
            VoiceFallbackMethod = "&VoiceFallbackMethod=" + urllib.parse.quote(args.voice_fallback_method)
        if args.voice_fallback_url:
            VoiceFallbackUrl = "&VoiceFallbackUrl=" + urllib.parse.quote(args.voice_fallback_url)
        if args.voice_method:
            VoiceMethod = "&VoiceMethod=" + urllib.parse.quote(args.voice_fallback_url)
        if args.voice_url:
            VoiceUrl = "&VoiceUrl=" + urllib.parse.quote(args.voice_url)

        payload = FriendlyName + MessageStatusCallback + SmsFallbackMethod + SmsFallbackUrl + SmsMethod + SmsStatusCallback + SmsUrl + StatusCallback + StatusCallbackMethod + VoiceCallerIdLookup + VoiceFallbackMethod + VoiceFallbackUrl + VoiceMethod + VoiceUrl

        output, status_code = laml_app_func(req_type="POST", payload=payload)
        valid = validate_http(status_code)
        if valid:
            output_json = json.loads(output)
            sid = str(output_json["sid"])
            print ("LaML App, " + sid + " has been created successfully\n")
        else:
            is_json = valididate_json(output)
            if is_json:
                print_error_json_compatibility(output)
            else:
                print("Error: " + output + "\n")

    def laml_app_update(self, args):
        '''update subcommand of laml_app'''
        sid = args.id
        query_params = "/" + sid
        FriendlyName = ""
        MessageStatusCallback = ""
        SmsFallbackMethod = ""
        SmsFallbackUrl = ""
        SmsMethod = ""
        SmsStatusCallback = ""
        SmsUrl = ""
        StatusCallback = ""
        StatusCallbackMethod = ""
        VoiceCallerIdLookup = ""
        VoiceFallbackMethod = ""
        VoiceFallbackUrl = ""
        VoiceMethod = ""
        VoiceUrl = ""

        if args.name:
            args.name = ' '.join(args.name)
            FriendlyName = "&FriendlyName=" + urllib.parse.quote(args.name)
        if args.message_status_callback:
            MessageStatusCallback = "&MessageStatusCallback=" + urllib.parse.quote(args.message_status_callback)
        if args.sms_fallback_method:
            SmsFallbackMethod = "&SmsFallbackMethod=" + urllib.parse.quote(args.sms_fallback_method)
        if args.sms_fallback_url:
            SmsFallbackUrl = "&SmsFallbackUrl=" + urllib.parse.quote(args.sms_fallback_url)
        if args.sms_method:
            SmsMethod = "&SmsMethod=" + urllib.parse.quote(args.sms_method)
        if args.sms_status_callback:
            SmsStatusCallback = "SmsStatusCallback=" + urllib.parse.quote(args.sms_status_callback)
        if args.sms_url:
            SmsUrl = "&SmsUrl=" + urllib.parse.quote(args.sms_url)
        if args.status_callback:
            StatusCallback = "&StatusCallback=" + urllib.parse.quote(args.status_callback)
        if args.status_callback_method:
            StatusCallbackMethod = "&StatusCallbackMethod=" + urllib.parse.quote(args.status_callback_method)
        if args.voice_caller_id_lookup:
            VoiceCallerIdLookup = "&VoiceCallerIdLookup=" + urllib.parse.quote(args.voice_caller_id_lookup)
        if args.voice_fallback_method:
            VoiceFallbackMethod = "&VoiceFallbackMethod=" + urllib.parse.quote(args.voice_fallback_method)
        if args.voice_fallback_url:
            VoiceFallbackUrl = "&VoiceFallbackUrl=" + urllib.parse.quote(args.voice_fallback_url)
        if args.voice_method:
            VoiceMethod = "&VoiceMethod=" + urllib.parse.quote(args.voice_method)
        if args.voice_url:
            VoiceUrl = "&VoiceUrl=" + urllib.parse.quote(args.voice_url)

        payload = FriendlyName + MessageStatusCallback + SmsFallbackMethod + SmsFallbackUrl + SmsMethod + SmsStatusCallback + SmsUrl + StatusCallback + StatusCallbackMethod + VoiceCallerIdLookup + VoiceFallbackMethod + VoiceFallbackUrl + VoiceMethod + VoiceUrl

        output, status_code = laml_app_func(query_params, req_type="POST", payload=payload)
        valid = validate_http(status_code)
        if valid:
            output_json = json.loads(output)
            print ("LaML App, " + sid + " has been updated successfully\n")
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json_compatibility(output)
            else:
                print ("Error: " + output + "\n")

    def laml_app_delete(self, args):
        sid = args.id
        query_params = "/" + sid
        if sid is not None:
            confirm = input("Remove LaML Application " + sid + "?  This cannot be undone! (y/n): ")
            if (confirm.lower() == "y" or confirm.lower() == "yes"):
                output, status_code = laml_app_func(query_params, req_type="DELETE")
                valid = validate_http(status_code)
                if valid:
                    print("Success! LaML App " + sid + " Removed\n")
                else:
                    is_json = validate_json(output)
                    if is_json:
                        print_error_json_compatibility(output)
                    else:
                        status_code = str(status_code)
                        print ( status_code + ": " + output + "\n" )
            else:
                print ("OK. Cancelling.")
        else:
            print ("ERROR: An error has occurred")

    # Set default handlers for each sub command
    laml_app_parser_list.set_defaults(func=laml_app_list)
    laml_app_parser_create.set_defaults(func=laml_app_create)
    laml_app_parser_update.set_defaults(func=laml_app_update)
    laml_app_parser_delete.set_defaults(func=laml_app_delete)

    @cmd2.with_argparser(base_laml_app_parser)
    def do_laml_app(self, args: argparse.Namespace):
        '''List, Create, Update, or Delete domain applications'''
        func = getattr(args, 'func', None)
        if func is not None:
            func(self, args)
        else:
            self.do_help('laml_app')


## DOMAIN APPLICATIONS ##
    # Create the top level parser for domain application: domain_application
    base_domain_application_parser = cmd2.Cmd2ArgumentParser()
    base_domain_application_subparsers = base_domain_application_parser.add_subparsers(title='subcommands',help='subcommand help') # TODO: Fix help text

    # create the domain application list subcommand
    domain_application_parser_list = base_domain_application_subparsers.add_parser('list', help='List Domain Applications for the Project')
    domain_application_parser_list.add_argument('-d', '--domain', type=str, nargs='+', help='Return all values for given domain of Domain App')
    domain_application_parser_list.add_argument('-n', '--name', type=str, nargs='+', help='Return all values for the given name of Domain App')
    domain_application_parser_list.add_argument('-i', '--id', help='SignalWire ID of the Domain Application')

    # create the domain application create command
    domain_application_parser_create = base_domain_application_subparsers.add_parser('create', help='List Domain Applications for the Project')
    domain_application_parser_create.add_argument('-n', '--name',  nargs='+', help='Friendly name for the domain application', required=True)
    domain_application_parser_create.add_argument('--identifier', help='Identifier of the domain.  Must be unique accross the project.', required=True)
    domain_application_parser_create.add_argument('--ip-auth-enabled',  help='Whether the domain application will enforce IP authentication (Boolean)', choices=['true','false'] )
    domain_application_parser_create.add_argument('--ip-auth', nargs='+',  help='A List of whitelisted / allowed IPs when --ip-auth-enabled is true ' )
    domain_application_parser_create.add_argument('--call-handler', help='How the domain Application handles calls', choices=['relay_context','laml_webhooks','laml_application','video_room'], required=True )
    domain_application_parser_create.add_argument('--call-request-url', help='The LaML URL to access when a call is received.  This is only used with laml_webhooks call handler')
    domain_application_parser_create.add_argument('--call-request-method', help='The HTTP method to use with call_request_url', choices=["POST", "GET"], default="POST")
    domain_application_parser_create.add_argument('--call-fallback-url', help='The LaML URL to access when call_request_url fails')
    domain_application_parser_create.add_argument('--call-fallback-method', help='The HTTP method to use with call_call_back_url', choices=["POST", "GET"], default="POST")
    domain_application_parser_create.add_argument('--call-status-callback-url', help='The URL to send status change messages to. This is only sed when call_hander is set to laml_webhooks')
    domain_application_parser_create.add_argument('--call-status-callback-method', help='The HTTP method to use with call_status_callback_url', choices=["POST", "GET"], default="POST")
    domain_application_parser_create.add_argument('--call-relay-context', help='Relay context to forward incoming calls to.  This is only used when call_handler is set to relay_context')
    domain_application_parser_create.add_argument('--call-laml-application-id', help='The ID of the LaML application to forward incoming calls to.  this is only used when call_handler is set to laml_application')
    domain_application_parser_create.add_argument('--call-video-room-id', help='The ID of the Video Room to forward incoming calls to.  This is only used when call_handler is set to video_room')
    domain_application_parser_create.add_argument('-e', '--encryption', type=str, help='Default Codecs', choices=['default', 'required', 'optional'])
    domain_application_parser_create.add_argument('--codecs', type=str, nargs='+', help='Default Codecs', choices=['OPUS', 'G722', 'PCMU', 'PCMA', 'VP8', 'H264'])
    domain_application_parser_create.add_argument('--ciphers', type=str, nargs='+',  help='Default Ciphers', choices=['AEAD_AES_256_GCM_8','AES_256_CM_HMAC_SHA1_80','AES_CM_128_HMAC_SHA1_80','AES_256_CM_HMAC_SHA1_32','AES_CM_128_HMAC_SHA1_32'])

    # create the domain application update command
    domain_application_parser_update = base_domain_application_subparsers.add_parser('update', help='List Domain Applications for the Project')
    domain_application_parser_update.add_argument('-i', '--id', help='ID of the Domain Application to be updated', required=True)
    domain_application_parser_update.add_argument('-n', '--name',  nargs='+', help='Friendly name for the domain application')
    domain_application_parser_update.add_argument('--identifier', help='Identifier of the domain.  Must be unique accross the project.')
    domain_application_parser_update.add_argument('--ip-auth-enabled',  help='Whether the domain application will enforce IP authentication (Boolean)', choices=['true','false'] )
    domain_application_parser_update.add_argument('--ip-auth', nargs='+',  help='A List of whitelisted / allowed IPs when --ip-auth-enabled is true ' )
    domain_application_parser_update.add_argument('--call-handler', help='How the domain Application handles calls', choices=['relay_context','laml_webhooks','laml_application','video_room'] )
    domain_application_parser_update.add_argument('--call-request-url', help='The LaML URL to access when a call is received.  This is only used with laml_webhooks call handler')
    domain_application_parser_update.add_argument('--call-request-method', help='The HTTP method to use with call_request_url', choices=["POST", "GET"], default="POST")
    domain_application_parser_update.add_argument('--call-fallback-url', help='The LaML URL to access when call_request_url fails')
    domain_application_parser_update.add_argument('--call-fallback-method', help='The HTTP method to use with call_call_back_url', choices=["POST", "GET"], default="POST")
    domain_application_parser_update.add_argument('--call-status-callback-url', help='The URL to send status change messages to. This is only sed when call_hander is set to laml_webhooks')
    domain_application_parser_update.add_argument('--call-status-callback-method', help='The HTTP method to use with call_status_callback_url', choices=["POST", "GET"], default="POST")
    domain_application_parser_update.add_argument('--call-relay-context', help='Relay context to forward incoming calls to.  This is only used when call_handler is set to relay_context')
    domain_application_parser_update.add_argument('--call-laml-application-id', help='The ID of the LaML application to forward incoming calls to.  this is only used when call_handler is set to laml_application')
    domain_application_parser_update.add_argument('--call-video-room-id', help='The ID of the Video Room to forward incoming calls to.  This is only used when call_handler is set to video_room')
    domain_application_parser_update.add_argument('-e', '--encryption', type=str, help='Default Codecs', choices=['default', 'required', 'optional'])
    domain_application_parser_update.add_argument('--codecs', type=str, nargs='+', help='Default Codecs', choices=['OPUS', 'G722', 'PCMU', 'PCMA', 'VP8', 'H264'])
    domain_application_parser_update.add_argument('--ciphers', type=str, nargs='+',  help='Default Ciphers', choices=['AEAD_AES_256_GCM_8','AES_256_CM_HMAC_SHA1_80','AES_CM_128_HMAC_SHA1_80','AES_256_CM_HMAC_SHA1_32','AES_CM_128_HMAC_SHA1_32'])

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
        elif args.id:
            sid = args.id
            query_params = "/" + sid
        else:
            # Will list all Domain Applications
            query_params=""

        # When retrieving just an ID, there is no data json object
        output, status_code = domain_application_func(query_params)
        valid = validate_http(status_code)
        if valid:
            output_json = json.loads(output)
            if args.id:
                json_nice_print (output_json)
            else:
                data_json = output_json["data"]
                json_nice_print (data_json)

    def domain_application_create(self, args):
        '''create subcommand of domain_application'''
        # Make the Name look nice
        if args.name:
            args.name = ' '.join(args.name)
        domain_application_dictionary = {
           "name": args.name,
           "identifier": args.identifier,
           "ip_auth_enabled": args.ip_auth_enabled,
           "ip_auth": args.ip_auth,
           "call_handler": args.call_handler,
           "call_request_url": args.call_request_url,
           "call_request_method": args.call_request_method,
           "call_fallback_url": args.call_fallback_url,
           "call_fallback_method": args.call_fallback_method,
           "call_status_callback_url": args.call_status_callback_url,
           "call_status_callback_method": args.call_status_callback_method,
           "call_relay_context": args.call_relay_context,
           "call_laml_application_id": args.call_laml_application_id,
           "call_video_room_id": args.call_video_room_id,
           "encryption": args.encryption,
           "codecs": args.codecs,
           "ciphers": args.ciphers
        }

        create_domain_application_dictionary = {}
        for x, y in domain_application_dictionary.items():
            if y is not None:
                create_domain_application_dictionary[x] = y

        payload = json.dumps(create_domain_application_dictionary)
        output, status_code = domain_application_func(req_type="POST", payload=payload)
        valid = validate_http(status_code)
        if valid:
            # Grab the SID of the new domain app and output for user
            output_json = json.loads(output)
            endpoint_id = output_json["id"]
            print("Domain Application created with ID: " + endpoint_id)
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                print(status_code + ": " + output + "\n")

    def domain_application_update(self, args):
        '''create subcommand of domain_application'''
        sid = args.id
        query_params = "/" + sid
        # Make the Name look nice
        if args.name:
            print(args.name)
            args.name = ' '.join(args.name)
        domain_application_dictionary = {
           "name": args.name,
           "identifier": args.identifier,
           "ip_auth_enabled": args.ip_auth_enabled,
           "ip_auth": args.ip_auth,
           "call_handler": args.call_handler,
           "call_request_url": args.call_request_url,
           "call_request_method": args.call_request_method,
           "call_fallback_url": args.call_fallback_url,
           "call_fallback_method": args.call_fallback_method,
           "call_status_callback_url": args.call_status_callback_url,
           "call_status_callback_method": args.call_status_callback_method,
           "call_relay_context": args.call_relay_context,
           "call_laml_application_id": args.call_laml_application_id,
           "call_video_room_id": args.call_video_room_id,
           "encryption": args.encryption,
           "codecs": args.codecs,
           "ciphers": args.ciphers
        }

        update_domain_application_dictionary = {}
        for x, y in domain_application_dictionary.items():
            if y is not None:
                update_domain_application_dictionary[x] = y

        payload = json.dumps(update_domain_application_dictionary)
        output, status_code = domain_application_func(query_params, req_type="PUT", payload=payload)
        valid = validate_http(status_code)
        if valid:
            print("Domain Application, " + sid + " has been udpated.\n")
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                print(status_code + ": " + outpout + "\n")

    def domain_application_delete(self, args):
        '''delete subcommand of domain_application'''
        sid = args.id
        query_params = "/" + sid
        if sid is not None:
            confirm = input("Remove Domain Application " + sid + "? This cannot be undone! (y/n): " )
            if (confirm == "Y" or confirm == "y"):
                output, status_code = domain_application_func(query_params, req_type="DELETE")
                valid = validate_http(status_code)
                if valid:
                    print("Success! Domain Application " + sid + " Removed\n")
                else:
                    is_json = validate_json(output)
                    if is_json:
                        print_error_json(output)
                    else:
                        print (status_code + ": " + output + "\n")
            else:
                print ("Aborting.")
        else:
            print ("ERROR")

    # Set default handlers for each sub command
    domain_application_parser_list.set_defaults(func=domain_application_list)
    domain_application_parser_create.set_defaults(func=domain_application_create)
    domain_application_parser_update.set_defaults(func=domain_application_update)
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

        output, status_code = number_group_func( query_params )
        valid = validate_http(status_code)
        if valid:
            output_json = json.loads(output)
            # if only ID is used, there is no data object.
            if args.id:
                json_nice_print (output_json)
            else:
                data_json = output_json["data"]
                json_nice_print (data_json)
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                print ("Error: " + output + "\n")

    def number_group_create(self, args):
        '''create subcommand of number_group'''
        number_group_dictionary = {
          "name": args.name,
          "sticky_sender": args.sticky_sender
        }

        payload = json.dumps(number_group_dictionary)
        output, status_code = number_group_func(req_type="POST", payload=payload)
        valid = validate_http(status_code)
        if valid:
            output_json = json.loads(output)
            print (output_json)
            endpoint_id = output_json["id"]
            print("Number group created with ID: " + endpoint_id + "\n")
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                print (status_code + ": " + output + "\n")

    def number_group_update(self, args):
        '''update subcommand of number_group'''
        sid = args.id
        query_params = "/" + sid
        number_group_dictionary = {
          "name": args.name,
          "sticky_sender": args.sticky_sender
        }

        update_number_group_dictionary = {}
        for x, y in number_group_dictionary.items():
            if y is not None:
              update_number_group_dictionary[x] = y

        payload = json.dumps(update_number_group_dictionary)
        output, status_code = number_group_func(query_params, req_type="PUT", payload=payload)
        valid = validate_http(status_code)
        if valid:
            # TODO: Output the sip endpoint after updated.  Maybe?
            print("Success! Number group " + sid + " Updated\n")
        else:
            is_json = validate_json(output)
            if is_json:
                print_error_json(output)
            else:
                print (status_code + ": " + output + "\n" )

    def number_group_delete(self, args):
        '''delete subcommand of number_group'''
        sid = args.id
        query_params = "/" + sid
        if sid is not None:
            confirm = input("Remove Number Group " + sid + "? This cannot be undone! (y/n): " )
            if (confirm == "Y" or confirm == "y"):
                output, status_code = number_group_func(query_params, req_type="DELETE")
                valid = validate_http(status_code)
                if valid:
                    print("Success! Number Group " + sid + " Removed\n")
                else:
                    is_json = validate_json(output)
                    if is_json:
                        print_error_json(output)
                    else:
                        status_code = str(status_code)
                        print ( status_code + ": " + output + "\n" )
            else:
                print ("OK. Cancelling")
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
        # TODO: Move this into the functions file
        signalwire_space, project_id, rest_api_token = get_environment()
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