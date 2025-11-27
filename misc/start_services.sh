#!/bin/bash

# Persistent storage directory
PERSIST="/workdir/persistent"
mkdir -p "$PERSIST" 2>/dev/null

# ============================================================================
# setup_persistence - Create all symlinks from ~ to $PERSIST
# This runs once at container startup, not on every shell
# ============================================================================
setup_persistence() {
    # ~/.config (ngrok, GitHub Copilot, etc.)
    mkdir -p "$PERSIST/.config"
    rm -rf ~/.config
    ln -sf "$PERSIST/.config" ~/.config

    # Editor configs
    [ -f "$PERSIST/.emacs" ] && ln -sf "$PERSIST/.emacs" ~/.emacs
    [ -d "$PERSIST/.emacs.d" ] && rm -rf ~/.emacs.d && ln -sf "$PERSIST/.emacs.d" ~/.emacs.d
    [ -f "$PERSIST/.vimrc" ] && ln -sf "$PERSIST/.vimrc" ~/.vimrc
    [ -d "$PERSIST/.vim" ] && rm -rf ~/.vim && ln -sf "$PERSIST/.vim" ~/.vim
    [ -f "$PERSIST/.nanorc" ] && ln -sf "$PERSIST/.nanorc" ~/.nanorc

    # Git configs
    [ -f "$PERSIST/.gitconfig" ] && ln -sf "$PERSIST/.gitconfig" ~/.gitconfig
    [ -f "$PERSIST/.git-credentials" ] && ln -sf "$PERSIST/.git-credentials" ~/.git-credentials
    [ -f "$PERSIST/.pypirc" ] && ln -sf "$PERSIST/.pypirc" ~/.pypirc

    # Cache directory (pip, npm, etc.)
    # Migrate existing cache if it's a real directory
    if [ -d ~/.cache ] && [ ! -L ~/.cache ]; then
        mkdir -p "$PERSIST/.cache"
        cp -a ~/.cache/. "$PERSIST/.cache/" 2>/dev/null || true
        rm -rf ~/.cache
    fi
    mkdir -p "$PERSIST/.cache"
    ln -sf "$PERSIST/.cache" ~/.cache

    # SSH directory
    if [ -d "$PERSIST/.ssh" ]; then
        rm -rf ~/.ssh
        ln -sf "$PERSIST/.ssh" ~/.ssh
    fi

    # Claude Code config
    mkdir -p "$PERSIST/.claude"
    rm -rf ~/.claude
    ln -sf "$PERSIST/.claude" ~/.claude
    # Claude MCP config files - migrate if needed
    if [ -f ~/.claude.json ] && [ ! -L ~/.claude.json ] && [ ! -f "$PERSIST/.claude.json" ]; then
        mv ~/.claude.json "$PERSIST/.claude.json"
    fi
    if [ -f ~/.claude.json.backup ] && [ ! -L ~/.claude.json.backup ] && [ ! -f "$PERSIST/.claude.json.backup" ]; then
        mv ~/.claude.json.backup "$PERSIST/.claude.json.backup"
    fi
    ln -sf "$PERSIST/.claude.json" ~/.claude.json
    ln -sf "$PERSIST/.claude.json.backup" ~/.claude.json.backup

    # Gemini CLI config
    mkdir -p "$PERSIST/.gemini"
    rm -rf ~/.gemini
    ln -sf "$PERSIST/.gemini" ~/.gemini
    # Ensure MCP settings file exists
    [ ! -f "$PERSIST/.gemini/settings.json" ] && echo '{"mcpServers":{}}' > "$PERSIST/.gemini/settings.json"

    # NanoCoder config (local-first CLI coding agent for Ollama/local LLMs)
    mkdir -p "$PERSIST/.nanocoder"
    rm -rf ~/.nanocoder
    ln -sf "$PERSIST/.nanocoder" ~/.nanocoder

    # Cloudflare Tunnel config
    if [ -d "$PERSIST/.cloudflared" ]; then
        rm -rf ~/.cloudflared
        ln -sf "$PERSIST/.cloudflared" ~/.cloudflared
    fi

    # AWS CLI config (~/.aws)
    mkdir -p "$PERSIST/.aws"
    rm -rf ~/.aws
    ln -sf "$PERSIST/.aws" ~/.aws

    # Google Cloud CLI config (~/.config/gcloud)
    mkdir -p "$PERSIST/.config/gcloud"
    mkdir -p ~/.config
    rm -rf ~/.config/gcloud
    ln -sf "$PERSIST/.config/gcloud" ~/.config/gcloud

    # Azure CLI config (~/.azure)
    mkdir -p "$PERSIST/.azure"
    rm -rf ~/.azure
    ln -sf "$PERSIST/.azure" ~/.azure

    # UV (Python package manager) - tools and cache
    mkdir -p "$PERSIST/.local/share/uv"
    mkdir -p "$PERSIST/.local/bin"
    mkdir -p ~/.local/share
    rm -rf ~/.local/share/uv
    ln -sf "$PERSIST/.local/share/uv" ~/.local/share/uv
    rm -rf ~/.local/bin
    ln -sf "$PERSIST/.local/bin" ~/.local/bin

    # NPM cache and config - use $PERSIST/.npm directly (no double symlinks)
    mkdir -p "$PERSIST/.npm"
    # Always set correct cache path in npmrc
    echo "cache=$PERSIST/.npm" > "$PERSIST/.npmrc"
    rm -f ~/.npmrc
    ln -sf "$PERSIST/.npmrc" ~/.npmrc
    rm -rf ~/.npm
    ln -sf "$PERSIST/.npm" ~/.npm

    # swsh history
    touch "$PERSIST/.swsh_history"
    ln -sf "$PERSIST/.swsh_history" ~/.swsh_history

    # Global gitignore
    if [ ! -f "$PERSIST/.gitignore_global" ]; then
        cat > "$PERSIST/.gitignore_global" << 'GITIGNORE'
# Global gitignore - prevents committing secrets
.env
.env.*
*.env
.envrc
.npmrc
credentials.json
*_credentials.json
*.pem
*.key
id_rsa
id_ed25519
.claude.json
.claude.json.backup
GITIGNORE
    fi
    git config --global core.excludesfile "$PERSIST/.gitignore_global" 2>/dev/null

    # Create public and logs directories
    mkdir -p "$PERSIST/public"
    mkdir -p "$PERSIST/logs"
}

