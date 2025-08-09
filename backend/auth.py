from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db, User, AnalysisHistory
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# JWT token utilities
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

# Database utilities
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user_profile(db: Session, user_id: int, profile_data: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in profile_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user

def update_user_password(db: Session, user_id: int, new_password_hash: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.hashed_password = new_password_hash
        db.commit()
        db.refresh(user)
    return user

def update_user_notifications(db: Session, user_id: int, preferences: dict):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.notification_preferences = json.dumps(preferences)
        db.commit()
        db.refresh(user)
    return user

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_users_by_role(db: Session, role: str):
    return db.query(User).filter(User.role == role).all()

def update_user_role(db: Session, user_id: int, new_role: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.role = new_role
        db.commit()
        db.refresh(user)
    return user

def update_user_status(db: Session, user_id: int, is_active: bool):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_active = is_active
        db.commit()
        db.refresh(user)
    return user

def get_user_stats(db: Session):
    total_users = db.query(User).count()
    consumer_users = db.query(User).filter(User.role == 'consumer').count()
    brand_users = db.query(User).filter(User.role == 'brand').count()
    admin_users = db.query(User).filter(User.role == 'admin').count()
    
    # Get analysis stats from AnalysisHistory table
    total_analyses = db.query(AnalysisHistory).count()
    today = datetime.now().date()
    analyses_today = db.query(AnalysisHistory).filter(
        func.date(AnalysisHistory.created_at) == today
    ).count()
    
    return {
        'total_users': total_users,
        'consumer_users': consumer_users,
        'brand_users': brand_users,
        'admin_users': admin_users,
        'total_analyses': total_analyses,
        'analyses_today': analyses_today
    }

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, email: str, username: str, password: str, full_name: str = None, role: str = "consumer", send_verification: bool = True):
    # Check if user already exists
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if get_user_by_username(db, username):
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Validate role
    valid_roles = ["consumer", "brand", "admin"]
    if role not in valid_roles:
        role = "consumer"  # Default to consumer if invalid role provided
    
    # Create new user (unverified by default)
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email, 
        username=username, 
        hashed_password=hashed_password, 
        full_name=full_name,
        role=role,
        is_verified=False  # New users start unverified
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Send verification email if email service is available and requested
    if send_verification:
        try:
            from email_service import email_service, EMAIL_AVAILABLE
            from email_models import EmailVerificationToken
            
            if EMAIL_AVAILABLE:
                # Create verification token
                verification_token = EmailVerificationToken(
                    user_id=db_user.id,
                    email=db_user.email
                )
                db.add(verification_token)
                db.commit()
                db.refresh(verification_token)
                
                # Send verification email
                email_service.send_verification_email(
                    email=db_user.email,
                    username=db_user.username,
                    verification_token=verification_token.token
                )
        except Exception as e:
            # Log error but don't fail registration
            print(f"Failed to send verification email: {str(e)}")
    return db_user

# Dependency to get current user
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    
    return user

# Optional dependency for current user (doesn't raise exception if not authenticated)
def get_current_user_optional(
    authorization: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Optional[User]:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    try:
        token = authorization.replace("Bearer ", "")
        username = verify_token(token)
        if username is None:
            return None
        
        user = get_user_by_username(db, username=username)
        if user is None:
            return None
        
        return user
    except Exception:
        return None

# Role-based permission checking
def check_permission(user: User, required_role: str) -> bool:
    """Check if user has required role or higher permissions"""
    role_hierarchy = {
        "consumer": 1,
        "brand": 2,
        "admin": 3
    }
    
    user_level = role_hierarchy.get(user.role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level

def require_role(required_role: str):
    """Dependency to require specific role"""
    def role_checker(current_user: User = Depends(get_current_user)):
        if not check_permission(current_user, required_role):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {required_role}"
            )
        return current_user
    return role_checker

# Role-specific dependencies
def get_admin_user(current_user: User = Depends(require_role("admin"))):
    return current_user

def get_brand_user(current_user: User = Depends(require_role("brand"))):
    return current_user

def get_consumer_user(current_user: User = Depends(require_role("consumer"))):
    return current_user
