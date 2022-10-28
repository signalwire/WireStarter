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

## BUILDING on MacOS and Linux ##
* make up
* make enter or docker exec -ti wirestarter bash

## INSTALLATION ##

 ### On Windows:

Prerequisites

* Docker Desktop: https://docs.docker.com/desktop/install/windows-install/
* Github Desktop: https://desktop.github.com/
* NGROK account AND token: https://ngrok.com/
* [Create a localtonet account for API and AUTH tokens](https://localtonet.com/Identity/Account/Register?returnUrl=%2F)
  
1. Open Github Desktop
2. Clone repo
3. Top menu click Repository > Open in Command Prompt
4. Start docker Desktop
5. .\setup.ps1

Note: If `.\setup.ps1` give an error and won't run, more steps are needed.

- `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- [More information on ExecutionPolicy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2#powershell-execution-policies)

### On Mac OSX or Linux:
 1.  git pull
 2.  make up

That's it!  The container will build in the background and then start by itself placing the user in the SWiSH 
shell.
