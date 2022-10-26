@echo off

title ~#~#~#~#~#~#~Swish~#~#~#~#~#~#~
:start

if exist .env ( 
REM echo Remove .env to setup again
docker ps
docker compose -f docker/docker-compose.yml --env-file .env --project-name wirestarter up -d
docker exec -it wirestarter /bin/bash
) else (

set /p sig_space="What is your Signalwire space "
set /p proj_id="What is your Signalwire Project ID "
set /p api_token="What is your Signalwire REST API token "
set /p ngrok_token="What is your NGROK Token (Optional) "
set /p visual_editor="What editor to use? nano, vim, emacs "
set /p localtonet_api_token="What is your localtonet API Token (Optional) "
set /p localtonet_auth_token="What is your localtonet Tunnel Token (Optional) "
set /p work_dir="Define work directory, C:/SWISH "

echo SIGNALWIRE_SPACE=%sig_space% > .env
echo PROJECT_ID=%proj_id% >> .env
echo REST_API_TOKEN=%api_token% >> .env
echo NGROK_TOKEN=%ngrok_token% >> .env
echo VISUAL=%visual_editor% >> .env
echo LOCALTONET_API_TOKEN=%localtonet_api_token% >> .env
echo LOCALTONET_AUTH_TOKEN=%localtonet_auth_token% >> .env
echo WORKDIR=%work_dir% >> .env

REM CD docker
docker network create --attachable wirestarter --subnet 172.50.0.1/24
docker compose -f docker/docker-compose.yml --env-file .env --project-name wirestarter up -d
docker ps
docker exec -it wirestarter /bin/bash
)
