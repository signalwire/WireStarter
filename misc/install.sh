#!/bin/bash
# WireStarter Quick Install Script
# Usage: curl -fsSL https://raw.githubusercontent.com/signalwire/WireStarter/master/misc/install.sh | bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}WireStarter Installer${NC}"
echo "====================="
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker Desktop from https://docker.com/products/docker-desktop"
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo -e "${GREEN}✓${NC} Docker is running"

# Pull latest image
echo ""
echo "Pulling WireStarter image..."
docker pull briankwest/wirestarter:latest

echo ""

# Check if container exists
if docker ps -a --format '{{.Names}}' | grep -q '^wirestarter$'; then
    # Container exists - check if running
    if docker ps --format '{{.Names}}' | grep -q '^wirestarter$'; then
        echo "WireStarter container is already running"
    else
        echo "Starting existing WireStarter container..."
        docker start wirestarter
    fi
else
    echo "Creating WireStarter container..."
    docker run -d \
        --name wirestarter \
        -v wirestarter_workdir:/workdir \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -p 9080:9080 \
        briankwest/wirestarter:latest

    # Wait for container to be ready
    sleep 2
fi

# Enter container
echo ""
echo -e "${GREEN}Entering WireStarter...${NC}"
echo "Run 'setup' to configure your environment"
echo ""
docker exec -it wirestarter bash