# Run persistence setup
setup_persistence

# Start Ngrok
if [ -n "$NGROK_TOKEN" ]; then
    /usr/local/bin/ngrok config add-authtoken "$NGROK_TOKEN" > /dev/null 2>&1
    /usr/bin/tmux new-session -d -s ngrok "/usr/local/bin/ngrok http $NGROK_ARGS 9080"

    # Wait for ngrok to be ready (up to 20 seconds)
    RETRY_COUNT=0
    MAX_RETRIES=10
    while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
        sleep 2
        NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels 2>/dev/null | jq -r '.tunnels[0].public_url' 2>/dev/null)
        if [ "$NGROK_URL" != "null" ] && [ -n "$NGROK_URL" ]; then
            echo "ngrok tunnel ready: $NGROK_URL"
            break
        fi
        RETRY_COUNT=$((RETRY_COUNT+1))
    done
fi

export HOSTNAME=$(curl -s http://127.0.0.1:4040/api/tunnels 2>/dev/null | jq -r '.tunnels[0].public_url' 2>/dev/null | sed 's/https:\/\///')

# Start Cloudflare Tunnel if configured (symlink already created by setup_persistence)
if [ -f "$PERSIST/.cloudflared/token" ]; then
    /usr/bin/tmux new-session -d -s cloudflared "TUNNEL_TOKEN=\$(cat $PERSIST/.cloudflared/token) exec cloudflared tunnel run"
    echo "Cloudflare Tunnel starting..."
fi

/etc/init.d/redis-server start > /dev/null 2>&1
/etc/init.d/nginx start > /dev/null 2>&1

# Start PostgreSQL if data directory exists (PG_VERSION file indicates valid cluster)
if [ -f "$PERSIST/postgres/PG_VERSION" ]; then
    sudo -u postgres /usr/lib/postgresql/15/bin/pg_ctl -D "$PERSIST/postgres" -l "$PERSIST/postgres/logfile" start >/dev/null 2>&1
fi

# Start webhook catcher in background (logs directory created by setup_persistence)
/usr/bin/tmux new-session -d -s webhook "python3 /usr/bin/webhook-catcher.py 5002 --log-file $PERSIST/logs/webhook.log"


# Loop so we can update the urls if they change while running.
while true
do
    if [ -n "$NGROK_TOKEN" ]; then
        export NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels 2>/dev/null | jq -r '.tunnels[0].public_url' 2>/dev/null)
    fi

    clear
    echo -e "\n\n";
    cat /.sw.ans
    echo -e "\n\n";
    echo -e "Welcome to WireStarter!";
    echo -e "\n"

    if [ -n "$NGROK_URL" ] && [ "$NGROK_URL" != "null" ]; then
        echo -e "NGROK Tunnel: $NGROK_URL";
        echo -e "/workdir/persistent/public -> $NGROK_URL/public\n";
    fi
    if [ -n "$WORKDIR" ]; then
        echo -e "Persistent host directory is /workdir -> $WORKDIR\n";
    fi
    
    echo -e "\n-- Thank you!\nsupport@signalwire.com\n\n";
    
    sleep 300
done
