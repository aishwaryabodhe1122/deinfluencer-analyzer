from fastapi import FastAPI, HTTPException, Depends, status, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List
import uvicorn
import os
from datetime import datetime, timedelta
import json

# Import our modules
from database import get_db, create_tables, User, AnalysisHistory, Watchlist
from email_models import EmailVerificationToken, PasswordResetToken  # Import email models for relationships
from auth import (
    create_user, authenticate_user, create_access_token, verify_token,
    get_current_user, get_current_user_optional, require_role, check_permission,
    get_user_by_id, get_user_by_username, get_user_by_email, update_user_profile, update_user_password, update_user_notifications,
    get_all_users, update_user_role, update_user_status, get_user_stats,
    verify_password, get_password_hash
)
from social_media_apis import fetch_influencer_data
from authenticity_analyzer import authenticity_analyzer
# from unified_data_manager import unified_data_manager  # Temporarily disabled due to async issues
# from canonical_schemas import PlatformType
# from multi_platform_endpoints import router as multi_platform_router
from social_auth import router as social_auth_router
from email_verification import router as email_verification_router
from schemas import (
    UserCreate, UserLogin, UserResponse, Token, AnalysisRequest, AnalysisResponse,
    ProfileUpdateRequest, PasswordChangeRequest, NotificationUpdateRequest,
    UserManagementResponse, UserRoleUpdateRequest, UserStatusUpdateRequest,
    SystemStatsResponse,
    InfluencerProfile, AuthenticityScore, WatchlistAdd, WatchlistItem,
    AnalysisHistoryItem, TrendingResponse, MessageResponse, UserProfile
)

# Initialize FastAPI app
app = FastAPI(
    title="Deinfluencer Authenticity Analyzer",
    description="AI-powered authenticity analysis for social media influencers with unified multi-platform schema",
    version="3.0.0"
)

# Include multi-platform endpoints
# app.include_router(multi_platform_router)  # Temporarily disabled

# Include social authentication endpoints
app.include_router(social_auth_router, prefix="/api")

# Include email verification endpoints
app.include_router(email_verification_router, prefix="/api")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# Real data fetching is now handled by social_media_apis.py

