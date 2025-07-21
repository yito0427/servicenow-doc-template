.PHONY: help install test lint format clean run

help:
	@echo "ServiceNow Documentation Template Generator"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies with Poetry"
	@echo "  make test       - Run tests with coverage"
	@echo "  make lint       - Run linters (flake8, mypy)"
	@echo "  make format     - Format code (black, isort)"
	@echo "  make clean      - Clean generated files and cache"
	@echo "  make run        - Run the CLI tool"

install:
	poetry install

test:
	poetry run pytest

lint:
	poetry run flake8 src tests
	poetry run mypy src

format:
	poetry run black src tests
	poetry run isort src tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf dist/ build/

run:
	poetry run servicenow-doc