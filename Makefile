.PHONY: all
all: help

.PHONY: build
build:
	docker-compose up --build


.PHONY: up
up:
	docker-compose up -d

.PHONY: help
help:
	@echo "Makefile commands:"
	@echo "  make build - Build the Docker images"
	@echo "  make up    - Start the services in detached mode"
