SIGNALWIRE_SPACE ?= $(shell bash -c 'read -p "What is your Signalwire space: " sig_space; echo $$sig_space')
PROJECT_ID ?= $(shell bash -c 'read -p "What is your Signalwire project ID: " proj_id; echo $$proj_id')
REST_API_TOKEN ?= $(shell bash -c 'read -p "What is your Signalwire REST API token: " api_token; echo $$api_token')
NGROK_TOKEN ?= $(shell bash -c 'read -p "What is your NGROK Token: " ngrok_token; echo $$ngrok_token')
	

signalwire_docker:
	docker build --no-cache --build-arg SIGNALWIRE_SPACE=$(SIGNALWIRE_SPACE) \
	--build-arg PROJECT_ID=$(PROJECT_ID) \
	--build-arg REST_API_TOKEN=$(REST_API_TOKEN) \
	--build-arg NGROK_TOKEN=$(NGROK_TOKEN) \
	-t signalwire-getting-started ./docker/.

all: signalwire_docker
