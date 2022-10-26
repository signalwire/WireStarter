#!/bin/bash
# TODO: Validate input and test on each build that it still works (prevents support cases)

if [ ! -f ".env" ]; then
   read -p "What is your Signalwire space: " sig_space;
   read -p "What is your Signalwire project ID: " proj_id;
   read -p "What is your Signalwire REST API token: " api_token;
   read -p "What is your NGROK Token: " ngrok_token;
   read -p "What is your LocaltoNet API TOKEN: " localtonet_api_token;
   read -p "What is your LocaltoNet AUTH TOKEN: " localtonet_auth_token;
   read -p "What is your Work Dir: " workdir;
   read -p "Editor (nano, vim, emacs): " visual;

   URL="https://${sig_space}.signalwire.com/api/laml/2010-04-01/Accounts -u ${proj_id}:${api_token}"
   response_code=$(curl -s -o /dev/null -I -w "%{http_code}" $URL )
   if [[ $response_code  -eq 200 ]]; then
      echo "SIGNALWIRE_SPACE=$sig_space" > .env
      echo "PROJECT_ID=$proj_id" >> .env
      echo "REST_API_TOKEN=$api_token" >> .env
      echo "NGROK_TOKEN=$ngrok_token" >> .env
      echo "VISUAL=$visual" >> .env
      echo "LOCALTONET_API_TOKEN=$localtonet_api_token" >> .env
      echo "LOCALTONET_AUTH_TOKEN=$localtonet_auth_token" >> .env
      echo "WORKDIR=$workdir" >> .env
      echo "setup successful"
   elif [[ $response_code -eq 404 ]]; then
      echo "Make sure you entered correct space URL"
   elif [[ $response_code -eq 401 ]]; then
      echo "Make sure you entered correct project ID and RSET API token"
   else
      echo  "Setup failed please try again"
   fi
else
   echo "Setup .env file already exists"
fi
