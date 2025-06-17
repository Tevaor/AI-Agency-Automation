"""
Pytest configuration file for setting up the test environment.
"""
import os
import pytest
import asyncio
from typing import Generator

# Set up test environment variables
os.environ["TEST_GCP_PROJECT_ID"] = "test-project"
os.environ["TEST_SSH_HOST"] = "localhost"
os.environ["TEST_SSH_USERNAME"] = "testuser"
os.environ["TEST_SSH_KEY_PATH"] = "~/.ssh/id_rsa"
os.environ["TEST_API_BASE_URL"] = "http://localhost:8000"

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close() 