build:
	docker build --build-arg PROJECT_ID=${PROJECT_ID} \
	--build-arg REST_API_TOKEN=${REST_API_TOKEN} \
	-t python-example .

run:
	docker run -d python-example

up: build run

all: build run 
