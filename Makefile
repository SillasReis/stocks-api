.PHONY: install run test clean build-image deploy down

UV = uv
PYTHON = $(UV) run python
PYTEST = $(PYTHON) -m pytest
DOCKER_COMPOSE = docker compose

install:
	$(UV) sync --frozen --dev

run:
	$(PYTHON) -m src.api

test:
	$(PYTEST) tests/ -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

build-image:
	docker build -t stocks-api:0.1.0 .

deploy: build-image
	$(DOCKER_COMPOSE) -f docker-compose.yaml up --build -d

down:
	$(DOCKER_COMPOSE) -f docker-compose.yaml down -v
