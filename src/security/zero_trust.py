"""
Zero-trust security implementation for the automation platform.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import logging
import jwt
from jwt.exceptions import InvalidTokenError
import bcrypt
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base import Base
from pydantic import BaseModel, Field
from passlib.context import CryptContext
import json
import os

logger = logging.getLogger(__name__)

class SecurityConfig(BaseModel):
    """Security configuration model."""
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    password_hash_rounds: int = 12

class User(Base):
    """User model for authentication."""
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    roles = Column(String, nullable=False, default='[]')
    permissions = Column(String, nullable=False, default='[]')

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool = True
    is_superuser: bool = False
    roles: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)

    class Config:
        from_attributes = True

class Token(BaseModel):
    """Token model for authentication."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime

class ZeroTrustManager:
    """Manager class for zero-trust security implementation."""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
    
    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        roles: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None
    ) -> User:
        """Create a new user with hashed password."""
        hashed_password = self._hash_password(password)
        return User(
            id=str(datetime.utcnow().timestamp()),
            username=username,
            email=email,
            hashed_password=hashed_password,
            roles=roles or [],
            permissions=permissions or []
        )
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return bcrypt.checkpw(
            plain_password.encode(),
            hashed_password.encode()
        )
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        salt = bcrypt.gensalt(rounds=self.config.password_hash_rounds)
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    def create_tokens(self, user: User) -> Token:
        """Create access and refresh tokens for a user."""
        access_token_expires = datetime.utcnow() + timedelta(
            minutes=self.config.access_token_expire_minutes
        )
        refresh_token_expires = datetime.utcnow() + timedelta(
            days=self.config.refresh_token_expire_days
        )
        
        access_token_data = {
            "sub": user.id,
            "username": user.username,
            "email": user.email,
            "roles": user.roles,
            "permissions": user.permissions,
            "exp": access_token_expires
        }
        
        refresh_token_data = {
            "sub": user.id,
            "exp": refresh_token_expires
        }
        
        access_token = jwt.encode(
            access_token_data,
            self.config.jwt_secret,
            algorithm=self.config.jwt_algorithm
        )
        
        refresh_token = jwt.encode(
            refresh_token_data,
            self.config.jwt_secret,
            algorithm=self.config.jwt_algorithm
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=access_token_expires
        )
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.config.jwt_secret,
                algorithms=[self.config.jwt_algorithm]
            )
            return payload
        except InvalidTokenError as e:
            logger.error(f"Token verification failed: {str(e)}")
            raise
    
    def refresh_access_token(self, refresh_token: str) -> Token:
        """Create a new access token using a refresh token."""
        try:
            payload = self.verify_token(refresh_token)
            user_id = payload["sub"]
            
            # In a real implementation, you would fetch the user from the database
            # For this example, we'll create a mock user
            user = User(
                id=user_id,
                username="user",
                email="user@example.com",
                hashed_password=""
            )
            
            return self.create_tokens(user)
        except Exception as e:
            logger.error(f"Failed to refresh access token: {str(e)}")
            raise
    
    def check_permission(self, token: str, required_permission: str) -> bool:
        """Check if a token has a specific permission."""
        try:
            payload = self.verify_token(token)
            user_permissions = payload.get("permissions", [])
            return required_permission in user_permissions
        except Exception as e:
            logger.error(f"Permission check failed: {str(e)}")
            return False
    
    def check_role(self, token: str, required_role: str) -> bool:
        """Check if a token has a specific role."""
        try:
            payload = self.verify_token(token)
            user_roles = payload.get("roles", [])
            return required_role in user_roles
        except Exception as e:
            logger.error(f"Role check failed: {str(e)}")
            return False
    
    def validate_request(
        self,
        token: str,
        required_permissions: Optional[List[str]] = None,
        required_roles: Optional[List[str]] = None
    ) -> bool:
        """Validate a request based on token, permissions, and roles."""
        try:
            payload = self.verify_token(token)
            
            # Check permissions
            if required_permissions:
                user_permissions = payload.get("permissions", [])
                if not all(perm in user_permissions for perm in required_permissions):
                    return False
            
            # Check roles
            if required_roles:
                user_roles = payload.get("roles", [])
                if not all(role in user_roles for role in required_roles):
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Request validation failed: {str(e)}")
            return False
    
    def audit_log(
        self,
        user_id: str,
        action: str,
        resource: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create an audit log entry."""
        try:
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "action": action,
                "resource": resource,
                "status": status,
                "details": details or {}
            }
            
            # In a real implementation, you would store this in a database
            logger.info(f"Audit log: {log_entry}")
            
            return log_entry
        except Exception as e:
            logger.error(f"Failed to create audit log: {str(e)}")
            raise 