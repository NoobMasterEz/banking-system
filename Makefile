### THIS IST THE VERSION WITH docker-compose
# grep the version from the mix file
VERSION=$(shell ./version.sh)
NAME=$(shell docker ps --format "{{.Names}}" | grep Web)

# Filenames
DEV_COMPOSE_FILE := docker/docker-compose.yml

# HELP
# This will output the help for each taskl
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# DOCKER TASKS
# Build the container
build: ## Build the release and develoment container. The development
	docker-compose -f $(DEV_COMPOSE_FILE) up -d --build $(c)

bash: ## Run container in development mode
	docker exec -it $(NAME) bash

dev: ## Run container in development mode
	docker-compose build --no-cache $(c) && docker-compose run $(c)

start: ## Start the project
	${INFO} "Start local..."
	docker-compose -f $(DEV_COMPOSE_FILE) start $(c)

up: ## Spin up the containers
	docker-compose -f $(DEV_COMPOSE_FILE) up -d  $(c)

update: ## Spin up the containers
	docker-compose -f $(DEV_COMPOSE_FILE) pull $(c)

stop: ## Stop running containers
	docker-compose -f $(DEV_COMPOSE_FILE) stop $(c)

restart: ## restart containers
	docker-compose -f $(DEV_COMPOSE_FILE) stop $(c) && docker-compose -f $(DEV_COMPOSE_FILE) up -d $(c)

rm: ## Stop and remove running containers
	docker-compose -f $(DEV_COMPOSE_FILE) down -v $(c)

ps: ## Process running containers
	docker-compose -f $(DEV_COMPOSE_FILE) ps

logs: ## Logs process running containers
	docker-compose -f $(DEV_COMPOSE_FILE) logs --tail=100 -f $(c)

clean: ## Clean the generated/compiles files
	echo "nothing clean ..."

repo-login: ## Auto login to AWS-ECR unsing aws-cli
	@eval $(CMD_REPOLOGIN)

version: ## output to version
	@echo $(VERSION)