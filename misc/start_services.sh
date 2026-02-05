#!/bin/bash

# Persistent storage directory
PERSIST="/workdir/persistent"
DEVUSER_HOME="/home/devuser"
mkdir -p "$PERSIST" 2>/dev/null

# ============================================================================
# setup_persistence - Create all symlinks from devuser home to $PERSIST
# This runs once at container startup as root, targeting devuser's home
# ============================================================================
setup_persistence() {
    local H="$DEVUSER_HOME"

    # ~/.config (ngrok, GitHub Copilot, etc.)
    mkdir -p "$PERSIST/.config"
    rm -rf "$H/.config"
    ln -sf "$PERSIST/.config" "$H/.config"

    # Editor configs
    [ -f "$PERSIST/.emacs" ] && ln -sf "$PERSIST/.emacs" "$H/.emacs"
    [ -d "$PERSIST/.emacs.d" ] && rm -rf "$H/.emacs.d" && ln -sf "$PERSIST/.emacs.d" "$H/.emacs.d"
    [ -f "$PERSIST/.vimrc" ] && ln -sf "$PERSIST/.vimrc" "$H/.vimrc"
    [ -d "$PERSIST/.vim" ] && rm -rf "$H/.vim" && ln -sf "$PERSIST/.vim" "$H/.vim"
    [ -f "$PERSIST/.nanorc" ] && ln -sf "$PERSIST/.nanorc" "$H/.nanorc"

    # Git configs
    [ -f "$PERSIST/.gitconfig" ] && ln -sf "$PERSIST/.gitconfig" "$H/.gitconfig"
    [ -f "$PERSIST/.git-credentials" ] && ln -sf "$PERSIST/.git-credentials" "$H/.git-credentials"
    [ -f "$PERSIST/.pypirc" ] && ln -sf "$PERSIST/.pypirc" "$H/.pypirc"

    # Cache directory (pip, npm, etc.)
    # Migrate existing cache if it's a real directory
    if [ -d "$H/.cache" ] && [ ! -L "$H/.cache" ]; then
        mkdir -p "$PERSIST/.cache"
        cp -a "$H/.cache/." "$PERSIST/.cache/" 2>/dev/null || true
        rm -rf "$H/.cache"
    fi
    mkdir -p "$PERSIST/.cache"
    ln -sf "$PERSIST/.cache" "$H/.cache"

    # SSH directory
    if [ -d "$PERSIST/.ssh" ]; then
        rm -rf "$H/.ssh"
        ln -sf "$PERSIST/.ssh" "$H/.ssh"
    fi

    # Claude Code config
    mkdir -p "$PERSIST/.claude"
    rm -rf "$H/.claude"
    ln -sf "$PERSIST/.claude" "$H/.claude"
    # Claude MCP config files - migrate if needed
    if [ -f "$H/.claude.json" ] && [ ! -L "$H/.claude.json" ] && [ ! -f "$PERSIST/.claude.json" ]; then
        mv "$H/.claude.json" "$PERSIST/.claude.json"
    fi
    if [ -f "$H/.claude.json.backup" ] && [ ! -L "$H/.claude.json.backup" ] && [ ! -f "$PERSIST/.claude.json.backup" ]; then
        mv "$H/.claude.json.backup" "$PERSIST/.claude.json.backup"
    fi
    ln -sf "$PERSIST/.claude.json" "$H/.claude.json"
    ln -sf "$PERSIST/.claude.json.backup" "$H/.claude.json.backup"

    # Gemini CLI config
    mkdir -p "$PERSIST/.gemini"
    rm -rf "$H/.gemini"
    ln -sf "$PERSIST/.gemini" "$H/.gemini"
    # Ensure MCP settings file exists
    [ ! -f "$PERSIST/.gemini/settings.json" ] && echo '{"mcpServers":{}}' > "$PERSIST/.gemini/settings.json"

    # Cloudflare Tunnel config
    if [ -d "$PERSIST/.cloudflared" ]; then
        rm -rf "$H/.cloudflared"
        ln -sf "$PERSIST/.cloudflared" "$H/.cloudflared"
    fi

    # AWS CLI config (~/.aws)
    mkdir -p "$PERSIST/.aws"
    rm -rf "$H/.aws"
    ln -sf "$PERSIST/.aws" "$H/.aws"

    # Google Cloud CLI config (~/.config/gcloud)
    # Note: ~/.config is already symlinked to $PERSIST/.config above,
    # so we just need to ensure the gcloud subdirectory exists
    mkdir -p "$PERSIST/.config/gcloud"

    # Azure CLI config (~/.azure)
    mkdir -p "$PERSIST/.azure"
    rm -rf "$H/.azure"
    ln -sf "$PERSIST/.azure" "$H/.azure"

    # ~/.local (UV, pip user installs, etc.)
    # Migrate existing content from Docker image if present
    if [ -d "$H/.local" ] && [ ! -L "$H/.local" ]; then
        mkdir -p "$PERSIST/.local"
        cp -a "$H/.local/." "$PERSIST/.local/" 2>/dev/null || true
        rm -rf "$H/.local"
    fi
    mkdir -p "$PERSIST/.local/bin"
    mkdir -p "$PERSIST/.local/share/uv"
    ln -sf "$PERSIST/.local" "$H/.local"

    # NPM cache and config - use $PERSIST/.npm directly (no double symlinks)
    mkdir -p "$PERSIST/.npm"
    # Always set correct cache path in npmrc
    echo "cache=$PERSIST/.npm" > "$PERSIST/.npmrc"
    rm -f "$H/.npmrc"
    ln -sf "$PERSIST/.npmrc" "$H/.npmrc"
    rm -rf "$H/.npm"
    ln -sf "$PERSIST/.npm" "$H/.npm"

    # swsh history
    touch "$PERSIST/.swsh_history"
    ln -sf "$PERSIST/.swsh_history" "$H/.swsh_history"

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
    runuser -u devuser -- git config --global core.excludesfile "$PERSIST/.gitignore_global" 2>/dev/null

    # Create public and logs directories
    mkdir -p "$PERSIST/public"
    mkdir -p "$PERSIST/logs"

    # Fix ownership: devuser home and persistent storage
    chown -R devuser:devuser "$H" 2>/dev/null || true
    chown devuser:devuser /workdir 2>/dev/null || true
    chown -R devuser:devuser "$PERSIST" 2>/dev/null || true
}

