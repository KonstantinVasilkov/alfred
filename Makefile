.PHONY: install test lint format typecheck pre-commit docker-build docker-up docker-down clean

# Workspace-wide commands
install:
	uv sync

test:
	uv run pytest apps/*/tests libs/*/tests -v

lint:
	uv run ruff check .

format:
	uv run ruff format .

typecheck:
	uv run mypy apps/ libs/

pre-commit:
	uv run pre-commit run --all-files

pre-commit-install:
	uv run pre-commit install

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

# Per-app commands
test-app:
	@if [ -z "$(APP)" ]; then echo "Usage: make test-app APP=<app_name>"; exit 1; fi
	uv run pytest apps/$(APP)/tests -v

lint-app:
	@if [ -z "$(APP)" ]; then echo "Usage: make lint-app APP=<app_name>"; exit 1; fi
	uv run ruff check apps/$(APP)

format-app:
	@if [ -z "$(APP)" ]; then echo "Usage: make format-app APP=<app_name>"; exit 1; fi
	uv run ruff format apps/$(APP)

typecheck-app:
	@if [ -z "$(APP)" ]; then echo "Usage: make typecheck-app APP=<app_name>"; exit 1; fi
	uv run mypy apps/$(APP)

run-app:
	@if [ -z "$(APP)" ]; then echo "Usage: make run-app APP=<app_name>"; exit 1; fi
	cd apps/$(APP) && uv run python -m $(APP).main

# Docker commands
docker-build-app:
	@if [ -z "$(APP)" ]; then echo "Usage: make docker-build-app APP=<app_name>"; exit 1; fi
	docker build -t alfred-$(APP):latest apps/$(APP)

docker-up:
	docker compose -f deploy/docker-compose.dev.yml up -d

docker-down:
	docker compose -f deploy/docker-compose.dev.yml down

docker-logs:
	docker compose -f deploy/docker-compose.dev.yml logs -f
