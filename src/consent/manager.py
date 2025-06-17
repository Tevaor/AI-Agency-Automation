"""
Consent management module for handling data privacy and user consent.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
import logging
from enum import Enum
import json

from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.db.base import Base

logger = logging.getLogger(__name__)

class ConsentStatus(str, Enum):
    """Enum for consent status."""
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    EXPIRED = "expired"
    WITHDRAWN = "withdrawn"

class ConsentPurpose(str, Enum):
    """Enum for consent purposes."""
    DATA_COLLECTION = "data_collection"
    DATA_PROCESSING = "data_processing"
    DATA_SHARING = "data_sharing"
    MARKETING = "marketing"
    ANALYTICS = "analytics"

class Consent(Base):
    """Database model for consent records."""
    __tablename__ = "consents"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False, index=True)
    purpose = Column(String, nullable=False)
    status = Column(String, nullable=False)
    granted_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ConsentRequest(BaseModel):
    """Model for consent requests."""
    user_id: str
    purpose: ConsentPurpose
    expires_at: Optional[datetime] = None
    meta_data: Optional[Dict[str, Any]] = None

class ConsentResponse(BaseModel):
    """Model for consent responses."""
    consent_id: int
    status: ConsentStatus
    granted_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

class ConsentManager:
    """Manager class for handling consent operations."""
    
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def request_consent(self, request: ConsentRequest) -> ConsentResponse:
        """Create a new consent request."""
        session = self.Session()
        try:
            consent = Consent(
                user_id=request.user_id,
                purpose=request.purpose,
                status=ConsentStatus.PENDING,
                expires_at=request.expires_at,
                meta_data=request.meta_data
            )
            session.add(consent)
            session.commit()
            return ConsentResponse(
                consent_id=consent.id,
                status=ConsentStatus.PENDING,
                expires_at=consent.expires_at
            )
        finally:
            session.close()
    
    def grant_consent(self, consent_id: int) -> ConsentResponse:
        """Grant consent for a specific request."""
        session = self.Session()
        try:
            consent = session.query(Consent).get(consent_id)
            if not consent:
                raise ValueError(f"Consent {consent_id} not found")
            
            consent.status = ConsentStatus.GRANTED
            consent.granted_at = datetime.utcnow()
            session.commit()
            
            return ConsentResponse(
                consent_id=consent.id,
                status=ConsentStatus.GRANTED,
                granted_at=consent.granted_at,
                expires_at=consent.expires_at
            )
        finally:
            session.close()
    
    def deny_consent(self, consent_id: int) -> ConsentResponse:
        """Deny consent for a specific request."""
        session = self.Session()
        try:
            consent = session.query(Consent).get(consent_id)
            if not consent:
                raise ValueError(f"Consent {consent_id} not found")
            
            consent.status = ConsentStatus.DENIED
            session.commit()
            
            return ConsentResponse(
                consent_id=consent.id,
                status=ConsentStatus.DENIED
            )
        finally:
            session.close()
    
    def withdraw_consent(self, consent_id: int) -> ConsentResponse:
        """Withdraw previously granted consent."""
        session = self.Session()
        try:
            consent = session.query(Consent).get(consent_id)
            if not consent:
                raise ValueError(f"Consent {consent_id} not found")
            
            consent.status = ConsentStatus.WITHDRAWN
            session.commit()
            
            return ConsentResponse(
                consent_id=consent.id,
                status=ConsentStatus.WITHDRAWN
            )
        finally:
            session.close()
    
    def get_consent_status(self, consent_id: int) -> ConsentResponse:
        """Get the current status of a consent request."""
        session = self.Session()
        try:
            consent = session.query(Consent).get(consent_id)
            if not consent:
                raise ValueError(f"Consent {consent_id} not found")
            
            return ConsentResponse(
                consent_id=consent.id,
                status=ConsentStatus(consent.status),
                granted_at=consent.granted_at,
                expires_at=consent.expires_at
            )
        finally:
            session.close()
    
    def get_user_consents(self, user_id: str) -> List[ConsentResponse]:
        """Get all consent records for a user."""
        session = self.Session()
        try:
            consents = session.query(Consent).filter_by(user_id=user_id).all()
            return [
                ConsentResponse(
                    consent_id=consent.id,
                    status=ConsentStatus(consent.status),
                    granted_at=consent.granted_at,
                    expires_at=consent.expires_at
                )
                for consent in consents
            ]
        finally:
            session.close()
    
    def check_consent_validity(self, user_id: str, purpose: ConsentPurpose) -> bool:
        """Check if a user has valid consent for a specific purpose."""
        session = self.Session()
        try:
            consent = session.query(Consent).filter_by(
                user_id=user_id,
                purpose=purpose,
                status=ConsentStatus.GRANTED
            ).first()
            
            if not consent:
                return False
            
            if consent.expires_at and consent.expires_at < datetime.utcnow():
                consent.status = ConsentStatus.EXPIRED
                session.commit()
                return False
            
            return True
        finally:
            session.close() 