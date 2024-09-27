.PHONY: all run tests lint

WORDDIR=.
BLACKFLAGS=--target-version=py312

all: run tests lint

# tests:
# 	@echo "Running tests..."
# 	@poetry run pytest $(WORDDIR)/tests

build:
	@echo "Building all Docker images using Docker Compose..."
	@docker-compose build
	@echo "All Docker images built successfully"

run:
	@echo "Starting server..."
	@docker-compose up

lint:
	@echo "Linting..."
	@poetry run black $(WORDDIR) $(BLACKFLAGS)
	@echo "Linting done"