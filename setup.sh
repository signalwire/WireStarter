#!/bin/bash
# Ask the user for their name

if [ ! -f ".env" ]; then

read -p "What is your Signalwire space: " sig_space;
read -p "What is your Signalwire project ID: " proj_id;
read -p "What is your Signalwire REST API token: " api_token;
read -p "What is your NGROK Token: " ngrok_token;
read -p "Editor (nano, vim, emacs: " visual;

echo "SIGNALWIRE_SPACE=$sig_space" > .env
echo "PROJECT_ID=$proj_id" >> .env
echo "REST_API_TOKEN=$api_token" >> .env
echo "NGROK_TOKEN=$ngrok_token" >> .env
echo "VISUAL=$visual" >> .env

fi
