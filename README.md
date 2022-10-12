# signalwire-getting-started

Required Prerequisites:
A Signalwire Account

A Signalwire Space and Projects

Docker Desktop
 - MacOS:   https://docs.docker.com/desktop/install/mac-install/
 - Windows: https://docs.docker.com/desktop/install/windows-install/
 - Linux:   https://docs.docker.com/desktop/install/linux-install/

NGROK account AND token (for tunnel into signalwire-getting-started container)
 - https://ngrok.com


## INSTALLATION ##
On Windows:

Prerequisites

* Docker Desktop: https://docs.docker.com/desktop/install/windows-install/
* Github Desktop: https://desktop.github.com/
  
1. Open Github Desktop
2. Clone repo
3. Top menu click Repository > Open in Command Prompt
4. cd docker
5. docker build -t signalwire-getting-started -f Dockerfile .

On Mac OSX or Linux:
 1.  git pull
 2.  make up

That's it!  The container will build in the background and then start by itself placing the user in the SWiSH 
shell.
