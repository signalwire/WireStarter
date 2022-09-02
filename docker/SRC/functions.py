#!/usr/bin/env python3
import base64
import requests

def encode_auth(project_id, rest_api_token):
    auth = str(project_id + ":" + rest_api_token)
    auth_bytes = auth.encode('ascii')
    base64_auth_bytes = base64.b64encode(auth_bytes)
    base64_auth = base64_auth_bytes.decode('ascii')

    return base64_auth



def http_request(signalwire_space, project_id, rest_api_token, destination, req_type, payload={}, headers={}):
    http_basic_auth = str(encode_auth(project_id, rest_api_token))

    url = 'https://%s.signalwire.com/api/relay/rest/' % signalwire_space

    # This seems Janky, but I'm going with it.
    # If no other set of headers are being passed in.  Set to default
    if len(headers) == 0:
        headers = {
          'Accept': 'applications/json',
          'Authorization': 'Basic %s' % http_basic_auth
        }

    fqdn = str(url + destination)
    response = requests.request(req_type, fqdn, headers=headers, data=payload)

    return (response)
