require 'bundler'
Bundler.require
Envyable.load('./config/env.yml')

require './app'
run FaxApp
