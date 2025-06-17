@echo off

REM Create and activate virtual environment if it doesn't exist
if not exist venv (
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install test dependencies
pip install -r tests/requirements-test.txt

REM Run tests with PYTHONPATH set inline
set PYTHONPATH=%CD%\src && pytest tests/ -v

REM Deactivate virtual environment
call venv\Scripts\deactivate.bat 