# Routes
@app.get("/")
async def root():
    return {
        "message": "Deinfluencer Authenticity Analyzer API",
        "version": "2.0.0",
        "status": "active",
        "features": "Real data fetching with advanced AI scoring"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

# Authentication endpoints
@app.post("/api/auth/register", response_model=Token)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user
    """
    # Check if user already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user with role support
    user = create_user(
        db=db,
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
        full_name=user_data.full_name,
        role=getattr(user_data, 'role', 'consumer')  # Default to consumer if no role specified
    )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.post("/api/auth/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login user and return access token
    """
    user = authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last_login time
    from datetime import datetime
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    
    access_token = create_access_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/api/auth/me", response_model=UserProfile)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user profile with stats
    """
    analysis_count = db.query(AnalysisHistory).filter(
        AnalysisHistory.user_id == current_user.id
    ).count()
    
    watchlist_count = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id
    ).count()
    
    return {
        **current_user.__dict__,
        "analysis_count": analysis_count,
        "watchlist_count": watchlist_count
    }

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_influencer(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    authorization: Optional[str] = Header(None)
):
    """
    Analyze an influencer's authenticity score using unified multi-platform data
    """
    try:
        # Validate platform (simple string validation)
        supported_platforms = ['twitter', 'instagram', 'youtube', 'tiktok', 'facebook', 'linkedin']
        if request.platform.lower() not in supported_platforms:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported platform: {request.platform}"
            )
        
        # Fetch real influencer data from social media APIs
        profile = await fetch_influencer_data(request.username, request.platform)
        
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not find influencer '{request.username}' on {request.platform}"
            )
        
        # Get recent posts data for advanced analysis
        recent_posts = getattr(profile, 'recent_posts', [])
        
        # Use advanced authenticity analyzer
        authenticity_score = authenticity_analyzer.analyze_authenticity(profile, recent_posts)
        
        # Generate insights and recommendations
        insights = authenticity_analyzer.generate_insights(profile, authenticity_score, recent_posts)
        recommendations = authenticity_analyzer.generate_recommendations(profile, authenticity_score)
        
        # Save analysis history if user is authenticated
        current_user = None
        print(f"DEBUG: Authorization header received: {authorization}")
        
        if authorization and authorization.startswith("Bearer "):
            try:
                token = authorization.replace("Bearer ", "")
                print(f"DEBUG: Extracted token: {token[:20]}...")
                username = verify_token(token)
                print(f"DEBUG: Verified username: {username}")
                if username:
                    current_user = get_user_by_username(db, username=username)
                    print(f"DEBUG: Found user: {current_user.username if current_user else None}")
            except Exception as e:
                print(f"DEBUG: Auth error: {str(e)}")
                pass  # Ignore auth errors for optional authentication
        else:
            print("DEBUG: No authorization header or invalid format")
        
        if current_user:
            print(f"DEBUG: Saving analysis history for user {current_user.username}")
            analysis_history = AnalysisHistory(
                user_id=current_user.id,
                influencer_username=request.username,
                platform=request.platform,
                overall_score=authenticity_score.overall_score,
                engagement_quality=authenticity_score.engagement_quality,
                content_authenticity=authenticity_score.content_authenticity,
                sponsored_ratio=authenticity_score.sponsored_ratio,
                follower_authenticity=authenticity_score.follower_authenticity,
                consistency_score=authenticity_score.consistency_score,
                insights=json.dumps(insights),
                recommendations=json.dumps(recommendations)
            )
            db.add(analysis_history)
            db.commit()
            print(f"DEBUG: Analysis history saved successfully with ID: {analysis_history.id}")
        else:
            print("DEBUG: No authenticated user found, analysis history not saved")
        
        return AnalysisResponse(
            profile=profile,
            authenticity_score=authenticity_score,
            insights=insights,
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Enter valid username {str(e)}"
        )

@app.get("/api/trending")
async def get_trending_influencers():
    """
    Get trending influencers with their authenticity scores
    """
    return {
        "trending": [
            {
                "username": "johndoe",
                "platform": "instagram",
                "authenticity_score": 8.5,
                "follower_count": 150000,
                "trend_direction": "up"
            },
            {
                "username": "janesmith",
                "platform": "instagram", 
                "authenticity_score": 9.2,
                "follower_count": 50000,
                "trend_direction": "stable"
            }
        ]
    }

# User-specific endpoints
@app.get("/api/user/history", response_model=List[AnalysisHistoryItem])
async def get_user_analysis_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0
):
    """
    Get user's analysis history
    """
    analyses = db.query(AnalysisHistory).filter(
        AnalysisHistory.user_id == current_user.id
    ).order_by(AnalysisHistory.created_at.desc()).offset(offset).limit(limit).all()
    
    return analyses

@app.get("/api/user/watchlist", response_model=List[WatchlistItem])
async def get_user_watchlist(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's watchlist
    """
    watchlist = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id
    ).order_by(Watchlist.added_at.desc()).all()
    
    return watchlist

