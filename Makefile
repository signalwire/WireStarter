# WireStarter Makefile
# Docker development environment for SignalWire applications

IMAGE_NAME := briankwest/wirestarter
CONTAINER_NAME := wirestarter
PLATFORMS := linux/amd64,linux/arm64

# Default target
.DEFAULT_GOAL := help

# Phony targets
.PHONY: help build up down enter logs restart clean prune push debug status shell

##@ General

help: ## Show this help message
	@echo "WireStarter - Docker development environment for SignalWire"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"; printf ""} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Container Management

up: ## Start container in background (detached)
	@if [ -z "$${WORKDIR}" ]; then \
		echo "Error: WORKDIR environment variable must be set"; \
		echo "Usage: WORKDIR=/path/to/workspace make up"; \
		exit 1; \
	fi
	@ENV_FILE=""; \
	if [ -f "$${WORKDIR}/persistent/.env" ]; then \
		ENV_FILE="--env-file $${WORKDIR}/persistent/.env"; \
		echo "Using $${WORKDIR}/persistent/.env"; \
	else \
		echo "No .env found - starting fresh (run 'setup' inside container)"; \
	fi; \
	docker run -it -d --rm \
		--name $(CONTAINER_NAME) \
		$$ENV_FILE \
		-e HOST_WORKDIR="$${WORKDIR}" \
		--volume "$${WORKDIR}:/workdir" \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		$(IMAGE_NAME) || echo "Container may already be running"

down: ## Stop running container
	@docker stop $(CONTAINER_NAME) 2>/dev/null || echo "Container not running"

restart: down up ## Restart container

enter: ## Enter running container (interactive bash)
	@docker exec -it $(CONTAINER_NAME) /bin/bash

shell: enter ## Alias for enter

logs: ## Tail container logs
	@docker logs -f $(CONTAINER_NAME)

status: ## Show container status and info
	@echo "=== Container Status ==="
	@docker ps -a --filter name=$(CONTAINER_NAME) --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
	@echo ""
	@echo "=== WORKDIR ==="
	@if [ -n "$${WORKDIR}" ]; then \
		echo "WORKDIR: $${WORKDIR}"; \
		if [ -f "$${WORKDIR}/persistent/.env" ]; then \
			echo ".env: Found at $${WORKDIR}/persistent/.env"; \
			grep -c "^[^#]" "$${WORKDIR}/persistent/.env" 2>/dev/null | xargs -I {} echo "Variables defined: {}"; \
		else \
			echo ".env: Not found (run 'setup' inside container)"; \
		fi; \
	else \
		echo "WORKDIR: NOT SET"; \
		echo "Set WORKDIR environment variable to your workspace directory"; \
	fi

##@ Build & Deploy

build: ## Build image (no cache)
	@echo "Building $(IMAGE_NAME)..."
	@docker build --no-cache -t $(IMAGE_NAME) .

build-cache: ## Build image (with cache)
	@echo "Building $(IMAGE_NAME) with cache..."
	@docker build -t $(IMAGE_NAME) .

push: ## Build and push multi-arch image to Docker Hub
	@echo "Building and pushing multi-arch image..."
	@docker buildx build \
		--platform $(PLATFORMS) \
		--tag $(IMAGE_NAME):latest \
		--push .

##@ Development

debug: ## Run container in foreground (for debugging)
	@if [ -z "$${WORKDIR}" ]; then \
		echo "Error: WORKDIR environment variable must be set"; \
		echo "Usage: WORKDIR=/path/to/workspace make debug"; \
		exit 1; \
	fi
	@ENV_FILE=""; \
	if [ -f "$${WORKDIR}/persistent/.env" ]; then \
		ENV_FILE="--env-file $${WORKDIR}/persistent/.env"; \
		echo "Using $${WORKDIR}/persistent/.env"; \
	else \
		echo "No .env found - starting fresh (run 'setup' inside container)"; \
	fi; \
	docker run -it --rm \
		--name $(CONTAINER_NAME) \
		$$ENV_FILE \
		-e HOST_WORKDIR="$${WORKDIR}" \
		--volume "$${WORKDIR}:/workdir" \
		--volume /var/run/docker.sock:/var/run/docker.sock \
		$(IMAGE_NAME)

exec: ## Execute a command in container (usage: make exec CMD="command")
	@docker exec -it $(CONTAINER_NAME) $(CMD)

copy-in: ## Copy file to container (usage: make copy-in SRC=local DST=/path)
	@docker cp $(SRC) $(CONTAINER_NAME):$(DST)

copy-out: ## Copy file from container (usage: make copy-out SRC=/path DST=local)
	@docker cp $(CONTAINER_NAME):$(SRC) $(DST)

##@ Cleanup

clean: down ## Stop container and prune Docker system
	@docker system prune -f

prune: ## Aggressive Docker cleanup (removes all unused images)
	@docker system prune -a -f

nuke: down ## Remove everything including volumes (DESTRUCTIVE)
	@echo "WARNING: This will remove all unused Docker data including volumes"
	@docker system prune -a --volumes -f

##@ Setup

init: ## Initial setup - create persistent directory structure
	@if [ -z "$${WORKDIR}" ]; then \
		echo "Error: WORKDIR environment variable must be set"; \
		echo "Usage: WORKDIR=/path/to/workspace make init"; \
		exit 1; \
	fi
	@mkdir -p "$${WORKDIR}/persistent"
	@echo "Created $${WORKDIR}/persistent"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Run: WORKDIR=$${WORKDIR} make up"
	@echo "  2. Enter container: make enter"
	@echo "  3. Run 'setup' to configure credentials"

check: ## Verify environment is ready
	@echo "=== Checking Prerequisites ==="
	@command -v docker >/dev/null 2>&1 && echo "✓ Docker installed" || echo "✗ Docker not found"
	@docker info >/dev/null 2>&1 && echo "✓ Docker running" || echo "✗ Docker not running"
	@test -n "$${WORKDIR}" && echo "✓ WORKDIR set: $${WORKDIR}" || echo "✗ WORKDIR not set"
	@if [ -n "$${WORKDIR}" ]; then \
		test -f "$${WORKDIR}/persistent/.env" && echo "✓ .env exists at $${WORKDIR}/persistent/.env" || echo "○ No .env yet (will be created by 'setup' in container)"; \
	fi
