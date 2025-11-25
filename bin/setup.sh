#!/bin/bash
# WireStarter Environment Setup

# Load existing .env if present
if [ -f "/workdir/.env" ]; then
    set -a
    source /workdir/.env
    set +a
fi

setup_credentials() {
    # Prepopulate with existing values
    local sw_space="${SIGNALWIRE_SPACE:-}"
    local project_id="${PROJECT_ID:-}"
    local api_token="${REST_API_TOKEN:-}"
    local ngrok_token="${NGROK_TOKEN:-}"
    local ngrok_args="${NGROK_ARGS:-}"
    local visual="${VISUAL:-vim}"

    # SignalWire Space
    sw_space=$(whiptail --inputbox "SignalWire Space Domain:" 8 60 "$sw_space" --title "SignalWire Credentials" 3>&1 1>&2 2>&3)
    [ $? -ne 0 ] && return

    # Project ID
    project_id=$(whiptail --inputbox "Project ID:" 8 60 "$project_id" --title "SignalWire Credentials" 3>&1 1>&2 2>&3)
    [ $? -ne 0 ] && return

    # API Token
    api_token=$(whiptail --inputbox "REST API Token:" 8 60 "$api_token" --title "SignalWire Credentials" 3>&1 1>&2 2>&3)
    [ $? -ne 0 ] && return

    # NGROK Token
    ngrok_token=$(whiptail --inputbox "NGROK Token (optional):" 8 60 "$ngrok_token" --title "NGROK Setup" 3>&1 1>&2 2>&3)
    [ $? -ne 0 ] && return

    # NGROK Args
    ngrok_args=$(whiptail --inputbox "NGROK Args (e.g., --url yourdomain.ngrok.io):" 8 70 "$ngrok_args" --title "NGROK Setup" 3>&1 1>&2 2>&3)
    [ $? -ne 0 ] && return

    # Editor selection
    visual=$(whiptail --title "Default Editor" --menu "Choose your editor:" 12 50 3 \
        "vim" "" \
        "emacs" "" \
        "nano" "" 3>&1 1>&2 2>&3)
    [ $? -ne 0 ] && return

    # Strip .signalwire.com if included
    sw_space=$(echo "$sw_space" | sed 's/\.signalwire\.com//g')

    # Write .env file (Docker --env-file compatible format)
    cat > /workdir/.env << ENVEOF
SIGNALWIRE_SPACE=$sw_space
PROJECT_ID=$project_id
REST_API_TOKEN=$api_token
NGROK_TOKEN=$ngrok_token
NGROK_ARGS=$ngrok_args
VISUAL=$visual
WORKDIR=/workdir
ENVEOF

    # Export for current session
    set -a
    source /workdir/.env
    set +a

    # Test credentials
    local test_url="https://${sw_space}.signalwire.com/api/laml/2010-04-01/Accounts"
    local response_code=$(curl -s -o /dev/null -w "%{http_code}" "$test_url" -u "${project_id}:${api_token}")

    if [ "$response_code" = "200" ]; then
        whiptail --title "Credentials Saved" --msgbox "Credentials saved to /workdir/.env\n\n[OK] SignalWire API test successful!" 10 50
    else
        whiptail --title "Credentials Saved" --msgbox "Credentials saved to /workdir/.env\n\n[!!] SignalWire API test failed (HTTP $response_code)\nPlease verify your credentials." 12 50
    fi
}

