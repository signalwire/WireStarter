# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WireStarter is a Docker-based development environment for building SignalWire applications. It provides a containerized workspace with pre-installed tools, SDKs, and AI Agent demo templates for rapid SignalWire development.

## Common Commands

### Container Management (from host machine)
```bash
make up       # Build and start container (detached, uses .env and WORKDIR volume)
make down     # Stop container
make enter    # Enter running container shell
make build    # Rebuild Docker image (no cache)
make debug    # Run container interactively (foreground)
make push     # Build and push multi-arch image to Docker Hub
make clean    # Stop container and prune Docker system
```

### Inside Container
```bash
setup         # Interactive environment setup menu
swsh          # SignalWire Shell - interactive CLI for SignalWire API
up            # Run app.py in infinite loop (auto-restart on exit)
venv init     # Create and activate Python virtual environment
venv delete   # Remove Python virtual environment
ngrok_url     # Get current NGROK public URL
```

## Architecture

### Directory Structure
- `bin/` - Utility scripts
  - `setup` - Interactive environment setup menu
  - `python.d/`, `nodejs.d/`, `perl.d/` - Language-specific AI Agent demo installers
  - `setupgolang`, `setupnvm`, `setuppgsql` - Environment setup scripts
- `misc/` - Container configuration files
  - `bash.rc` - Container shell configuration with SignalWire credential validation
  - `start_services.sh` - Container entrypoint (starts ngrok, redis, nginx)
- `conf/` - Service configurations (nginx)

### Container Runtime
The container runs these services on startup:
1. NGROK tunnel on port 9080 (if NGROK_TOKEN set)
2. Redis server
3. Nginx (serves `/workdir/public` at `$NGROK_URL/public`)

### Volume Mounting
- Host `$WORKDIR` directory mounts to `/workdir` in container
- Place persistent files (`.env`, `.bashrc`, `.ssh`, code) in WORKDIR
- The container automatically sources `/workdir/.env` and `/workdir/.bashrc`

### Environment Variables
Required in `.env` (see `env.example`):
- `SIGNALWIRE_SPACE_NAME` - SignalWire space name (without .signalwire.com)
- `SIGNALWIRE_PROJECT_ID` - SignalWire project ID
- `SIGNALWIRE_TOKEN` - SignalWire API token
- `NGROK_TOKEN` - NGROK auth token (optional but recommended)
- `WORKDIR` - Host directory to mount as /workdir

### Python Environment
- Python 3.11 with venv support
- Pre-installed packages: signalwire, signalwire-agents, signalwire-swml, signalwire-swaig, flask
- Use `venv init` to create project-specific virtual environments
- The shell auto-activates venv when entering directories containing one
