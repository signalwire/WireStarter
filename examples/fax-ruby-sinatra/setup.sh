#!/bin/bash
# TODO: Validate input and test on each build that it still works (prevents support cases)

CONF_DIR=./config
FILES_DIR=./files

if [ ! -f "$CONF_DIR/env.yml" ]; then
   read -p "What is your Signalwire space: " sig_space;
   read -p "What is your Signalwire project ID: " proj_id;
   read -p "What is your Signalwire REST API token: " api_token;
   read -p "What is your Signalwire Number To send Fax: " from_number;
   read -p "What is your NGROK Token (optional): " ngrok_token;
   read -p "What is your LocaltoNet API TOKEN (optional): " localtonet_api_token;
   read -p "What is your LocaltoNet AUTH TOKEN (optional): " localtonet_auth_token;
   read -p "Base URL:" base_url;
   read -p "Editor (nano, vim, emacs): " visual;

   # Remove domain, if attached to signalwire space
   sig_space=$( echo "${sig_space}" | cut -d \. -f1 )

   URL="https://${sig_space}.signalwire.com/api/laml/2010-04-01/Accounts -u ${proj_id}:${api_token}"
   response_code=$(curl -s -o /dev/null -I -w "%{http_code}" $URL )
   if [[ $response_code  -eq 200 ]]; then
      if [ ! -d "$CONF_DIR" ]; then
          mkdir $CONF_DIR
      fi
      echo "SIGNALWIRE_SPACE: '$sig_space'" > $CONF_DIR/env.yml
      echo "PROJECT_ID: '$proj_id'" >> $CONF_DIR/env.yml
      echo "REST_API_TOKEN: '$api_token'" >> $CONF_DIR/env.yml
      echo "FROM_NUMBER: '$from_number'" >> $CONF_DIR/env.yml
      echo "BASE_URL: '$base_url'" >> $CONF_DIR/env.yml
      echo "NGROK_TOKEN: '$ngrok_token'" >> $CONF_DIR/env.yml
      echo "VISUAL: '$visual'" >> $CONF_DIR/env.yml
      echo "LOCALTONET_API_TOKEN: '$localtonet_api_token'" >> $CONF_DIR/env.yml
      echo "LOCALTONET_AUTH_TOKEN: '$localtonet_auth_token'" >> $CONF_DIR/env.yml
      if [ ! -d "$FILES_DIR" ]; then
          mkdir $FILES_DIR
      fi
      echo "setup successful"
   elif [[ $response_code -eq 404 ]]; then
      echo "Make sure you entered correct space URL"
   elif [[ $response_code -eq 401 ]]; then
      echo "Make sure you entered correct project ID and REST API token"
   else
      echo  "Setup failed please try again"
   fi
else
   # This can be changed once .env file validation is happening
   # Search for .signalwire.com and remove if exists
   sed -i~ 's/\.signalwire.com//g' $CONF_DIR/env.yml

   echo "Setup $CONF_DIR/env.yml file already exists"
fi

