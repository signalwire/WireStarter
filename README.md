# WireStarter

![WireStarter Screenshot](https://raw.githubusercontent.com/signalwire/WireStarter/master/misc/ws.png)

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
 
## INSTALLATION ##

 ### On Windows:

Prerequisites

* Docker Desktop: https://docs.docker.com/desktop/install/windows-install/
* Github Desktop: https://desktop.github.com/
* NGROK account AND token: https://ngrok.com/
  
1. Start docker Desktop
2. Open Github Desktop
3. Clone repo
4. Top menu in Github Desktop click Repository > Open in Command Prompt
5. Install Git if prompted.
6. powershell Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
7. powershell .\setup.ps1

Note: If `.\setup.ps1` give an error and won't run, more steps are needed.

- `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- [More information on ExecutionPolicy](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2#powershell-execution-policies)

### On Mac OSX or Linux:
 1.  git pull
 2.  make up
 3.  make enter or docker exec -ti wirestarter bash

That's it!  The container will build in the background and then start by itself placing the user in the SWiSH 
shell.
