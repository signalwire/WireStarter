@echo off
REM Pull the briankwest/wirestarter Docker image
docker pull briankwest/wirestarter

REM Run a new container named "wirestarter" from the pulled image
docker run -it -d --rm --name wirestarter --env-file .env --volume "C:/SWISH:/workdir" --volume opt:/opt briankwest/wirestarter /start_services.sh || echo "up"

REM Executing a bash shell inside the running "wirestarter" container
docker exec -it wirestarter bash

echo Container "wirestarter" is running and a bash shell has been executed inside it.
pause
