"""
Main FastAPI application for the AI automation platform.
"""
from typing import Any, Dict, List, Optional
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.core.automation import AutomationTask, GCPAutomationTask, SSHAutomationTask, APIAutomationTask
from src.agents.it_operations_agent import ITOperationsAgent, echo_tool_instance, monitor_system_health_tool_instance
from src.consent.manager import ConsentManager, ConsentRequest, ConsentResponse
from src.gcp.manager import GCPManager
from src.security.zero_trust import ZeroTrustManager, SecurityConfig, User, Token, UserResponse
from src.core.tasks import GCPVMCreationTask, SSHCommandTask, APIRestartServiceTask
from src.core.scheduler import TaskScheduler

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Automation Platform",
    description="An integrated AI engineering solution for automation and IT operations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5000"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], # Allow necessary HTTP methods
    allow_headers=["*"],  # Allow all headers for now
)

# Mount static files for the frontend
try:
    app.mount("/static", StaticFiles(directory="frontend/dist"), name="static")
except Exception as e:
    logger.warning(f"Could not mount static files: {e}")

# Initialize security
security_config = SecurityConfig(
    jwt_secret=os.getenv("JWT_SECRET_KEY", "your-secret-key"),
    jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
    access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
    refresh_token_expire_days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")),
    password_hash_rounds=int(os.getenv("PASSWORD_HASH_ROUNDS", "12"))
)
security_manager = ZeroTrustManager(security_config)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize managers
consent_manager = ConsentManager(os.getenv("DATABASE_URL", "sqlite:///./consent.db"))
gcp_manager = GCPManager(
    project_id=os.getenv("GOOGLE_CLOUD_PROJECT", ""),
    credentials_path=os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)

# Initialize IT operations agent
it_agent = ITOperationsAgent(tools=[echo_tool_instance, monitor_system_health_tool_instance])

# Initialize task scheduler
task_scheduler = TaskScheduler(max_concurrent_tasks=10)

# Models
class UserCreate(BaseModel):
    """Model for user creation."""
    username: str
    email: str
    password: str
    roles: Optional[List[str]] = None
    permissions: Optional[List[str]] = None

class TaskRequest(BaseModel):
    """Model for task requests."""
    task_type: str
    parameters: Dict[str, Any]

# Root endpoint to serve the React app
@app.get("/")
async def serve_frontend():
    """Serve the React frontend."""
    try:
        return FileResponse("frontend/dist/index.html")
    except FileNotFoundError:
        return {"message": "Frontend not found. Please build the frontend first."}

# Security dependencies
async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """Get the current user from the token."""
    try:
        payload = security_manager.verify_token(token)
        return UserResponse(
            id=payload["sub"],
            username=payload["username"],
            email=payload["email"],
            roles=payload.get("roles", []),
            permissions=payload.get("permissions", []),
            is_active=payload.get("is_active", True),
            is_superuser=payload.get("is_superuser", False)
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )

# Authentication endpoints
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login endpoint."""
    # In a real implementation, you would verify the user's credentials
    # For this example, we'll create a mock user
    user = User(
        id="1",
        username=form_data.username,
        email=f"{form_data.username}@example.com",
        hashed_password=""
    )
    return security_manager.create_tokens(user)

# User management endpoints
@app.post("/users", response_model=UserResponse)
async def create_user(user_data: UserCreate):
    """Create a new user."""
    return security_manager.create_user(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        roles=user_data.roles,
        permissions=user_data.permissions
    )

# Consent management endpoints
@app.post("/consent/request", response_model=ConsentResponse)
async def request_consent(
    request: ConsentRequest,
    current_user: User = Depends(get_current_user)
):
    """Request user consent."""
    return consent_manager.request_consent(request)

@app.post("/consent/{consent_id}/grant", response_model=ConsentResponse)
async def grant_consent(
    consent_id: int,
    current_user: User = Depends(get_current_user)
):
    """Grant consent."""
    return consent_manager.grant_consent(consent_id)

@app.post("/consent/{consent_id}/deny", response_model=ConsentResponse)
async def deny_consent(
    consent_id: int,
    current_user: User = Depends(get_current_user)
):
    """Deny consent."""
    return consent_manager.deny_consent(consent_id)

# GCP management endpoints
@app.post("/gcp/instances", response_model=Dict[str, Any])
async def create_vm_instance(
    instance_name: str,
    machine_type: str,
    zone: str,
    current_user: User = Depends(get_current_user)
):
    """Create a new VM instance."""
    return await gcp_manager.create_vm_instance(
        instance_name=instance_name,
        machine_type=machine_type,
        zone=zone
    )

@app.delete("/gcp/instances/{instance_name}", response_model=Dict[str, Any])
async def delete_vm_instance(
    instance_name: str,
    zone: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a VM instance."""
    return await gcp_manager.delete_vm_instance(
        instance_name=instance_name,
        zone=zone
    )

