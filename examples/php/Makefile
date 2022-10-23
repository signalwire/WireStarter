build:
	docker build --build-arg PROJECT_ID=${PROJECT_ID} \
	--build-arg REST_API_TOKEN=${REST_API_TOKEN} \
	-t php-example .

run:
	docker run -d php-example

up: build run

all: build run 
