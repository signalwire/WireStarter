#!/usr/bin/env python3
from signalwire.voice_response import *


## Gather digits and POST to IVR script

response = VoiceResponse()
#gather = Gather(input='dtmf', timeout=5, numDigits=1)
gather = Gather(input='dtmf', timeout=5, numDigits=1, action='ivr-digit_press.py')
gather.say('Welcome to Shanes demo I V R.  Please press 1 to record a message.  Press 2 to have me read back your Caller ID.  Press 3 if you want to talk to Shane on his cell phone')
response.append(gather)

print('Content-Type: text/plain')
print('')
print (response)
