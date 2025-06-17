SET "PYTHONPATH=%~dp0"
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 