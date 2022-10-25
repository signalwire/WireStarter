@echo off

title ~#~#~#~#~#~#~Swish~#~#~#~#~#~#~
:start

if exist .env ( 
 echo "Remove .env to run again. Press the only key to exit"
 pause  exit
) else (

set /p sig_space="What is your Signalwire space "
set /p proj_id= "What is your Signalwire project ID "
set /p api_token= "What is your Signalwire REST API token "
set /p ngrok_token= "What is your NGROK Token "
set /p visual_editor= "What editor to use? nano, vim, emacs "
set /p localtonet_api_token= "What is localtonet api Token "

echo SIGNALWIRE_SPACE=%sig_space% > .env
echo PROJECT_ID=%proj_id% >> .env
echo REST_API_TOKEN=%proj_id% >> .env
echo NGROK_TOKEN=%ngrok_token% >> .env
echo VISUAL=%visual_editor% >> .env
echo LOCALTONET_API_TOKEN=%localtonet_api_token% >> .env


REM docker "run" "-it" "wirestarter"

)