# Run persistence setup
setup_persistence

# Auto-unlock encrypted secrets if key file exists (for automation)
if [ -f /workdir/.secrets/age-key.txt ] && [ -d /workdir/.git-crypt ]; then
    echo "Auto-unlocking encrypted secrets..."
    /usr/bin/secrets unlock --quiet 2>/dev/null || true
fi

# Start Ngrok (as devuser so tmux sessions are accessible)
if [ -n "$NGROK_TOKEN" ]; then
    runuser -u devuser -- /usr/local/bin/ngrok config add-authtoken "$NGROK_TOKEN" > /dev/null 2>&1
    runuser -u devuser -- /usr/bin/tmux new-session -d -s ngrok "/usr/local/bin/ngrok http $NGROK_ARGS 9080"

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
    runuser -u devuser -- /usr/bin/tmux new-session -d -s cloudflared "TUNNEL_TOKEN=\$(cat $PERSIST/.cloudflared/token) exec cloudflared tunnel run"
    echo "Cloudflare Tunnel starting..."
fi

/etc/init.d/redis-server start > /dev/null 2>&1
/etc/init.d/nginx start > /dev/null 2>&1

# Start PostgreSQL if data directory exists (PG_VERSION file indicates valid cluster)
if [ -f "$PERSIST/postgres/PG_VERSION" ]; then
    sudo -u postgres /usr/lib/postgresql/17/bin/pg_ctl -D "$PERSIST/postgres" -l "$PERSIST/postgres/logfile" start >/dev/null 2>&1
fi

# Start webhook catcher in background (logs directory created by setup_persistence)
runuser -u devuser -- /usr/bin/tmux new-session -d -s webhook "python3 /usr/bin/webhook-catcher.py 5002 --log-file $PERSIST/logs/webhook.log"


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
