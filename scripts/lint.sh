#!/bin/bash
# Run all linting and formatting tools

echo "Running ruff check..."
uv run ruff check --fix .

echo "Running ruff format..."
uv run ruff format .

echo "Running mypy..."
uv run mypy .

echo "Running tests..."
uv run pytest

echo "All checks complete!"