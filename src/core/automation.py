"""
Core automation module providing base classes and utilities for the automation framework.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime
import uuid

import paramiko
import requests
from google.cloud import compute_v1
from google.cloud import storage
from google.cloud.compute_v1.services.instances import InstancesClient
from google.cloud.compute_v1.types import Instance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TaskResult:
    """Class representing the result of a task execution."""
    
    def __init__(self, success: bool, result: Optional[Dict[str, Any]] = None, error: Optional[str] = None):
        """Initialize task result."""
        self.success = success
        self.result = result or {}
        self.error = error
        self.timestamp = datetime.now()

class AutomationTask:
    """Base class for automation tasks."""
    
    def __init__(self, task_type: str, task_id: str, parameters: Dict[str, Any]):
        """Initialize automation task."""
        self.task_type = task_type
        self.task_id = task_id
        self.parameters = parameters
        self.created_at = datetime.now()
        self.updated_at = self.created_at
        self.status = "pending"
        self.result = None
        self.error = None

    async def execute(self) -> TaskResult:
        """Execute the task. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement execute()")

    def validate_parameters(self) -> bool:
        """Validate task parameters. Can be overridden by subclasses."""
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary representation."""
        return {
            "task_type": self.task_type,
            "task_id": self.task_id,
            "parameters": self.parameters,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "status": self.status,
            "result": self.result,
            "error": self.error
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AutomationTask':
        """Create task from dictionary representation."""
        task = cls(
            task_type=data["task_type"],
            task_id=data["task_id"],
            parameters=data["parameters"]
        )
        task.created_at = datetime.fromisoformat(data["created_at"])
        task.updated_at = datetime.fromisoformat(data["updated_at"])
        task.status = data["status"]
        task.result = data["result"]
        task.error = data["error"]
        return task

class GCPAutomationTask(AutomationTask):
    """Base class for GCP-specific automation tasks."""
    
    def __init__(self, name: str, description: str, project_id: str):
        super().__init__(name, description)
        self.project_id = project_id
        self.compute_client = InstancesClient()
        self.storage_client = storage.Client(project=project_id)
    
    async def execute(self) -> Dict[str, Any]:
        """Execute GCP automation task."""
        try:
            self.start_time = datetime.now()
            result = await self._execute_gcp_task()
            self.status = "completed"
            return result
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            raise
        finally:
            self.end_time = datetime.now()
            self.log_execution()
    
    @abstractmethod
    async def _execute_gcp_task(self) -> Dict[str, Any]:
        """Execute the specific GCP task implementation."""
        pass

class SSHAutomationTask(AutomationTask):
    """Base class for SSH-based automation tasks."""
    
    def __init__(self, name: str, description: str, host: str, username: str, key_path: str):
        super().__init__(name, description)
        self.host = host
        self.username = username
        self.key_path = key_path
        self.client: Optional[paramiko.SSHClient] = None
    
    async def execute(self) -> Dict[str, Any]:
        """Execute SSH automation task."""
        try:
            self.start_time = datetime.now()
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                hostname=self.host,
                username=self.username,
                key_filename=self.key_path
            )
            result = await self._execute_ssh_task()
            self.status = "completed"
            return result
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            raise
        finally:
            if self.client:
                self.client.close()
            self.end_time = datetime.now()
            self.log_execution()
    
    @abstractmethod
    async def _execute_ssh_task(self) -> Dict[str, Any]:
        """Execute the specific SSH task implementation."""
        pass

class APIAutomationTask(AutomationTask):
    """Base class for API-based automation tasks."""
    
    def __init__(self, name: str, description: str, base_url: str, headers: Optional[Dict[str, str]] = None):
        super().__init__(name, description)
        self.base_url = base_url
        self.headers = headers or {}
        self.session = requests.Session()
    
    async def execute(self) -> Dict[str, Any]:
        """Execute API automation task."""
        try:
            self.start_time = datetime.now()
            result = await self._execute_api_task()
            self.status = "completed"
            return result
        except Exception as e:
            self.status = "failed"
            self.error = str(e)
            raise
        finally:
            self.session.close()
            self.end_time = datetime.now()
            self.log_execution()
    
    @abstractmethod
    async def _execute_api_task(self) -> Dict[str, Any]:
        """Execute the specific API task implementation."""
        pass 