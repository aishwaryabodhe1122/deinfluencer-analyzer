"""
Database Models for Email Verification and Password Reset
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from database import Base
import secrets

class EmailVerificationToken(Base):
    """Email verification tokens for new user registrations"""
    __tablename__ = "email_verification_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="verification_tokens")
    
    def __init__(self, user_id: int, email: str, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.email = email
        self.token = secrets.token_urlsafe(32)
        self.expires_at = datetime.utcnow() + timedelta(hours=24)  # 24 hour expiry
    
    @property
    def is_expired(self) -> bool:
        """Check if token has expired"""
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Check if token is valid (not used and not expired)"""
        return not self.used and not self.is_expired

class PasswordResetToken(Base):
    """Password reset tokens for user password recovery"""
    __tablename__ = "password_reset_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    used_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="reset_tokens")
    
    def __init__(self, user_id: int, email: str, **kwargs):
        super().__init__(**kwargs)
        self.user_id = user_id
        self.email = email
        self.token = secrets.token_urlsafe(32)
        self.expires_at = datetime.utcnow() + timedelta(hours=1)  # 1 hour expiry
    
    @property
    def is_expired(self) -> bool:
        """Check if token has expired"""
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_valid(self) -> bool:
        """Check if token is valid (not used and not expired)"""
        return not self.used and not self.is_expired
