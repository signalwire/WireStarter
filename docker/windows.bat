@echo off

title ~#~#~#~#~#~#~Swish~#~#~#~#~#~#~
:start
set /p sig_space="What is your Signalwire space "

set /p proj_id= "What is your Signalwire project ID "
set /p api_token= "What is your Signalwire REST API token "
set /p ngrok_token= "What is your NGROK Token "



REM build:


docker build --build-arg SIGNALWIRE_SPACE=%sig_space% --build-arg PROJECT_ID=%proj_id% --build-arg REST_API_TOKEN=%api_token% --build-arg NGROK_TOKEN=%ngrok_token% -t signalwire-getting-started  -f Dockerfile .

REM run:

docker "run" "-it" "signalwire-getting-started"

REM up: "build" "run"

REM all: "build" "run"
