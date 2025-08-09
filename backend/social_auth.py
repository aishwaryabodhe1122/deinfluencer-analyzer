"""
Social Authentication Endpoints
Handles OAuth login/registration for Google and GitHub
"""

from fastapi import APIRouter, HTTPException, Depends, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Dict, Any
import secrets
import json

from database import get_db
from auth import create_user, get_user_by_email, create_access_token, get_user_by_username
from oauth_config import oauth, social_auth_provider, OAUTH_AVAILABLE
from schemas import Token

router = APIRouter()

# Store OAuth state temporarily (in production, use Redis or database)
oauth_states = {}

@router.get("/auth/{provider}/login")
async def social_login(provider: str, request: Request):
    """Initiate OAuth login with social provider"""
    if not OAUTH_AVAILABLE:
        # Redirect to frontend with specific error for social login
        frontend_url = f"http://localhost:3000/landing?social_error=oauth_unavailable&provider={provider}&message=Social authentication is not configured yet. Please use email/password login or contact support."
        return RedirectResponse(url=frontend_url)
    
    if provider not in ['google', 'github', 'facebook', 'instagram', 'linkedin', 'twitter']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported provider"
        )
    
    # Generate state for CSRF protection
    state = secrets.token_urlsafe(32)
    oauth_states[state] = {'provider': provider}
    
    # Get OAuth client
    client = oauth.create_client(provider)
    
    # Redirect URI for callback
    redirect_uri = f"http://localhost:8000/api/auth/{provider}/callback"
    
    return await client.authorize_redirect(request, redirect_uri, state=state)

@router.get("/auth/{provider}/callback")
async def social_callback(
    provider: str, 
    request: Request, 
    db: Session = Depends(get_db)
):
    """Handle OAuth callback and create/login user"""
    if not OAUTH_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Social authentication is not available. OAuth dependencies not installed."
        )
    
    if provider not in ['google', 'github']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported provider"
        )
    
    try:
        # Get OAuth client
        client = oauth.create_client(provider)
        
        # Get access token
        token = await client.authorize_access_token(request)
        
        # Verify state parameter
        state = request.query_params.get('state')
        if not state or state not in oauth_states:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid state parameter"
            )
        
        # Clean up state
        del oauth_states[state]
        
        # Get user info from provider
        if provider == 'google':
            user_data = await social_auth_provider.get_google_user_info(
                token.get('access_token')
            )
        elif provider == 'github':
            user_data = await social_auth_provider.get_github_user_info(
                token.get('access_token')
            )
        elif provider == 'facebook':
            user_data = await social_auth_provider.get_facebook_user_info(
                token.get('access_token')
            )
        elif provider == 'instagram':
            user_data = await social_auth_provider.get_instagram_user_info(
                token.get('access_token')
            )
        elif provider == 'linkedin':
            user_data = await social_auth_provider.get_linkedin_user_info(
                token.get('access_token')
            )
        elif provider == 'twitter':
            user_data = await social_auth_provider.get_twitter_user_info(
                token.get('access_token')
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported provider: {provider}"
            )
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to fetch user information"
            )
        
        # Normalize user data
        normalized_data = social_auth_provider.normalize_user_data(provider, user_data)
        
        if not normalized_data.get('email'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required for registration"
            )
        
        # Check if user exists
        existing_user = get_user_by_email(db, normalized_data['email'])
        
        if existing_user:
            # User exists, log them in
            user = existing_user
            
            # Update avatar if available
            if normalized_data.get('avatar_url') and not existing_user.avatar_url:
                existing_user.avatar_url = normalized_data['avatar_url']
                db.commit()
                db.refresh(existing_user)
        else:
            # Create new user
            # Generate unique username if needed
            base_username = normalized_data['username']
            username = base_username
            counter = 1
            
            while get_user_by_username(db, username):
                username = f"{base_username}{counter}"
                counter += 1
            
            user = create_user(
                db=db,
                email=normalized_data['email'],
                username=username,
                password=secrets.token_urlsafe(32),  # Random password for OAuth users
                full_name=normalized_data.get('full_name'),
                role='consumer'  # Default role for social signups
            )
            
            # Update additional fields
            if normalized_data.get('avatar_url'):
                user.avatar_url = normalized_data['avatar_url']
            if normalized_data.get('verified'):
                user.is_verified = True
            
            db.commit()
            db.refresh(user)
        
        # Create access token
        access_token = create_access_token(data={"sub": user.username})
        
        # Redirect to frontend with token (in production, use secure cookies)
        frontend_url = f"http://localhost:3000/auth/callback?token={access_token}&user={user.id}"
        return RedirectResponse(url=frontend_url)
        
    except Exception as e:
        print(f"OAuth callback error: {str(e)}")
        # Redirect to frontend with error
        frontend_url = f"http://localhost:3000/auth/callback?error=oauth_failed"
        return RedirectResponse(url=frontend_url)

@router.post("/auth/social/verify", response_model=Token)
async def verify_social_token(
    request: Dict[str, Any],
    db: Session = Depends(get_db)
):
    """Verify social authentication token and return user data"""
    if not OAUTH_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Social authentication is not available. OAuth dependencies not installed."
        )
    
    provider = request.get('provider')
    access_token = request.get('access_token')
    
    if not provider or not access_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provider and access token are required"
        )
    
    if provider not in ['google', 'github']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported provider"
        )
    
    try:
        # Get user info from provider
        if provider == 'google':
            user_data = await social_auth_provider.get_google_user_info(access_token)
        else:  # github
            user_data = await social_auth_provider.get_github_user_info(access_token)
        
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token"
            )
        
        # Normalize user data
        normalized_data = social_auth_provider.normalize_user_data(provider, user_data)
        
        if not normalized_data.get('email'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is required"
            )
        
        # Check if user exists or create new one
        existing_user = get_user_by_email(db, normalized_data['email'])
        
        if existing_user:
            user = existing_user
        else:
            # Generate unique username
            base_username = normalized_data['username']
            username = base_username
            counter = 1
            
            while get_user_by_username(db, username):
                username = f"{base_username}{counter}"
                counter += 1
            
            user = create_user(
                db=db,
                email=normalized_data['email'],
                username=username,
                password=secrets.token_urlsafe(32),
                full_name=normalized_data.get('full_name'),
                role='consumer'
            )
            
            if normalized_data.get('avatar_url'):
                user.avatar_url = normalized_data['avatar_url']
            if normalized_data.get('verified'):
                user.is_verified = True
            
            db.commit()
            db.refresh(user)
        
        # Create JWT token
        jwt_token = create_access_token(data={"sub": user.username})
        
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "user": user
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Social token verification error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Social authentication failed"
        )
