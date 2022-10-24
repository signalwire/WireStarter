build: 
	@./setup.sh
	@./docker-dev build

run: build
	@./docker-dev up -d

up: build run

all: build run 