@app.post("/api/user/watchlist", response_model=MessageResponse)
async def add_to_watchlist(
    watchlist_data: WatchlistAdd,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Add influencer to user's watchlist
    """
    # Check if already in watchlist
    existing = db.query(Watchlist).filter(
        Watchlist.user_id == current_user.id,
        Watchlist.influencer_username == watchlist_data.influencer_username,
        Watchlist.platform == watchlist_data.platform
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Influencer already in watchlist"
        )
    
    watchlist_item = Watchlist(
        user_id=current_user.id,
        influencer_username=watchlist_data.influencer_username,
        platform=watchlist_data.platform
    )
    
    db.add(watchlist_item)
    db.commit()
    
    return {"message": "Added to watchlist successfully"}

@app.delete("/api/user/watchlist/{watchlist_id}", response_model=MessageResponse)
async def remove_from_watchlist(
    watchlist_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Remove influencer from user's watchlist
    """
    watchlist_item = db.query(Watchlist).filter(
        Watchlist.id == watchlist_id,
        Watchlist.user_id == current_user.id
    ).first()
    
    if not watchlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist item not found"
        )
    
    db.delete(watchlist_item)
    db.commit()
    
    return {"message": "Removed from watchlist successfully"}

# Profile Management Endpoints
@app.put("/api/profile", response_model=UserResponse)
async def update_profile(
    profile_data: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile information
    """
    try:
        # Prepare update data
        update_data = {}
        if profile_data.full_name is not None:
            update_data['full_name'] = profile_data.full_name
        if profile_data.email is not None:
            update_data['email'] = profile_data.email
        if profile_data.avatar_url is not None:
            update_data['avatar_url'] = profile_data.avatar_url
        
        # Update user profile
        updated_user = update_user_profile(db, current_user.id, update_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return updated_user
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}"
        )

@app.put("/api/profile/password")
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    """
    try:
        # Verify current password
        if not verify_password(password_data.current_password, current_user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Hash new password
        new_password_hash = get_password_hash(password_data.new_password)
        
        # Update password
        updated_user = update_user_password(db, current_user.id, new_password_hash)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "Password updated successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )

@app.put("/api/profile/notifications")
async def update_notifications(
    notification_data: NotificationUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user notification preferences
    """
    try:
        # Convert preferences to dict
        preferences = notification_data.preferences.dict()
        
        # Update notification preferences
        updated_user = update_user_notifications(db, current_user.id, preferences)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "Notification preferences updated successfully"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update notifications: {str(e)}"
        )

# Admin Management Endpoints
@app.get("/api/admin/stats", response_model=SystemStatsResponse)
async def get_system_stats(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Get system statistics (admin only)
    """
    try:
        stats = get_user_stats(db)
        return SystemStatsResponse(**stats)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get system stats: {str(e)}"
        )

@app.get("/api/admin/users", response_model=List[UserManagementResponse])
async def get_all_users_admin(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all users for admin management
    """
    try:
        users = get_all_users(db, skip=skip, limit=limit)
        return [UserManagementResponse.from_orm(user) for user in users]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get users: {str(e)}"
        )

@app.put("/api/admin/users/role")
async def update_user_role_admin(
    role_data: UserRoleUpdateRequest,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Update user role (admin only)
    """
    try:
        # Validate role
        valid_roles = ['consumer', 'brand', 'admin']
        if role_data.new_role not in valid_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}"
            )
        
        # Update user role
        updated_user = update_user_role(db, role_data.user_id, role_data.new_role)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": f"User role updated to {role_data.new_role} successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user role: {str(e)}"
        )

