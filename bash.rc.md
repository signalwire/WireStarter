# Bash Configuration File Documentation

This document provides an overview of the features and configurations set in the `bash.rc` file. This file is used to customize the shell environment, set up environment variables, and define functions and aliases for ease of use.

## Environment Variables

- **PROMPT_COMMAND**: Customizes the shell prompt to display memory usage and system load averages.
- **PS1**: Sets the primary prompt string to include process IDs, job count, command history number, time, date, user, host, and working directory.
- **ENV_FILE**: Specifies the path to the environment file (`/workdir/.env`).

## SignalWire Configuration

- **SW_TEST_URL**: Constructs a URL for testing SignalWire credentials.
- **response_code**: Captures the HTTP response code from the SignalWire API to verify credentials.

## SignalWire Credential Verification

- Checks the response code from the SignalWire API:
  - `200`: Credentials are valid.
  - `404`: SignalWire space not found; deletes the `.env` file.
  - `401`: Invalid credentials; deletes the `.env` file.
  - Other: Indicates incomplete setup; deletes the `.env` file.

## Environment Setup

- Prompts the user for SignalWire and NGROK credentials if the `.env` file is missing.
- Uses `whiptail` to collect user inputs for various credentials and settings.
- Writes collected inputs to the `.env` file and sources it.

## NGROK Setup

- Starts an NGROK tunnel if the NGROK token is provided.
- Retrieves and exports the public URL of the NGROK tunnel.

## Welcome Message

- Displays a welcome message and NGROK tunnel information if available.

## File and Directory Management

- Sources additional configuration files if they exist in `/workdir`.
- Creates symbolic links for configuration files like `.emacs`, `.gitconfig`, `.pypirc`, and `.ssh`.
- Executes a PostgreSQL setup script if available.

## PostgreSQL Setup

- **/usr/bin/setuppgsql**: Moves the PostgreSQL database to `/workdir` to ensure data persistence and proper configuration.

## GitHub Copilot

- Copies GitHub Copilot configuration to the user's config directory if present.

## Perl Library Setup

- Installs Perl dependencies specified in `cpanfile` and updates the `PATH` and `PERL5LIB`.

## Aliases

- Defines common typos for `emacs` to ensure the correct command is executed.
- Defines an alias `ngrok_url` to fetch the current NGROK public URL.

## Node Version Manager (NVM)

- Sets up the environment for NVM if the script is available.

## Go Language Setup

- Updates the `PATH` for Go binaries if Go is installed.

## Default Editor

- Sets the default visual editor to `vim` if not already set.

## PATH Updates

- Extends the `PATH` to include directories for Node.js, Perl, and Python binaries.

## SignalWire Shell (swsh)

- Executes a SignalWire shell script if all necessary credentials are available and a specific file is not present.

## Functions

### `cd()`

- Overrides the default `cd` command to automatically activate or deactivate Python virtual environments based on the presence of a `venv` directory.

### `venv()`

- Manages Python virtual environments:
  - `init`: Creates or activates a virtual environment in the current directory.
  - `delete`: Deletes the virtual environment if it exists.

### `up()`

- Runs `app.py` in an infinite loop, restarting it after a 1-second delay if it exits.

---
