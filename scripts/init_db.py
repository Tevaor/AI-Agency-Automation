"""
Database initialization script for the AI automation platform.
"""
import os
import logging
import datetime
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from consent.manager import Base, Consent
from security.zero_trust import User, SecurityConfig, ZeroTrustManager, Base

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def init_database():
    """Initialize the database with required tables and initial data."""
    try:
        # Get database URL from environment
        database_url = os.getenv("DATABASE_URL", "sqlite:///./consent.db")
        
        # Create engine and session
        engine = create_engine(database_url)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        # Create tables
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
        
        # Initialize security manager
        security_config = SecurityConfig(
            jwt_secret=os.getenv("JWT_SECRET_KEY", "your-secret-key"),
            jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            access_token_expire_minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
            refresh_token_expire_days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")),
            password_hash_rounds=int(os.getenv("PASSWORD_HASH_ROUNDS", "12"))
        )
        security_manager = ZeroTrustManager(security_config)
        
        # Create admin user if it doesn't exist
        admin_user = session.query(User).filter_by(username="admin").first()
        if not admin_user:
            admin_user = security_manager.create_user(
                username="admin",
                email="admin@example.com",
                password="admin123",  # In production, use a secure password
                roles=json.dumps(["admin"]),
                permissions=json.dumps(["admin"])
            )
            session.add(admin_user)
            session.commit()
            logger.info("Admin user created successfully")
        
        # Create initial consent records if needed
        initial_consents = [
            Consent(
                user_id="system",
                purpose="data_collection",
                status="granted",
                granted_at=datetime.datetime.utcnow(),
                meta_data={"source": "system_init"}
            ),
            Consent(
                user_id="system",
                purpose="data_processing",
                status="granted",
                granted_at=datetime.datetime.utcnow(),
                meta_data={"source": "system_init"}
            )
        ]
        
        for consent in initial_consents:
            existing_consent = session.query(Consent).filter_by(
                user_id=consent.user_id,
                purpose=consent.purpose
            ).first()
            
            if not existing_consent:
                session.add(consent)
        
        session.commit()
        logger.info("Initial consent records created successfully")
        
        logger.info("Database initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise
    finally:
        session.close()

if __name__ == "__main__":
    init_database() 