"""
Integration tests for the automation platform.
"""
import asyncio
import os
import pytest
from datetime import datetime
from typing import Dict, Any
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from core.tasks import GCPVMCreationTask, SSHCommandTask, APIRestartServiceTask
from core.scheduler import TaskScheduler, TaskStatus
from security.zero_trust import ZeroTrustManager, SecurityConfig, User

# Test configuration
TEST_CONFIG = {
    "gcp": {
        "project_id": "test-project",
        "instance_name": "test-instance",
        "machine_type": "n1-standard-1",
        "zone": "us-central1-a"
    },
    "ssh": {
        "host": "localhost",
        "username": "testuser",
        "key_path": "test_key.pem",
        "command": "echo 'test'"
    },
    "api": {
        "base_url": "http://localhost:8000",
        "service_name": "test-service"
    }
}

@pytest.fixture
def mock_gcp_client():
    """Mock GCP client for testing."""
    with patch('google.auth.default', return_value=(MagicMock(), 'test-project')), \
         patch('google.cloud.compute_v1.services.instances.InstancesClient') as mock:
        instance = mock.return_value
        instance.insert = AsyncMock(return_value=MagicMock())
        yield instance

@pytest.fixture
def mock_ssh_client():
    """Create a mock SSH client."""
    client = MagicMock()
    client.set_missing_host_key_policy = MagicMock()
    client.connect = MagicMock()
    
    # Mock stdin, stdout, stderr
    mock_stdin = MagicMock()
    mock_stdout = MagicMock()
    mock_stderr = MagicMock()
    
    # Configure stdout and stderr
    mock_stdout.read.return_value = b"test output"
    mock_stderr.read.return_value = b""
    
    # Configure exec_command to return the mocked streams
    client.exec_command.return_value = (mock_stdin, mock_stdout, mock_stderr)
    
    return client

@pytest.fixture
def mock_api_client():
    """Mock API client for testing."""
    with patch('requests.Session') as mock:
        session = mock.return_value
        session.post = MagicMock(return_value=MagicMock(status_code=200))
        yield session

@pytest_asyncio.fixture
async def task_scheduler():
    """Create a task scheduler for testing."""
    scheduler = TaskScheduler()
    await scheduler.start()
    yield scheduler
    await scheduler.stop()

@pytest.fixture
def test_user():
    """Create a test user."""
    return User(
        id="test-user",
        username="testuser",
        email="test@example.com",
        hashed_password="hashed_password",
        roles='["admin"]',
        permissions='["admin"]'
    )

@pytest.mark.asyncio
async def test_gcp_vm_creation(task_scheduler, test_user, mock_gcp_client):
    """Test GCP VM creation task."""
    # Create and submit task
    task = GCPVMCreationTask(
        project_id=TEST_CONFIG["gcp"]["project_id"],
        instance_name=TEST_CONFIG["gcp"]["instance_name"],
        machine_type=TEST_CONFIG["gcp"]["machine_type"],
        zone=TEST_CONFIG["gcp"]["zone"],
        compute_client=mock_gcp_client
    )
    task_id = await task_scheduler.submit_task(task)
    
    # Wait for task completion
    max_wait_time = 60  # 1 minute
    start_time = datetime.now()
    while True:
        status = await task_scheduler.get_task_status(task_id)
        if status["status"] in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value]:
            break
        if (datetime.now() - start_time).seconds > max_wait_time:
            pytest.fail("Task execution timed out")
        await asyncio.sleep(1)
    
    # Verify task result
    assert status["status"] == TaskStatus.COMPLETED.value
    mock_gcp_client.insert.assert_called_once()

@pytest.mark.asyncio
async def test_ssh_command(task_scheduler, test_user, mock_ssh_client):
    """Test SSH command execution task."""
    # Create and submit task
    task = SSHCommandTask(
        host=TEST_CONFIG["ssh"]["host"],
        username=TEST_CONFIG["ssh"]["username"],
        key_path=TEST_CONFIG["ssh"]["key_path"],
        command=TEST_CONFIG["ssh"]["command"],
        ssh_client=mock_ssh_client
    )
    task_id = await task_scheduler.submit_task(task)
    
    # Wait for task completion
    max_wait_time = 60  # 1 minute
    start_time = datetime.now()
    while True:
        status = await task_scheduler.get_task_status(task_id)
        if status["status"] in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value]:
            break
        if (datetime.now() - start_time).seconds > max_wait_time:
            pytest.fail("Task execution timed out")
        await asyncio.sleep(1)
    
    # Verify task result
    assert status["status"] == TaskStatus.COMPLETED.value
    mock_ssh_client.connect.assert_called_once()

