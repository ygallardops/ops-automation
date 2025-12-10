# Makefile para ops-automation

# Variables
PYTHON = python
PIP = pip

.PHONY: help install format lint test clean

help:  ## Muestra este mensaje de ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instala todas las dependencias
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	$(PIP) install -e .

format: ## Formatea el código automáticamente con Black e Isort
	black src tests
	isort src tests

lint: ## Verifica el estilo del código (sin modificarlo)
	flake8 src tests --max-line-length=88 --ignore=E203,W503
	black --check src tests

test: ## Ejecuta los tests unitarios
	pytest

clean: ## Limpia archivos temporales y caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf build dist *.egg-info
