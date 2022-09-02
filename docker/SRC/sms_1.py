#!/usr/bin/env python3
from signalwire.voice_response import *
from twilio.twiml.messaging_response import Message, MessagingResponse
import os, sys
import json

## Take input from previous script as RAW and format as JSON"
## I found this code, I did not write it.
POST={}
args=sys.stdin.read().split('&')

for arg in args:
    t=arg.split('=')
    if len(t)>1: k, v=arg.split('='); POST[k]=v
######

###
# <Response>
# <Message>Hello from SignalWire!</Message>
# {"MessageSid"=&gt;"0a457f0e-ced3-42b6-9486-77780c128a1f", "SmsSid"=&gt;"0a457f0e-ced3-42b6-9486-77780c128a1f", "AccountSid"=&gt;"0fd6cfc3-ac8c-4b6f-9bc3-57048cf6a7f3", "From"=&gt;"+14403346366", "To"=&gt;"+12085170069", "Body"=&gt;"Hello", "NumMedia"=&gt;"0", "NumSegments"=&gt;"1"}
# </Response>
###

incommingmessage = POST['Body'].replace('+'," ")

response = MessagingResponse()
response.message('Your text said: ' + incommingmessage )

print('Content-Type: text/plain')
print('')
print (response)