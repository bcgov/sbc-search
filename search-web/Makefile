.PHONY: setup
.PHONY: ci cd

PROJECT_NAME=search-web
DOCKER_NAME:=search-web

#################################################################################
# COMMANDS -- Setup                                                             #
#################################################################################
setup: ## Clean and Install npm dependencies
	npm ci

#################################################################################
# COMMANDS - CI                                                                 #
#################################################################################
ci: lint test

lint:  ## Run linting ofcode.
	npm run lint

test:  ## Unit testing
	npm run test:unit

#################################################################################
# COMMANDS - CD                                                                 #
#################################################################################
cd: build tag ## CD flow

local-build: ## NPM build
	npm run build

build: ## Build the docker container
	docker build . -t $(DOCKER_NAME) \
		--build-arg VCS_REF=$(shell git rev-parse --short HEAD) \
		--build-arg BUILD_DATE=$(shell date -u +"%Y-%m-%dT%H:%M:%SZ") \

build-nc: ## Build the docker container without caching
	docker build --no-cache -t $(PROJECT_NAME) .

# expects the terminal to be docker login
# expects export OPENSHIFT_DOCKER_REGISTRY=""
# expects export OPENSHIFT_REPOSITORY=""
# expects export OPENSHIFT_SA_TOKEN=""
# expects export OPENSHIFT_SA_NAME="github-cicd"
# expects export TAG_NAME="dev/test"
REGISTRY_IMAGE=$(OPENSHIFT_DOCKER_REGISTRY)/$(OPENSHIFT_REPOSITORY)-tools/$(DOCKER_NAME)
push: #build ## Push the docker container to the registry
	@echo "$(OPENSHIFT_SA_TOKEN)" | docker login $(OPENSHIFT_DOCKER_REGISTRY) -u $(OPENSHIFT_SA_NAME) --password-stdin ;\
    docker tag $(DOCKER_NAME) $(REGISTRY_IMAGE):latest ;\
    docker push $(REGISTRY_IMAGE):latest

tag: push #tag ## Push the docker container to the registry & tag
	docker tag $(REGISTRY_IMAGE):latest $(REGISTRY_IMAGE):$(TAG_NAME) ;\
    docker push $(REGISTRY_IMAGE):$(TAG_NAME)

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################
.PHONY: help

.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
