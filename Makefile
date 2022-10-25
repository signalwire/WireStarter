build: 
	@./setup.sh
	@./docker-dev build

up: build
	./docker-dev up -d

up: build 

all: build up

down:
	@./docker-dev down

prune:
	@docker system prune -a

enter:
	docker exec -it wirestarter /bin/bash

restart: down up
