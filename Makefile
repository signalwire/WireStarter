build: 
	@./setup.sh
	@./docker-dev build

up: build
	@./docker-dev up -d

up: build 

all: build up

down:
	@./docker-dev down

prune:
	@docker system prune -a

enter: up
	@docker exec -it wirestarter /bin/bash

restart: down up

tag:
	docker tag signalwire/wirestarter:latest briankwest/wirestarter:latest

push:
	docker buildx build -f docker/Dockerfile --platform linux/amd64,linux/arm64 --tag briankwest/wirestarter:latest --push .
