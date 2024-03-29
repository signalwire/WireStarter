# WireStarter Documentation

![Screenshot of WireStarter](https://raw.githubusercontent.com/signalwire/WireStarter/master/misc/ws.png)

## Prerequisites
Before you begin, ensure you have the following prerequisites:

- A Signalwire [Account](https://signalwire.com/signup)
- A Signalwire [API Credentials](https://developer.signalwire.com/guides/your-first-api-calls/)
- Docker Desktop
  - [Install on MacOS](https://docs.docker.com/desktop/install/mac-install/)
  - [Install on Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Install on Linux](https://docs.docker.com/desktop/install/linux-install/)

- An NGROK account and token. NGROK is optional but recommended for tunneling into the WireStarter container. 
  - [Sign up for NGROK](https://ngrok.com)

## Installation

### Windows:

#### Prerequisites
- Docker Desktop: [Download and Install](https://docs.docker.com/desktop/install/windows-install/)
- GitHub Desktop: [Download and Install](https://desktop.github.com/)
- NGROK Account and Token: [Sign Up](https://ngrok.com)

#### Steps:
1. Launch Docker Desktop.
2. Open GitHub Desktop.
3. Clone the repository.
4. In GitHub Desktop, navigate to `Repository` > `Open in Command Prompt`.
5. Install Git if prompted.
6. Run the `windows-start.bat` script



### Linux quick start bash script

- `Start-WireStarter.sh` is an optional automated option to launch WireStarter in Linux
- How to use Start-WireStater.sh:
```
chmod +x Start-WireStater.sh
./Start-WireStater.sh
```

### Mac OSX or Linux:

#### Steps:
1. Pull the repository: `git pull`.
2. Build and start the container: `make up`.
3. Enter the container: `make enter` or `docker exec -ti wirestarter bash`.

After starting, the container will build in the background and automatically place you in the SWiSH shell.

### Features and Utilities

The following features and utilities are available if they exist in `/workdir`:

1. Source environment variables: `. /workdir/.env`.
2. Source bash configurations: `. /workdir/.bashrc`.
3. Link Emacs configuration: `ln -f -s /workdir/.emacs ~/.emacs`.
4. Link Git configuration: `ln -f -s /workdir/.gitconfig ~`.
5. Link SSH configuration: `ln -f -s /workdir/.ssh ~`.
6. Copy GitHub Copilot configuration: `cp -drp /workdir/github-copilot ~/.config/`.
7. Install Perl dependencies: `cpanm --installdeps /workdir/` if `/workdir/cpanfile` exists.
8. Set up Go and Node Version Manager: `setupgolang` and `setupnvm` for persistent environments in `/opt`, which will be its own volume.

For more information, visit the [WireStarter GitHub repository](https://github.com/signalwire/WireStarter).

### SignalWire Digital Employee

WireStarter also has the capability to setup and run pre-made AI Agent demo's.
To install and run an AI Agent:
1. Type exit or ctrl+d to go back to exit the `swsh` command line
2. Then type `setup.sh`
3. Choose a language to work with
4. Select the Ai Agent to install.

![image](https://github.com/signalwire/WireStarter/assets/13131198/43fc9ff8-e99e-48cd-9d4b-3780b3030360)

`*Please note each language has different AI Agents*`
