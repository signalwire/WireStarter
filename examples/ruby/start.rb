require "signalwire"

class MyConsumer < Signalwire::Relay::Consumer
 contexts ['home','office']

 def on_incoming_call(call)
  call.answer
  call.play_tts 'Welcome to SignalWire!'
  call.hangup
 end
end

MyConsumer.new(project: ENV['PROJECT_ID'], token: ENV['REST_API_TOKEN']).run
