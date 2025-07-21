.PHONY: help install test test-unit test-integration test-web test-coverage test-fast lint format clean run web-dev

help:
	@echo "ServiceNow Documentation Template Generator"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run all tests"
	@echo "  make test-unit     - Run unit tests only"
	@echo "  make test-integration - Run integration tests only"
	@echo "  make test-web      - Run web interface tests"
	@echo "  make test-coverage - Run tests with coverage report"
	@echo "  make test-fast     - Run fast tests (stop on first failure)"
	@echo "  make lint          - Run linters (flake8, mypy)"
	@echo "  make format        - Format code (black, isort)"
	@echo "  make clean         - Clean generated files and cache"
	@echo "  make run           - Run the CLI tool"
	@echo "  make web-dev       - Start development web server"

install:
	pip install -r requirements.txt

test:
	python run_tests.py all

test-unit:
	python run_tests.py unit

test-integration:
	python run_tests.py integration

test-web:
	python run_tests.py web

test-coverage:
	python run_tests.py coverage

test-fast:
	python run_tests.py fast

lint:
	python -m flake8 src tests --max-line-length=88 --exclude=venv,__pycache__,.git
	python -m mypy src --ignore-missing-imports

format:
	python -m black src tests --line-length=88
	python -m isort src tests --profile=black

web-dev:
	python start_web.py

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