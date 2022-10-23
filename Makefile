build: 
	@./setup.sh
	@./docker-dev build

run: build
	@docker run -it wirestarter

up: build run

all: build run 
