#!/bin/bash

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install test dependencies
pip install -r tests/requirements-test.txt

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Deactivate virtual environment
deactivate 