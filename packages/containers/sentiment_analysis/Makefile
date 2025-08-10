# Makefile for Sentiment Analysis Project
# Usage: make <target>

.PHONY: help test test-llm test-sentiment test-all test-coverage test-lint clean install

# Default target
help:
	@echo "Available commands:"
	@echo "  test          - Run all tests"
	@echo "  test-llm      - Run LLM classifier tests only"
	@echo "  test-sentiment - Run sentiment analysis tests only"
	@echo "  test-all      - Run all tests with verbose output"
	@echo "  test-coverage - Run tests with coverage report"
	@echo "  test-lint     - Run linting checks"
	@echo "  install       - Install dependencies"
	@echo "  clean         - Clean up cache files"
	@echo "  help          - Show this help message"

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 black

# Run all tests
test:
	@echo "Running all tests..."
	python -m pytest tests/ -v

# Run LLM classifier tests only
test-llm:
	@echo "Running LLM classifier tests..."
	python -m pytest tests/test_llm_classifier.py -v

# Run sentiment analysis tests only
test-sentiment:
	@echo "Running sentiment analysis tests..."
	python -m pytest tests/test_sentiment_analysis.py -v

# Run all tests with verbose output
test-all:
	@echo "Running all tests with verbose output..."
	python -m pytest tests/ -vv --tb=short

# Run tests with coverage report
test-coverage:
	@echo "Running tests with coverage report..."
	python -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

# Run linting checks
test-lint:
	@echo "Running linting checks..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 . --max-line-length=79 --ignore=E501,W503; \
	else \
		echo "flake8 not found. Install with: pip install flake8"; \
	fi
	@if command -v black >/dev/null 2>&1; then \
		echo "Checking code formatting with black..."; \
		black --check --line-length=79 .; \
	else \
		echo "black not found. Install with: pip install black"; \
	fi

# Format code with black
format:
	@echo "Formatting code with black..."
	@if command -v black >/dev/null 2>&1; then \
		black --line-length=79 .; \
	else \
		echo "black not found. Install with: pip install black"; \
	fi

# Clean up cache files
clean:
	@echo "Cleaning up cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true

# Run tests in Docker (if Dockerfile exists)
test-docker:
	@echo "Building and running tests in Docker..."
	@if [ -f Dockerfile ]; then \
		docker build -t sentiment-analysis-test .; \
		docker run --rm sentiment-analysis-test python -m pytest tests/ -v; \
	else \
		echo "Dockerfile not found"; \
	fi

# Quick test run (fastest)
test-quick:
	@echo "Running quick test suite..."
	python -m pytest tests/ -x --tb=no

# Test with specific markers (if you add pytest markers later)
test-unit:
	@echo "Running unit tests..."
	python -m pytest tests/ -m "unit" -v

test-integration:
	@echo "Running integration tests..."
	python -m pytest tests/ -m "integration" -v

# Run VADER classifier tests only
test-vader:
	@echo "Running VADER classifier tests..."
	python -m pytest tests/test_vader_classifier.py -v

# Development setup
dev-setup: install
	@echo "Setting up development environment..."
	@echo "Development setup complete!"

# Show test statistics
test-stats:
	@echo "Test statistics:"
	@python -m pytest tests/ --collect-only -q | wc -l | xargs echo "Total test files:"
	@python -m pytest tests/ --collect-only -q | grep "::" | wc -l | xargs echo "Total test functions:" 