@app.put("/api/admin/users/status")
async def update_user_status_admin(
    status_data: UserStatusUpdateRequest,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """
    Update user status (admin only)
    """
    try:
        # Update user status
        updated_user = update_user_status(db, status_data.user_id, status_data.is_active)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        status_text = "activated" if status_data.is_active else "deactivated"
        return {"message": f"User {status_text} successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user status: {str(e)}"
        )

# Enhanced Analysis History Endpoint
@app.get("/api/history", response_model=List[AnalysisHistoryItem])
async def get_analysis_history_enhanced(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    platform: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = "date",
    limit: int = 20,
    offset: int = 0
):
    """
    Get user's analysis history with filtering and search
    """
    try:
        # Build query
        query = db.query(AnalysisHistory).filter(AnalysisHistory.user_id == current_user.id)
        
        # Apply filters
        if platform:
            query = query.filter(AnalysisHistory.platform == platform)
        
        if search:
            query = query.filter(AnalysisHistory.influencer_username.ilike(f"%{search}%"))
        
        # Apply sorting
        if sort_by == "score":
            query = query.order_by(AnalysisHistory.overall_score.desc())
        else:  # default to date
            query = query.order_by(AnalysisHistory.created_at.desc())
        
        # Apply pagination
        analyses = query.offset(offset).limit(limit).all()
        
        # Convert to response format
        result = []
        for analysis in analyses:
            insights = json.loads(analysis.insights) if analysis.insights else []
            recommendations = json.loads(analysis.recommendations) if analysis.recommendations else []
            
            result.append(AnalysisHistoryItem(
                id=analysis.id,
                influencer_username=analysis.influencer_username,
                platform=analysis.platform,
                overall_score=analysis.overall_score,
                engagement_quality=analysis.engagement_quality,
                content_authenticity=analysis.content_authenticity,
                sponsored_ratio=analysis.sponsored_ratio,
                follower_authenticity=analysis.follower_authenticity,
                consistency_score=analysis.consistency_score,
                insights=insights,
                recommendations=recommendations,
                created_at=analysis.created_at
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get analysis history: {str(e)}"
        )

# Helper functions for scoring (mock implementations)
def calculate_engagement_quality(profile: InfluencerProfile) -> float:
    """Calculate engagement quality score (0-10)"""
    # Mock calculation based on follower/following ratio
    ratio = profile.follower_count / max(profile.following_count, 1)
    if ratio > 100:
        return 9.0
    elif ratio > 50:
        return 8.0
    elif ratio > 10:
        return 7.0
    else:
        return 6.0

def calculate_content_authenticity(profile: InfluencerProfile) -> float:
    """Calculate content authenticity score (0-10)"""
    # Mock calculation based on bio content
    if profile.bio and "#sponsored" in profile.bio.lower():
        return 6.5
    return 8.5

def calculate_sponsored_ratio(profile: InfluencerProfile) -> float:
    """Calculate sponsored content ratio score (0-10)"""
    # Mock calculation - higher score for lower sponsored ratio
    return 7.5

def calculate_follower_authenticity(profile: InfluencerProfile) -> float:
    """Calculate follower authenticity score (0-10)"""
    # Mock calculation based on verification status
    return 9.0 if profile.verified else 7.5

def calculate_consistency_score(profile: InfluencerProfile) -> float:
    """Calculate posting consistency score (0-10)"""
    # Mock calculation based on post count
    posts_per_day = profile.post_count / 365  # Assume account is 1 year old
    if 0.5 <= posts_per_day <= 2:
        return 9.0
    elif posts_per_day > 5:
        return 6.0
    else:
        return 7.5

def generate_insights(profile: InfluencerProfile, score: AuthenticityScore) -> List[str]:
    """Generate insights based on analysis"""
    insights = []
    
    if score.overall_score >= 8.0:
        insights.append("This influencer shows high authenticity indicators")
    elif score.overall_score >= 6.0:
        insights.append("This influencer shows moderate authenticity")
    else:
        insights.append("This influencer shows low authenticity indicators")
    
    if score.engagement_quality < 7.0:
        insights.append("Engagement patterns may indicate artificial inflation")
    
    if score.sponsored_ratio < 6.0:
        insights.append("High ratio of sponsored content detected")
    
    return insights

def generate_recommendations(profile: InfluencerProfile, score: AuthenticityScore) -> List[str]:
    """Generate recommendations based on analysis"""
    recommendations = []
    
    if score.overall_score < 7.0:
        recommendations.append("Exercise caution when considering this influencer's recommendations")
    
    if score.engagement_quality < 7.0:
        recommendations.append("Verify engagement authenticity before partnerships")
    
    if score.content_authenticity < 7.0:
        recommendations.append("Review recent posts for authentic vs sponsored content balance")
    
    return recommendations

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
