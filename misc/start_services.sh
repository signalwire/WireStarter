#!/bin/bash

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

# Start Cloudflare Tunnel if configured
if [ -f "/workdir/.cloudflared/token" ]; then
    # Symlink config directory
    rm -rf ~/.cloudflared
    ln -sf /workdir/.cloudflared ~/.cloudflared
    # Start tunnel in tmux using TUNNEL_TOKEN env var to avoid exposing token in process list
    /usr/bin/tmux new-session -d -s cloudflared "TUNNEL_TOKEN=\$(cat /workdir/.cloudflared/token) exec cloudflared tunnel run"
    echo "Cloudflare Tunnel starting..."
fi

/etc/init.d/redis-server start > /dev/null 2>&1
/etc/init.d/nginx start > /dev/null 2>&1

# Start PostgreSQL if data directory exists (PG_VERSION file indicates valid cluster)
if [ -f "/workdir/postgres/PG_VERSION" ]; then
    sudo -u postgres /usr/lib/postgresql/15/bin/pg_ctl -D /workdir/postgres -l /workdir/postgres/logfile start >/dev/null 2>&1
fi


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
        echo -e "/workdir/public -> $NGROK_URL/public\n";
    fi
    if [ -n "$WORKDIR" ]; then
        echo -e "Persistent host directory is /workdir -> $WORKDIR\n";
    fi
    
    echo -e "\n-- Thank you!\nsupport@signalwire.com\n\n";
    
    sleep 300
done
