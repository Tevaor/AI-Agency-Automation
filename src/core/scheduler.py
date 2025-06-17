"""
Task scheduler for managing and executing automation tasks.
"""
from typing import Any, Dict, List, Optional
import asyncio
import logging
from datetime import datetime
import uuid
from enum import Enum

from .automation import AutomationTask

logger = logging.getLogger(__name__)

class TaskStatus(Enum):
    """Enum for task status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskResult:
    """Class for storing task execution results."""
    
    def __init__(self, task_id: str, task: AutomationTask):
        self.task_id = task_id
        self.task = task
        self.status = TaskStatus.PENDING
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.result: Optional[Dict[str, Any]] = None
        self.error: Optional[str] = None
        self.retry_count = 0
        self.max_retries = 3

class TaskScheduler:
    """Scheduler for managing and executing automation tasks."""
    
    def __init__(self, max_concurrent_tasks: int = 10):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.tasks: Dict[str, TaskResult] = {}
        self.task_queue: asyncio.Queue = asyncio.Queue()
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.scheduler_task: Optional[asyncio.Task] = None
    
    async def start(self):
        """Start the task scheduler."""
        if self.scheduler_task is None:
            self.scheduler_task = asyncio.create_task(self._run_scheduler())
            logger.info("Task scheduler started")
    
    async def stop(self):
        """Stop the task scheduler."""
        if self.scheduler_task:
            self.scheduler_task.cancel()
            try:
                await self.scheduler_task
            except asyncio.CancelledError:
                pass
            self.scheduler_task = None
            logger.info("Task scheduler stopped")
    
    async def submit_task(self, task: AutomationTask) -> str:
        """Submit a new task for execution."""
        task_id = str(uuid.uuid4())
        task_result = TaskResult(task_id, task)
        self.tasks[task_id] = task_result
        
        # Start the task immediately if we have capacity
        if len(self.running_tasks) < self.max_concurrent_tasks:
            task_result.status = TaskStatus.RUNNING
            task_result.start_time = datetime.now()
            task = asyncio.create_task(self._execute_task(task_id))
            self.running_tasks[task_id] = task
        else:
            await self.task_queue.put(task_id)
        
        logger.info(f"Task {task_id} submitted for execution")
        return task_id
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of a task."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task_result = self.tasks[task_id]
        return {
            "task_id": task_id,
            "status": task_result.status.value,
            "start_time": task_result.start_time.isoformat() if task_result.start_time else None,
            "end_time": task_result.end_time.isoformat() if task_result.end_time else None,
            "result": task_result.result,
            "error": task_result.error,
            "retry_count": task_result.retry_count
        }
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a running task."""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task_result = self.tasks[task_id]
        if task_result.status == TaskStatus.RUNNING:
            if task_id in self.running_tasks:
                self.running_tasks[task_id].cancel()
                task_result.status = TaskStatus.CANCELLED
                task_result.end_time = datetime.now()
                logger.info(f"Task {task_id} cancelled")
                return True
        return False
    
    async def _run_scheduler(self):
        """Run the task scheduler loop."""
        while True:
            try:
                # Wait for a task to be available
                task_id = await self.task_queue.get()
                
                # Check if we can run more tasks
                while len(self.running_tasks) >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                
                # Start the task
                task_result = self.tasks[task_id]
                task_result.status = TaskStatus.RUNNING
                task_result.start_time = datetime.now()
                
                # Create and start the task
                task = asyncio.create_task(self._execute_task(task_id))
                self.running_tasks[task_id] = task
                
                # Remove the task from the queue
                self.task_queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                await asyncio.sleep(0.1)
    
    async def _execute_task(self, task_id: str):
        """Execute a task and handle retries."""
        task_result = self.tasks[task_id]
        
        try:
            # Execute the task
            result = await task_result.task.execute()
            task_result.status = TaskStatus.COMPLETED
            task_result.result = result
            
        except Exception as e:
            task_result.error = str(e)
            
            # Handle retries
            if task_result.retry_count < task_result.max_retries:
                task_result.retry_count += 1
                task_result.status = TaskStatus.PENDING
                await self.task_queue.put(task_id)
                logger.info(f"Task {task_id} scheduled for retry {task_result.retry_count}")
            else:
                task_result.status = TaskStatus.FAILED
                logger.error(f"Task {task_id} failed after {task_result.retry_count} retries")
        
        finally:
            task_result.end_time = datetime.now()
            if task_id in self.running_tasks:
                del self.running_tasks[task_id] 