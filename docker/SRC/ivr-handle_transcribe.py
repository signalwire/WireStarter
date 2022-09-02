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

transcription = POST['TranscriptionText'].replace("+"," ")
# TODO: Clean up the transcription text.  This is just a proof of concept currently.

response = VoiceResponse()
response.say(transcription)

print('Content-Type: text/plain')
print('')
print (response)


original_stdout = sys.stdout
with open('/tmp/logfile.txt','w') as l:
  sys.stdout = l
  print (response)
  sys.stdout = original_stdout