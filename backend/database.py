from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL - fallback to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./deinfluencer.db")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="consumer")  # consumer, brand, admin
    avatar_url = Column(String)  # Profile avatar URL
    notification_preferences = Column(Text)  # JSON string for notification settings
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)  # Track user's last login time
    
    # Relationships
    analyses = relationship("AnalysisHistory", back_populates="user")
    watchlists = relationship("Watchlist", back_populates="user")
    verification_tokens = relationship("EmailVerificationToken", back_populates="user")
    reset_tokens = relationship("PasswordResetToken", back_populates="user")

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    influencer_username = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    overall_score = Column(Float)
    engagement_quality = Column(Float)
    content_authenticity = Column(Float)
    sponsored_ratio = Column(Float)
    follower_authenticity = Column(Float)
    consistency_score = Column(Float)
    insights = Column(Text)
    recommendations = Column(Text)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="analyses")

class Watchlist(Base):
    __tablename__ = "watchlists"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    influencer_username = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    added_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="watchlists")

class InfluencerProfile(Base):
    __tablename__ = "influencer_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    follower_count = Column(Integer)
    following_count = Column(Integer)
    post_count = Column(Integer)
    bio = Column(Text)
    verified = Column(Boolean, default=False)
    profile_image_url = Column(String)
    last_updated = Column(DateTime, default=func.now())
    
    # Unique constraint on username + platform
    __table_args__ = (
        UniqueConstraint('username', 'platform', name='unique_username_platform'),
    )

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
