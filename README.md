# WireStarter

A batteries-included Docker development environment for building SignalWire applications.

![Screenshot of WireStarter](https://raw.githubusercontent.com/signalwire/WireStarter/master/misc/ws.png)

## Features

- **Pre-configured SignalWire SDKs** - Python SDK, signalwire-agents, SWML, SWAIG ready to use
- **Automatic ngrok tunneling** - Public URLs for webhook development
- **Persistent storage** - Your code, venvs, and configs survive container rebuilds
- **Interactive setup** - TUI menus for configuring credentials and tools
- **Built-in services** - Redis, nginx, PostgreSQL available on demand
- **AI coding assistants** - Claude Code and Gemini CLI pre-installed
- **Developer tools** - Git, editors (vim/emacs/nano), debugging utilities

## Prerequisites

- [Docker Desktop](https://docs.docker.com/desktop/)
- [SignalWire Account](https://signalwire.com/signup) with [API Credentials](https://developer.signalwire.com/guides/your-first-api-calls/)
- [ngrok Account](https://ngrok.com) (optional but recommended)

## Quick Start

### 1. Clone and configure

```bash
git clone https://github.com/signalwire/WireStarter.git
cd WireStarter
cp env.example .env
```

Edit `.env` with your credentials:

```bash
SIGNALWIRE_SPACE_NAME=yourspace
SIGNALWIRE_PROJECT_ID=your-project-id
SIGNALWIRE_TOKEN=your-api-token
NGROK_TOKEN=your-ngrok-token
WORKDIR=/path/to/your/workspace
```

### 2. Start the container

```bash
make up      # Start in background
make enter   # Enter the container
```

### 3. First run

On first entry, WireStarter validates your SignalWire credentials and drops you into the SignalWire Shell (`swsh`). Type `exit` to access the full bash environment.

## Container Commands

### From your host machine

| Command | Description |
|---------|-------------|
| `make up` | Build and start container (detached) |
| `make down` | Stop container |
| `make enter` | Enter running container |
| `make build` | Rebuild image (no cache) |
| `make debug` | Run container in foreground |
| `make clean` | Stop and prune Docker system |
| `make push` | Build and push multi-arch image |

## Inside the Container

Type `help` for a complete command reference.

### Setup

```bash
setup                 # Interactive environment setup menu
```

The setup menu provides:
- SignalWire & ngrok credentials
- AI API keys (Claude/Gemini)
- Git identity & SSH keys
- Go, NVM/Node.js, PostgreSQL
- Python dev tools
- Audio tools (ffmpeg/sox)

### Python Virtual Environments

Venvs are stored in `/workdir/.venvs/` and persist across container rebuilds.

```bash
venv init             # Create venv for current directory (installs flask, requests, signalwire-agents)
venv delete           # Delete venv for current directory
venv list             # List all venvs
venv nuke             # Delete currently active venv
```

Venvs auto-activate when you `cd` into a directory that has one.

### Project Scaffolding

```bash
newproject myapp      # Create Flask project with venv
newagent mybot        # Create full SignalWire agent project
```

The `newagent` command creates a complete project structure:
- `agents/` - Agent modules with AgentBase patterns
- `skills/` - Reusable skills
- `tests/` - Pytest test scaffolding
- `web/` - Static files
- `.env` - Pre-configured with your SignalWire credentials

### Running Applications

```bash
up                    # Run app.py in loop (auto-restart on crash)
up server.py          # Run specific script
watch                 # Auto-restart on file changes
serve 5000            # Run Flask dev server
```

### SignalWire Tools

```bash
swsh                  # SignalWire Shell - interactive CLI
sw_test               # Test API credentials
sw_numbers            # List phone numbers
swpy                  # Python REPL with SignalWire client loaded
```

### Networking & Debugging

```bash
urls                  # Show ngrok tunnel URLs
tunnel                # Print ngrok URL
testapp               # Test local and public endpoints
webhook               # Start webhook catcher (dumps requests)
logs                  # Tail nginx access log
reqs                  # Formatted request log
```

### Process Management

```bash
ports                 # Show what's running on 5000, 5001, 9080
killport 5000         # Kill process on port
reload                # Reload nginx
```

### Redis

```bash
redis                 # Redis CLI
rkeys                 # List all keys
rget mykey            # Get value
rclear                # Flush all data
```

### Git Shortcuts

```bash
gs                    # git status
gd                    # git diff
gl                    # git log --oneline -20
gp                    # git pull
```

### Navigation

```bash
work                  # cd /workdir
public                # cd /workdir/public
..                    # cd ..
...                   # cd ../..
```

## Architecture

### Services

On startup, WireStarter runs:

1. **ngrok** - Tunnels port 9080 to a public URL
2. **nginx** - Reverse proxy on port 9080
   - `/` → localhost:5000 (your app)
   - `/webhook` → localhost:5002 (webhook catcher)
   - `/public` → /workdir/public (static files)
3. **Redis** - Available on default port

### Persistent Storage

Everything in `/workdir` persists across container rebuilds:

| Path | Purpose |
|------|---------|
| `/workdir/.env` | Environment variables |
| `/workdir/.venvs/` | Python virtual environments |
| `/workdir/.ssh/` | SSH keys |
| `/workdir/.gitconfig` | Git configuration |
| `/workdir/.go/` | Go installation |
| `/workdir/.nvm/` | NVM + Node.js |
| `/workdir/.npm/` | NPM cache |
| `/workdir/.claude/` | Claude Code config |
| `/workdir/.gemini/` | Gemini CLI config |
| `/workdir/postgres/` | PostgreSQL data |
| `/workdir/public/` | Static files (served at ngrok URL) |

### Pre-installed Packages

**System:** git, curl, wget, jq, screen, ffmpeg, sox, sqlite3, ncdu

**Editors:** vim, emacs, nano

**Python:** signalwire, signalwire-agents, signalwire-swml, signalwire-swaig, flask, requests, ipython, httpie, black

**AI Tools:** Claude Code, Gemini CLI

## Platform-Specific Installation

### Windows

1. Install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/) and [GitHub Desktop](https://desktop.github.com/)
2. Clone repository via GitHub Desktop
3. Open in Command Prompt: `Repository` > `Open in Command Prompt`
4. Run `windows-start.bat`

### Linux Quick Start

```bash
chmod +x Start-WireStarter.sh
./Start-WireStarter.sh
```

### macOS / Linux

```bash
git clone https://github.com/signalwire/WireStarter.git
cd WireStarter
cp env.example .env
# Edit .env with your credentials
make up
make enter
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SIGNALWIRE_SPACE_NAME` | Yes | Your SignalWire space (without .signalwire.com) |
| `SIGNALWIRE_PROJECT_ID` | Yes | SignalWire project ID |
| `SIGNALWIRE_TOKEN` | Yes | SignalWire API token |
| `NGROK_TOKEN` | No | ngrok auth token for tunneling |
| `NGROK_ARGS` | No | Additional ngrok arguments (e.g., `--url yourdomain.ngrok.io`) |
| `WORKDIR` | Yes | Host directory to mount as /workdir |
| `VISUAL` | No | Preferred editor (vim/emacs/nano) |

## Example: Creating a SignalWire Agent

```bash
# Enter the container
make enter

# Exit swsh to get to bash
exit

# Create a new agent project
newagent mybot
cd /workdir/mybot

# Edit app.py with your agent logic
vim app.py

# Run it
up

# Your agent is now available at the ngrok URL
urls
```

## Webhook Development

WireStarter includes a webhook catcher for debugging callbacks:

```bash
# Start the webhook catcher
webhook

# Your webhook URL is:
# https://your-ngrok-url.ngrok.io/webhook
# https://your-ngrok-url.ngrok.io/webhook/xml (returns XML/LaML)
```

All incoming requests are pretty-printed to the console with headers, body, and query parameters.

## Troubleshooting

**Container exits immediately**
- Check that `.env` exists and has valid credentials
- Run `make debug` to see startup errors

**ngrok not working**
- Verify `NGROK_TOKEN` is set in `.env`
- Check ngrok status: `curl http://127.0.0.1:4040/api/tunnels`

**SignalWire credentials fail**
- Run `sw_test` to validate credentials
- Ensure space name doesn't include `.signalwire.com`

**Venv not activating**
- Only works in `/workdir/*` directories
- Run `venv init` to create one

## Contributing

Issues and pull requests welcome at [github.com/signalwire/WireStarter](https://github.com/signalwire/WireStarter).

## License

MIT License - See LICENSE file for details.