setup_golang() {
    echo "Installing Go to /workdir/.go..."
    ARCH=$(uname -m | sed 's/aarch64/arm64/g' | sed 's/x86_64/amd64/g')

    # Get latest stable version
    GO_VERSION=$(curl -s https://go.dev/VERSION?m=text | head -1)

    if [ -d "/workdir/.go" ]; then
        whiptail --title "Go Already Installed" --yesno "Go is already installed. Reinstall?" 8 50
        if [ $? -ne 0 ]; then
            return
        fi
        rm -rf /workdir/.go
    fi

    cd /tmp
    wget -q --show-progress "https://go.dev/dl/${GO_VERSION}.linux-${ARCH}.tar.gz"
    mkdir -p /workdir/.go
    tar -zxf "${GO_VERSION}.linux-${ARCH}.tar.gz" -C /workdir/.go --strip-components=1
    rm -f "${GO_VERSION}.linux-${ARCH}.tar.gz"

    whiptail --title "Go Installed" --msgbox "Go ${GO_VERSION} installed to /workdir/.go\n\nRun 'exec bash' to update your environment." 10 50
}

setup_nvm() {
    echo "Installing NVM to /workdir/.nvm..."

    if [ -d "/workdir/.nvm" ]; then
        whiptail --title "NVM Already Installed" --yesno "NVM is already installed. Reinstall?" 8 50
        if [ $? -ne 0 ]; then
            return
        fi
        rm -rf /workdir/.nvm
    fi

    mkdir -p /workdir/.nvm
    export NVM_DIR="/workdir/.nvm"
    curl -s -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash

    # Install latest LTS node
    source /workdir/.nvm/nvm.sh
    nvm install --lts

    whiptail --title "NVM Installed" --msgbox "NVM installed to /workdir/.nvm\nNode LTS installed.\n\nRun 'exec bash' to update your environment." 10 50
}

setup_pgsql() {
    PG_VERSION="15"
    NEW_PGDATA="/workdir/postgres"

    # Check if already setup
    if [ -d "$NEW_PGDATA" ] && [ -f "/workdir/.setuppgsql" ]; then
        whiptail --title "PostgreSQL Already Setup" --yesno "PostgreSQL data directory already exists. Reinitialize?\n\nWARNING: This will delete existing data!" 10 50
        if [ $? -ne 0 ]; then
            return
        fi
        sudo /etc/init.d/postgresql stop 2>/dev/null
        rm -rf "$NEW_PGDATA"
        rm -f /workdir/.setuppgsql
    fi

    echo "Setting up PostgreSQL with data in /workdir/postgres..."

    # Stop PostgreSQL if running
    sudo /etc/init.d/postgresql stop 2>/dev/null

    # Create and initialize data directory
    mkdir -p "$NEW_PGDATA"
    sudo chown postgres:postgres "$NEW_PGDATA"
    sudo chmod 700 "$NEW_PGDATA"

    echo "Initializing database cluster..."
    sudo -u postgres /usr/lib/postgresql/${PG_VERSION}/bin/initdb -D "$NEW_PGDATA"

    # Start PostgreSQL
    echo "Starting PostgreSQL..."
    sudo -u postgres /usr/lib/postgresql/${PG_VERSION}/bin/pg_ctl -D "$NEW_PGDATA" -l /workdir/postgres/logfile start

    touch /workdir/.setuppgsql

    whiptail --title "PostgreSQL Setup" --msgbox "PostgreSQL initialized in /workdir/postgres\n\nService is running." 10 50
}

setup_npm() {
    echo "Setting up npm cache persistence..."

    mkdir -p /workdir/.npm
    npm config set cache /workdir/.npm

    whiptail --title "NPM Cache" --msgbox "NPM cache set to /workdir/.npm" 8 50
}

setup_all() {
    whiptail --title "Setup All" --yesno "This will setup:\n\n- Go (latest)\n- NVM + Node LTS\n- PostgreSQL\n- NPM cache\n\nContinue?" 14 50
    if [ $? -ne 0 ]; then
        return
    fi

    setup_golang
    setup_nvm
    setup_pgsql
    setup_npm

    whiptail --title "Setup Complete" --msgbox "All development tools installed!\n\nRun 'exec bash' to update your environment." 10 50
}

show_status() {
    STATUS=""

    # Credentials status
    if [ -n "$SIGNALWIRE_SPACE" ] && [ -n "$PROJECT_ID" ] && [ -n "$REST_API_TOKEN" ]; then
        STATUS+="SignalWire: [OK] ${SIGNALWIRE_SPACE}\n"
    else
        STATUS+="SignalWire: [--] Not configured\n"
    fi

    if [ -n "$NGROK_TOKEN" ]; then
        STATUS+="NGROK: [OK] Configured\n"
    else
        STATUS+="NGROK: [--] Not configured\n"
    fi

    STATUS+="\n"

    if [ -d "/workdir/.go" ]; then
        GO_VER=$(/workdir/.go/bin/go version 2>/dev/null | awk '{print $3}')
        STATUS+="Go: [OK] ${GO_VER}\n"
    else
        STATUS+="Go: [--] Not installed\n"
    fi

    if [ -d "/workdir/.nvm" ]; then
        STATUS+="NVM: [OK] Installed\n"
    else
        STATUS+="NVM: [--] Not installed\n"
    fi

    if [ -f "/workdir/.setuppgsql" ]; then
        STATUS+="PostgreSQL: [OK] Configured\n"
    else
        STATUS+="PostgreSQL: [--] Not configured\n"
    fi

    if [ -d "/workdir/.npm" ]; then
        STATUS+="NPM Cache: [OK] Persistent\n"
    else
        STATUS+="NPM Cache: [--] Default\n"
    fi

    # Count venvs
    if [ -d "/workdir/.venvs" ]; then
        VENV_COUNT=$(ls -1 /workdir/.venvs/ 2>/dev/null | wc -l)
        STATUS+="Python venvs: [OK] ${VENV_COUNT} environments\n"
    else
        STATUS+="Python venvs: [--] None\n"
    fi

    STATUS+="\nPersistent directories:\n"
    STATUS+="- /workdir/.venvs (Python venvs)\n"
    STATUS+="- /workdir/.claude (Claude Code)\n"
    STATUS+="- /workdir/.gemini (Gemini CLI)\n"
    STATUS+="- /workdir/.ssh (SSH keys)\n"
    STATUS+="- /workdir/public (Static files)\n"

    whiptail --title "Environment Status" --msgbox "$STATUS" 26 50
}

# Main menu
while true; do
    CHOICE=$(whiptail --title "WireStarter Environment Setup" --menu "Select an option:" 20 60 10 \
        "1" "Setup SignalWire & NGROK Credentials" \
        "2" "Setup Go (latest stable)" \
        "3" "Setup NVM + Node.js" \
        "4" "Setup PostgreSQL" \
        "5" "Setup NPM cache persistence" \
        "6" "Setup All Dev Tools" \
        "7" "Show Status" \
        "8" "Exit" \
        3>&1 1>&2 2>&3)

    exitstatus=$?
    if [ $exitstatus -ne 0 ]; then
        exit 0
    fi

    case $CHOICE in
        "1") setup_credentials ;;
        "2") setup_golang ;;
        "3") setup_nvm ;;
        "4") setup_pgsql ;;
        "5") setup_npm ;;
        "6") setup_all ;;
        "7") show_status ;;
        "8") exit 0 ;;
    esac
done