# IT operations endpoints
@app.post("/it/monitor", response_model=Dict[str, Any])
async def monitor_system_health(
    current_user: User = Depends(get_current_user)
):
    """Monitor system health."""
    return await it_agent.monitor_system_health()

@app.post("/it/incidents", response_model=Dict[str, Any])
async def handle_incident(
    incident_details: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Handle an IT incident."""
    return await it_agent.handle_incident(incident_details)

@app.post("/it/resources", response_model=Dict[str, Any])
async def provision_resources(
    resource_spec: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Provision IT resources."""
    return await it_agent.provision_resources(resource_spec)

# Automation task endpoints
@app.post("/automation/gcp/vm", response_model=Dict[str, Any])
async def create_vm_task(
    project_id: str,
    instance_name: str,
    machine_type: str,
    zone: str,
    current_user: User = Depends(get_current_user)
):
    """Submit a task to create a new VM instance."""
    task = GCPVMCreationTask(
        project_id=project_id,
        instance_name=instance_name,
        machine_type=machine_type,
        zone=zone
    )
    task_id = await task_scheduler.submit_task(task)
    return {"task_id": task_id}

@app.post("/automation/ssh/command", response_model=Dict[str, Any])
async def execute_ssh_command(
    host: str,
    username: str,
    key_path: str,
    command: str,
    timeout: int = 30,
    current_user: User = Depends(get_current_user)
):
    """Submit a task to execute an SSH command."""
    task = SSHCommandTask(
        host=host,
        username=username,
        key_path=key_path,
        command=command,
        timeout=timeout
    )
    task_id = await task_scheduler.submit_task(task)
    return {"task_id": task_id}

@app.post("/automation/api/restart-service", response_model=Dict[str, Any])
async def restart_service(
    base_url: str,
    service_name: str,
    headers: Optional[Dict[str, str]] = None,
    current_user: User = Depends(get_current_user)
):
    """Submit a task to restart a service."""
    task = APIRestartServiceTask(
        base_url=base_url,
        service_name=service_name,
        headers=headers
    )
    task_id = await task_scheduler.submit_task(task)
    return {"task_id": task_id}

# Task management endpoints
@app.get("/automation/tasks/{task_id}", response_model=Dict[str, Any])
async def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get the status of a task."""
    return await task_scheduler.get_task_status(task_id)

@app.post("/automation/tasks/{task_id}/cancel", response_model=Dict[str, Any])
async def cancel_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    """Cancel a running task."""
    success = await task_scheduler.cancel_task(task_id)
    return {"success": success}

# Chatbot endpoint
@app.post("/chat", response_model=Dict[str, Any])
async def chat_with_agent(
    message: Dict[str, str],
    # current_user: User = Depends(get_current_user) # Temporarily disable authentication
):
    """Interact with the IT Operations Agent through the chatbot."""
    user_input = message.get("message")
    if not user_input:
        raise HTTPException(status_code=400, detail="Message not provided")
    
    response = await it_agent.execute_task({"input": user_input})
    return {"response": response.get("result", "No response from agent.")}

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.on_event("startup")
async def startup_event():
    """Start the task scheduler on application startup."""
    await task_scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Stop the task scheduler on application shutdown."""
    await task_scheduler.stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 