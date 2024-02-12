# WireStarter Documentation

![Screenshot of WireStarter](https://raw.githubusercontent.com/signalwire/WireStarter/master/misc/ws.png)

## Prerequisites
Before you begin, ensure you have the following prerequisites:

- A Signalwire Account
- A Signalwire Space and Project
- Docker Desktop
  - [Install on MacOS](https://docs.docker.com/desktop/install/mac-install/)
  - [Install on Windows](https://docs.docker.com/desktop/install/windows-install/)
  - [Install on Linux](https://docs.docker.com/desktop/install/linux-install/)

**Note:** A Docker account is required to use Docker Compose.

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
6. Execute in PowerShell: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.
7. Run the setup script: `.\setup.ps1`.

**Note:** If `.\setup.ps1` encounters an error, ensure the execution policy is set correctly:

- `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- [More on Execution Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2#powershell-execution-policies)

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
