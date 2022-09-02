#!/usr/bin/env python3
from signalwire.voice_response import *
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

response = VoiceResponse()

## Option 1: Record a message
if POST['Digits'] == '1':
  #response.record()

  ## TODO:  Play with transcribe
  response.record(transcribe=True, transcribe_callback='handle_transcribe.py',finishOnKey='#')
  ## SignalWire will record the caller and transcribe the recording once it is complete. Then, SignalWire will make a POST request to the transcribecallback url with the transcription as a parameter

## Option 2: Read caller ID back to the caller
elif POST['Digits'] == '2':
  # Strip the URL encoded '+' symbol and prepended 1
  callingnum = POST['From'].strip('%2B1')
  callingnum = " ".join(callingnum)

  # NOTE: There is a way for the Say verb to read as a telephone number.  Can't figure out the syntax in say though.
  # HACK: adding a space in between each character in the telephone number.
  response.say("Your calling number is " + callingnum)

## Option 2: Forward to my mobile phone
elif POST['Digits'] == '3':
  # TODO: Make interactive to forward to any number

  dial = Dial(caller_id='+12085170069')
  dial.number('+14403346366')
  response.append(dial)

elif POST['Digits'] == '4':
  # Try a conference
  dial = Dial()
  dial.conference('Room - Shane')
  response.append(dial)

#elif POST['Digits'] == '5':
#  # Play a random audio file
   # Need mp3 files

else:
  response.say("That is not a valid option")


print('Content-Type: text/plain')
print('')
print (response)