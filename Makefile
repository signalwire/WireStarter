build: 
	@docker build --no-cache -f Dockerfile .

up:
	@docker run -it -d --rm --name wirestarter --env-file .env --volume "${WORKDIR}:/workdir" --volume opt:/opt  briankwest/wirestarter /start_services.sh || echo "up"

down:
	@docker stop wirestarter || echo "down"

prune:
	@docker system prune -a || echo "no prune"

enter:
	@docker exec -it wirestarter /bin/bash || echo "no enter"

tag:
	@docker tag briankwest/wirestarter:latest briankwest/wirestarter:latest 

push: tag
	@docker buildx build -f Dockerfile --platform linux/amd64,linux/arm64 --push .

clean: down prune
