PROJECT_ID ?= $(shell bash -c 'read -p "What is your Signalwire project ID: " proj_id; echo $$proj_id')
REST_API_TOKEN ?= $(shell bash -c 'read -p "What is your Signalwire REST API token: " api_token; echo $$api_token')

build:
	docker build --build-arg PROJECT_ID=$(PROJECT_ID) \
	--build-arg REST_API_TOKEN=$(REST_API_TOKEN) \
	-t php-example .

run:
	docker run -d php-example

up: build run

all: build run 
