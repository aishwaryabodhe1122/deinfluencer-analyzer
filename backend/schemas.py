from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    role: Optional[str] = "consumer"  # consumer, brand, admin

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserProfile(User):
    analysis_count: int
    watchlist_count: int

# Profile Management Schemas
class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    avatar_url: Optional[str] = None

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

class NotificationPreferences(BaseModel):
    analysis_updates: bool = True
    weekly_reports: bool = False
    security_alerts: bool = True

class NotificationUpdateRequest(BaseModel):
    preferences: NotificationPreferences

# Admin Management Schemas
class UserManagementResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    role: str
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    avatar_url: Optional[str]
    
    class Config:
        from_attributes = True

class UserRoleUpdateRequest(BaseModel):
    user_id: int
    new_role: str

class UserStatusUpdateRequest(BaseModel):
    user_id: int
    is_active: bool

class SystemStatsResponse(BaseModel):
    total_users: int
    consumer_users: int
    brand_users: int
    admin_users: int
    total_analyses: int
    analyses_today: int

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class TokenData(BaseModel):
    username: Optional[str] = None

# Analysis schemas
class AnalysisRequest(BaseModel):
    username: str
    platform: str
    deep_analysis: bool = False

class InfluencerProfile(BaseModel):
    username: str
    platform: str
    follower_count: int
    following_count: int
    post_count: int
    bio: Optional[str] = None
    verified: bool = False
    profile_image_url: Optional[str] = None
    recent_posts: Optional[List[dict]] = None  # For analysis purposes
    engagement_rate: Optional[float] = None  # Additional field from real data

class AuthenticityScore(BaseModel):
    overall_score: float
    engagement_quality: float
    content_authenticity: float
    sponsored_ratio: float
    follower_authenticity: float
    consistency_score: float
    last_updated: datetime

class AnalysisResponse(BaseModel):
    profile: InfluencerProfile
    authenticity_score: AuthenticityScore
    insights: List[str]
    recommendations: List[str]

class AnalysisHistoryItem(BaseModel):
    id: int
    influencer_username: str
    platform: str
    overall_score: float
    engagement_quality: float
    content_authenticity: float
    sponsored_ratio: float
    follower_authenticity: float
    consistency_score: float
    insights: List[str]
    recommendations: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Watchlist schemas
class WatchlistAdd(BaseModel):
    influencer_username: str
    platform: str

class WatchlistItem(BaseModel):
    id: int
    influencer_username: str
    platform: str
    added_at: datetime
    
    class Config:
        from_attributes = True

# Trending schemas
class TrendingInfluencer(BaseModel):
    username: str
    platform: str
    authenticity_score: float
    follower_count: int
    trend_direction: str

class TrendingResponse(BaseModel):
    trending: List[TrendingInfluencer]

# Response schemas
class MessageResponse(BaseModel):
    message: str
    
class ErrorResponse(BaseModel):
    detail: str
