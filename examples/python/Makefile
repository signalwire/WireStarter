PROJECT_ID ?= $(shell bash -c 'read -p "What is your Signalwire project ID: " proj_id; echo $$proj_id')
API_TOKEN ?= $(shell bash -c 'read -p "What is your Signalwire REST API token: " api_token; echo $$api_token')

build:
	docker build --build-arg PROJECT_ID=$(PROJECT_ID) \
	--build-arg API_TOKEN=$(API_TOKEN) \
	-t python-example .

run:
	docker run -d python-example

up: build run

all: build run 
