# WireStarter

Required Prerequisites:
A Signalwire Account

A Signalwire Space and Projects

Docker Desktop
 - MacOS:   https://docs.docker.com/desktop/install/mac-install/
 - Windows: https://docs.docker.com/desktop/install/windows-install/
 - Linux:   https://docs.docker.com/desktop/install/linux-install/

 `NOTE: Docker account required for docker compose`

NGROK account AND token (for tunnel into the WireStarter container, optional)
 - https://ngrok.com
 
Localtonet account
 - https://localtonet.com (needs tunnel auth token and api token, optional)

## BUILDING ##
* cp env.example .env
* edit .env and fill out details
* ./docker-dev build
* ./docker-dev up -d
* docker ps
* docker exec -ti <id> bash

## INSTALLATION ##

 ### On Windows:

Prerequisites

* Docker Desktop: https://docs.docker.com/desktop/install/windows-install/
* Github Desktop: https://desktop.github.com/
* NGROK account AND token: https://ngrok.com/
  
1. Open Github Desktop
2. Clone repo
3. Top menu click Repository > Open in Command Prompt
4. cd docker
5. windows.bat

### On Mac OSX or Linux:
 1.  git pull
 2.  make up

That's it!  The container will build in the background and then start by itself placing the user in the SWiSH 
shell.
