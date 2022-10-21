from signalwire.relay.consumer import Consumer
import os
from dotenv import load_dotenv

class CustomConsumer(Consumer):
 def setup(self):
  self.project = os.getenv('PROJECT_ID')
  self.token = os.getenv('API_TOKEN')
  self.contexts = ['home', 'office']

 async def ready(self):
   # Consumer is successfully connected with Relay.
   # You can make calls or send messages here..
  print('Relay Consumner Ready')
 async def on_incoming_call(self, call):
  result = await call.answer()
  if result.successful:
   print('Call answered..')
   result = await call.play_tts(text='Welcome to SignalWire!', gender='male')
   await call.hangup()
# Run your consumer..
consumer = CustomConsumer()
consumer.run()