@pytest.mark.asyncio
async def test_api_service_restart(task_scheduler, test_user, mock_api_client):
    """Test API service restart task."""
    # Create and submit task
    task = APIRestartServiceTask(
        base_url=TEST_CONFIG["api"]["base_url"],
        service_name=TEST_CONFIG["api"]["service_name"]
    )
    task_id = await task_scheduler.submit_task(task)
    
    # Wait for task completion
    max_wait_time = 60  # 1 minute
    start_time = datetime.now()
    while True:
        status = await task_scheduler.get_task_status(task_id)
        if status["status"] in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value]:
            break
        if (datetime.now() - start_time).seconds > max_wait_time:
            pytest.fail("Task execution timed out")
        await asyncio.sleep(1)
    
    # Verify task result
    assert status["status"] == TaskStatus.COMPLETED.value
    mock_api_client.post.assert_called_once_with(
        f"{TEST_CONFIG['api']['base_url']}/services/{TEST_CONFIG['api']['service_name']}/restart"
    )

@pytest.mark.asyncio
async def test_task_cancellation(task_scheduler, test_user, mock_ssh_client):
    """Test task cancellation."""
    # Create and submit a long-running task
    task = SSHCommandTask(
        host=TEST_CONFIG["ssh"]["host"],
        username=TEST_CONFIG["ssh"]["username"],
        key_path=TEST_CONFIG["ssh"]["key_path"],
        command="sleep 5",  # Shorter sleep time
        ssh_client=mock_ssh_client
    )
    task_id = await task_scheduler.submit_task(task)

    # Wait for the task to be in RUNNING state
    max_wait = 5  # Maximum wait time in seconds
    start_time = datetime.now()
    while (datetime.now() - start_time).total_seconds() < max_wait:
        status = await task_scheduler.get_task_status(task_id)
        if status["status"] == TaskStatus.RUNNING.value:
            break
        await asyncio.sleep(0.1)
    else:
        pytest.fail("Task did not start running within the expected time")

    # Cancel the task
    assert await task_scheduler.cancel_task(task_id)

    # Verify task is cancelled
    status = await task_scheduler.get_task_status(task_id)
    assert status["status"] == TaskStatus.CANCELLED.value

@pytest.mark.asyncio
async def test_concurrent_tasks(task_scheduler, test_user, mock_ssh_client):
    """Test concurrent task execution."""
    # Submit multiple tasks
    task_ids = []
    for i in range(3):
        task = SSHCommandTask(
            host=TEST_CONFIG["ssh"]["host"],
            username=TEST_CONFIG["ssh"]["username"],
            key_path=TEST_CONFIG["ssh"]["key_path"],
            command=f"echo 'Test command {i}'",
            ssh_client=mock_ssh_client
        )
        task_id = await task_scheduler.submit_task(task)
        task_ids.append(task_id)

    # Wait for all tasks to complete
    max_wait_time = 60  # 1 minute
    start_time = datetime.now()
    while True:
        all_completed = True
        for task_id in task_ids:
            status = await task_scheduler.get_task_status(task_id)
            if status["status"] not in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value]:
                all_completed = False
                break
        if all_completed:
            break
        if (datetime.now() - start_time).seconds > max_wait_time:
            pytest.fail("Task execution timed out")
        await asyncio.sleep(1)

    # Verify all tasks completed successfully
    for task_id in task_ids:
        status = await task_scheduler.get_task_status(task_id)
        assert status["status"] == TaskStatus.COMPLETED.value

    # Verify SSH client was called for each task
    assert mock_ssh_client.connect.call_count == 3
    assert mock_ssh_client.exec_command.call_count == 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 