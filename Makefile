# Filenames
DEV_COMPOSE_FILE := docker/dev/docker-compose.yml

# HELP
# This will output the help for each taskl
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# DOCKER TASKS
# Build the container
build: ## Build the release and develoment container. The development
	docker-compose -f $(DEV_COMPOSE_FILE) up -d --build $(target)

ssh: ## Run container in development mode
	docker exec -it $(c) $(user)

start: ## Start the project
	docker-compose -f $(DEV_COMPOSE_FILE) up -d $(target)

up: ## Spin up the containers
	docker-compose -f $(DEV_COMPOSE_FILE) up -d $(target)

update: ## Spin up the containers
	docker-compose -f $(DEV_COMPOSE_FILE) pull $(target)

stop: ## Stop running containers
	docker-compose -f $(DEV_COMPOSE_FILE) stop $(target)

restart: ## restart containers
	docker-compose -f $(DEV_COMPOSE_FILE) stop $(target) && docker-compose -f $(DEV_COMPOSE_FILE) up -d $(target)

rm: ## Stop and remove running containers
	docker-compose -f $(DEV_COMPOSE_FILE) down -v $(target)

ps: ## Process running containers
	docker-compose -f $(DEV_COMPOSE_FILE) ps

logs: ## Logs process running containers
	docker-compose -f $(DEV_COMPOSE_FILE) logs --tail=100 -f $(target)

clean: ## Clean the generated/compiles files
	echo "nothing clean ..."

list:
	docker ps -all
	docker images
	docker network ls

