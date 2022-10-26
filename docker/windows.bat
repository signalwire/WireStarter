@echo off

title ~#~#~#~#~#~#~Swish~#~#~#~#~#~#~
:start

if exist .env ( 
REM echo "Remove .env to run again. Press the key to exit. Yes, that one."
 pause  exit
) else (

set /p sig_space="What is your Signalwire space "
set /p proj_id="What is your Signalwire Project ID "
set /p api_token="What is your Signalwire REST API token "
set /p ngrok_token="What is your NGROK Token "
set /p visual_editor="What editor to use? nano, vim, emacs "
set /p localtonet_api_token="What is your localtonet API Token "
set /p localtonet_tunnel_token="What is your localtonet Tunnel Token "

echo SIGNALWIRE_SPACE=%sig_space%> .env
echo PROJECT_ID=%proj_id%>> .env
echo REST_API_TOKEN=%api_token%>> .env
echo NGROK_TOKEN=%ngrok_token%>> .env
echo VISUAL=%visual_editor%>> .env
echo LOCALTONET_API_TOKEN=%localtonet_api_token%>> .env
echo LOCALTONET_TUNNEL_TOKEN=%localtonet_api_token%>> .env

REM CD docker
docker network create --attachable wirestarter --subnet 172.50.0.1/24
docker compose up -d

)
