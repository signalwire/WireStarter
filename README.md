# WireStarter

A batteries-included Docker development environment for building SignalWire applications.

![Screenshot of WireStarter](https://raw.githubusercontent.com/signalwire/WireStarter/master/misc/ws.png)

## Features

- **Pre-configured SignalWire SDKs** - Python SDK, signalwire-agents, SWML, SWAIG ready to use
- **Automatic tunneling** - ngrok or Cloudflare Tunnel for public webhook URLs
- **Persistent storage** - Your code, venvs, configs, and credentials survive container rebuilds
- **Interactive setup** - TUI menus for configuring credentials and tools
- **Built-in services** - Redis, nginx, PostgreSQL, FreeSWITCH available on demand
- **AI coding assistants** - Claude Code, Gemini CLI, and OpenAI Codex pre-installed with MCP support
- **Developer tools** - Git, tmux, editors (vim/emacs/nano/micro/ne), debugging utilities
- **Security** - Global gitignore prevents accidental credential commits

## Prerequisites

- [Docker Desktop](https://docs.docker.com/desktop/)
- [SignalWire Account](https://signalwire.com/signup) with [API Credentials](https://developer.signalwire.com/guides/your-first-api-calls/)
- [ngrok Account](https://ngrok.com) or [Cloudflare Tunnel](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)

## Quick Start

### One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/signalwire/WireStarter/master/misc/install.sh | bash
```

This pulls the image from Docker Hub and drops you directly into the container. Run `setup` to configure your SignalWire credentials and environment.

### Alternative: Clone Repository

For developers who want to customize the image or contribute:

```bash
git clone https://github.com/signalwire/WireStarter.git
cd WireStarter
cp env.example .env
# Edit .env with your credentials
make up      # Start in background
make enter   # Enter the container
```

### First Run

On first entry, WireStarter shows a welcome screen. Run `setup` for the interactive configuration menu to set up:
- SignalWire credentials
- ngrok or Cloudflare tunnel
- AI assistants (Claude, Gemini, Codex)
- Development tools

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

### Interactive Setup Menu

```bash
setup                 # Interactive environment setup menu
```

The setup menu provides:

| Option | Description |
|--------|-------------|
| Setup SignalWire & NGROK Credentials | Configure API keys and ngrok token (required) |
| Start ngrok Tunnel | Start/restart the ngrok tunnel |
| Setup Cloudflare Tunnel | Alternative to ngrok using Cloudflare |
| Setup AI API Keys | Configure Claude/Gemini API keys or OAuth |
| Add MCP Servers | Add Model Context Protocol servers to Claude/Gemini |
| Remove MCP Server | Remove configured MCP servers |
| Setup Git Identity | Configure git user, email, and GitHub token |
| Setup SSH Key | Generate ED25519 SSH key for git |
| Setup Go | Install latest Go to /workdir/persistent/.go |
| Setup NVM + Node.js | Install NVM and Node.js LTS |
| Setup PostgreSQL | Initialize PostgreSQL in /workdir/persistent/postgres |
| Setup FreeSWITCH | Install FreeSWITCH (requires PAT) |
| Setup Python Dev Tools | Install black, pytest, build, twine |
| Setup Audio Tools | Install pydub for audio processing |
| Setup All Dev Tools | Install Go, NVM, PostgreSQL, Python tools |
| Enable/Disable swsh | Toggle SignalWire Shell on login |
| Show Status | Display current environment status |
| Clean Environment | Remove all dev tools and configs |

### Python Virtual Environments

Venvs are stored in `/workdir/persistent/.venvs/` and persist across container rebuilds.

```bash
venv init             # Create venv for current directory
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
- `web/` - Static files with WebRTC calling interface
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
webhook               # Tail webhook log (catcher runs in background)
logs                  # Tail nginx access log
reqs                  # Formatted request log
```

### Process Management

```bash
ports                 # Show what's running on 5000, 5001, 9080
killport 5000         # Kill process on port
reload                # Reload nginx
tmux attach -t ngrok  # Attach to ngrok session
tmux attach -t cloudflared  # Attach to Cloudflare tunnel session
```

### Redis

```bash
redis                 # Redis CLI
rkeys                 # List all keys
rget mykey            # Get value
rclear                # Flush all data
```

### PostgreSQL

```bash
psql                  # Connect to PostgreSQL (auto-configured)
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
public                # cd /workdir/persistent/public
..                    # cd ..
...                   # cd ../..
```

## Architecture

### Services

On startup, WireStarter runs:

1. **ngrok** (if configured) - Tunnels port 9080 to a public URL (runs in tmux)
2. **Cloudflare Tunnel** (if configured) - Alternative tunnel to ngrok (runs in tmux)
3. **nginx** - Reverse proxy on port 9080
   - `/` → localhost:5000 (your app)
   - `/webhook` → localhost:5002 (webhook catcher)
   - `/public` → /workdir/persistent/public (static files)
4. **Redis** - Available on default port
5. **PostgreSQL** (if configured) - Auto-starts if data directory exists
6. **Webhook catcher** - Logs incoming requests to `/workdir/persistent/logs/webhook.log` (runs in tmux)

### Persistent Storage

Everything in `/workdir/persistent` survives container rebuilds. The following files and directories are automatically symlinked from `/workdir/persistent` to their expected locations:

| Path | Purpose |
|------|---------|
| `/workdir/persistent/.env` | Environment variables (SignalWire, ngrok, etc.) |
| `/workdir/persistent/.venvs/` | Python virtual environments |
| `/workdir/persistent/.ssh/` | SSH keys |
| `/workdir/persistent/.gitconfig` | Git configuration |
| `/workdir/persistent/.git-credentials` | Git credential storage |
| `/workdir/persistent/.gitignore_global` | Global gitignore (auto-created) |
| `/workdir/persistent/.go/` | Go installation |
| `/workdir/persistent/.nvm/` | NVM + Node.js |
| `/workdir/persistent/.npm/` | NPM cache |
| `/workdir/persistent/.npmrc` | NPM configuration |
| `/workdir/persistent/.claude/` | Claude Code auth & session data |
| `/workdir/persistent/.claude.json` | Claude Code MCP configuration |
| `/workdir/persistent/.gemini/` | Gemini CLI auth & config |
| `/workdir/persistent/.codex/` | OpenAI Codex CLI auth & config |
| `/workdir/persistent/.cloudflared/` | Cloudflare Tunnel config & token |
| `/workdir/persistent/.config/` | XDG config (GitHub Copilot, etc.) |
| `/workdir/persistent/.emacs` | Emacs configuration |
| `/workdir/persistent/.vimrc` | Vim configuration |
| `/workdir/persistent/.nanorc` | Nano configuration |
| `/workdir/persistent/.pypirc` | PyPI configuration |
| `/workdir/persistent/.swsh_history` | SignalWire Shell history |
| `/workdir/persistent/.noswsh` | Disable swsh on login (if present) |
| `/workdir/persistent/postgres/` | PostgreSQL data directory |
| `/workdir/persistent/logs/` | Persistent logs (webhook, etc.) |
| `/workdir/persistent/public/` | Static files (served at tunnel URL/public) |

**Note for existing users:** Run `migrate-persistent` to move your config files from `/workdir` to the new `/workdir/persistent` structure. After running the migration script, rebuild the container with `make build && make up`.

### Security Features

**Global Gitignore**: WireStarter automatically creates `/workdir/persistent/.gitignore_global` to prevent accidentally committing secrets. The following patterns are globally ignored in all git repositories:

- `.env`, `.env.*`, `*.env`, `.envrc`
- `credentials.json`, `*_credentials.json`
- `*.pem`, `*.key`
- `id_rsa`, `id_ed25519`
- `.npmrc`
- `.claude.json`, `.claude.json.backup`

**Token Storage**: Sensitive tokens (like Cloudflare Tunnel) are stored in dedicated files with restricted permissions (chmod 600) rather than in `.env`.

### Pre-installed Packages

**System:** git, curl, wget, jq, tmux, screen, ffmpeg, sox, sqlite3, ncdu, cloudflared

**Editors:** vim, emacs, nano, micro, ne

**Python:** signalwire, signalwire-agents, signalwire-swml, signalwire-swaig, flask, requests, ipython, httpie, black

**AI Tools:** Claude Code, Gemini CLI, OpenAI Codex (with MCP server support)

## Tunneling Options

### ngrok (Default)

Set `NGROK_TOKEN` in your `.env` file. The tunnel starts automatically on container launch.

```bash
# Optional: Use a custom domain
NGROK_ARGS="--url yourdomain.ngrok.io"
```

Access the ngrok session: `tmux attach -t ngrok`

### Cloudflare Tunnel (Alternative)

1. Create a tunnel in [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/)
2. Run `setup` and select "Setup Cloudflare Tunnel"
3. Enter your tunnel token

The tunnel runs in a tmux session and auto-starts on container launch.

Access the cloudflared session: `tmux attach -t cloudflared`

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SIGNALWIRE_SPACE_NAME` | Yes | Your SignalWire space (without .signalwire.com) |
| `SIGNALWIRE_PROJECT_ID` | Yes | SignalWire project ID |
| `SIGNALWIRE_TOKEN` | Yes | SignalWire API token |
| `NGROK_TOKEN` | Yes* | ngrok auth token (*or use Cloudflare Tunnel) |
| `NGROK_ARGS` | No | Additional ngrok arguments (e.g., `--url yourdomain.ngrok.io`) |
| `FREESWITCH_PAT` | No | FreeSWITCH package access token |
| `WORKDIR` | Yes | Host directory to mount as /workdir |
| `VISUAL` | No | Preferred editor (vim/emacs/nano/micro/ne) |
| `ANTHROPIC_API_KEY` | No | Claude API key (alternative to OAuth) |
| `GEMINI_API_KEY` | No | Gemini API key (alternative to OAuth) |
| `OPENAI_API_KEY` | No | OpenAI Codex API key (alternative to OAuth) |
| `GITHUB_TOKEN` | No | GitHub personal access token |
| `SLACK_BOT_TOKEN` | No | Slack bot token (for MCP server) |
| `BRAVE_API_KEY` | No | Brave Search API key (for MCP server) |

## AI Coding Assistants

### Claude Code

Claude Code is pre-installed. Authenticate via:
- OAuth: `claude` (browser-based login)
- API Key: Set `ANTHROPIC_API_KEY` in setup

MCP servers can be added via the setup menu for enhanced capabilities (filesystem access, GitHub, memory, etc.).

### Gemini CLI

Gemini CLI is pre-installed. Authenticate via:
- OAuth: `gemini` (browser-based login)
- API Key: Set `GEMINI_API_KEY` in setup

### OpenAI Codex CLI

OpenAI Codex CLI is pre-installed. Authenticate via:
- OAuth: `codex auth login` (browser-based login)
- API Key: Set `OPENAI_API_KEY` in setup

Codex supports the same MCP servers as Claude and Gemini.

## Example: Creating a SignalWire Agent

```bash
# Enter the container
make enter

# Exit swsh to get to bash
exit

# Create a new agent project
newagent mybot
cd /workdir/mybot

# Edit the agent logic
vim agents/main_agent.py

# Run it
up

# Your agent is now available at the ngrok URL
urls
```

## Webhook Development

WireStarter includes a webhook catcher that runs automatically as a background service. All requests to `/webhook` are logged to `/workdir/persistent/logs/webhook.log`.

```bash
webhook               # Tail the webhook log (live view)
webhook clear         # Clear the log file
webhook status        # Show catcher status and URLs
webhook attach        # Attach to the tmux session
```

Your webhook URLs are:
- `https://your-tunnel-url/webhook` - Returns JSON response
- `https://your-tunnel-url/webhook/xml` - Returns XML/LaML response

Requests are logged with headers, body, and query parameters.

## Troubleshooting

**Container exits immediately**
- Check that `.env` exists and has valid credentials
- Run `make debug` to see startup errors

**ngrok not working**
- Verify `NGROK_TOKEN` is set in `.env`
- Check ngrok status: `curl http://127.0.0.1:4040/api/tunnels`
- Attach to session: `tmux attach -t ngrok`

**Cloudflare Tunnel not working**
- Check the tunnel session: `tmux attach -t cloudflared`
- Verify token file exists: `ls -la /workdir/persistent/.cloudflared/token`
- Re-run setup to reconfigure

**SignalWire credentials fail**
- Run `sw_test` to validate credentials
- Ensure space name doesn't include `.signalwire.com`

**Venv not activating**
- Only works in `/workdir/*` directories
- Run `venv init` to create one

**PostgreSQL not starting**
- Check if data exists: `ls /workdir/persistent/postgres/PG_VERSION`
- Run `setup` → "Setup PostgreSQL" to initialize

## Platform-Specific Notes

### macOS / Linux

The one-line install works directly:

```bash
curl -fsSL https://raw.githubusercontent.com/signalwire/WireStarter/master/misc/install.sh | bash
```

### Windows

1. Install [Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)
2. Open PowerShell or Command Prompt
3. Run the install script or use Docker directly:

```powershell
docker pull briankwest/wirestarter:latest
docker run -d --name wirestarter -v wirestarter_workdir:/workdir -v /var/run/docker.sock:/var/run/docker.sock -p 9080:9080 briankwest/wirestarter:latest
docker exec -it wirestarter bash
```

## Contributing

Issues and pull requests welcome at [github.com/signalwire/WireStarter](https://github.com/signalwire/WireStarter).

## License

MIT License - See LICENSE file for details.
