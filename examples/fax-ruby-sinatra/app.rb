# app.py
require 'sinatra/base'
require 'net/http'
require 'uri'
class FaxApp < Sinatra::Base
  get '/' do
    erb :index
  end

  post '/faxes' do
    filename = params[:file][:filename]
    file = params[:file][:tempfile]
    to = params[:number]

    if file
      File.open("./files/#{filename}", 'wb') do |f|
        f.write(file.read)
      end


      uri = URI.parse('https://'+ENV['SIGNALWIRE_SPACE']+'.signalwire.com/api/laml/2010-04-01/Accounts/:AccountSid/Faxes')
      request = Net::HTTP::Post.new(uri)
      request.basic_auth(ENV['PROJECT_ID'], ENV['REST_API_TOKEN'])
      request.set_form_data(
        "From" => ENV['FROM_NUMBER'],
        "To" => to,
        "MediaUrl" => "#{ENV["BASE_URL"]}/faxes/files/#{ERB::Util.url_encode(filename)}",
        "StatusCallback" => "#{ENV["BASE_URL"]}/faxes/status"
      )

      response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: uri.scheme == "https") do |http|
         http.request(request)
      end
    end
    redirect '/'
  end

  get '/faxes/files/:filename' do
    puts params[:filename]
    send_file "./files/#{params[:filename]}"
  end

  post '/faxes/status' do
    puts "===="
    puts "Fax SID:           #{params["FaxSid"]}"
    puts "To:                #{params["To"]}"
    puts "Remote Station ID: #{params["RemoteStationId"]}" if params["RemoteStationId"]
    puts "Status:            #{params["FaxStatus"]}"
    if params["ErrorCode"]
      puts "Error:             #{params["ErrorCode"]}"
       puts params["ErrorMessage"]
    end
    puts "===="
    200
  end
  run! if app_file == $0
end
