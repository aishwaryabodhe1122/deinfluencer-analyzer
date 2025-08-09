"""
Email Verification Endpoints
Handles email verification and password reset functionality
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
import logging

from database import get_db, User
from email_models import EmailVerificationToken, PasswordResetToken
from email_service import email_service, EMAIL_AVAILABLE
from auth import get_password_hash, verify_password, create_access_token
from schemas import UserResponse, Token
from decouple import config

router = APIRouter()
logger = logging.getLogger(__name__)

FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')

@router.post("/send-verification-email")
async def send_verification_email(
    email: str,
    db: Session = Depends(get_db)
):
    """Send verification email to user (for resending verification)"""
    if not EMAIL_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email service is not configured. Please contact support."
        )
    
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already verified"
        )
    
    # Invalidate any existing verification tokens
    existing_tokens = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.user_id == user.id,
        EmailVerificationToken.used == False
    ).all()
    
    for token in existing_tokens:
        token.used = True
        token.used_at = datetime.utcnow()
    
    # Create new verification token
    verification_token = EmailVerificationToken(
        user_id=user.id,
        email=user.email
    )
    db.add(verification_token)
    db.commit()
    db.refresh(verification_token)
    
    # Send verification email
    success = email_service.send_verification_email(
        email=user.email,
        username=user.username,
        verification_token=verification_token.token
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send verification email"
        )
    
    return {"message": "Verification email sent successfully"}

@router.get("/verify-email")
async def verify_email(
    token: str,
    db: Session = Depends(get_db)
):
    """Verify email using verification token"""
    # Find verification token
    verification_token = db.query(EmailVerificationToken).filter(
        EmailVerificationToken.token == token
    ).first()
    
    if not verification_token:
        # Redirect to frontend with error
        return RedirectResponse(
            url=f"{FRONTEND_URL}/?error=invalid_token&message=Invalid verification token"
        )
    
    if not verification_token.is_valid:
        # Redirect to frontend with error
        error_msg = "expired" if verification_token.is_expired else "already_used"
        return RedirectResponse(
            url=f"{FRONTEND_URL}/?error={error_msg}&message=Verification token is {error_msg.replace('_', ' ')}"
        )
    
    # Get user
    user = db.query(User).filter(User.id == verification_token.user_id).first()
    if not user:
        return RedirectResponse(
            url=f"{FRONTEND_URL}/?error=user_not_found&message=User not found"
        )
    
    # Mark user as verified
    user.is_verified = True
    user.updated_at = datetime.utcnow()
    
    # Mark token as used
    verification_token.used = True
    verification_token.used_at = datetime.utcnow()
    
    db.commit()
    
    # Send welcome email
    if EMAIL_AVAILABLE:
        email_service.send_welcome_email(
            email=user.email,
            username=user.username,
            role=user.role
        )
    
    # Redirect to frontend with success
    return RedirectResponse(
        url=f"{FRONTEND_URL}/?verified=true&message=Email verified successfully! Welcome to Nexora."
    )

@router.post("/forgot-password")
async def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):
    """Send password reset email"""
    if not EMAIL_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Email service is not configured. Please contact support."
        )
    
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        # Don't reveal if email exists or not for security
        return {"message": "If the email exists, a password reset link has been sent"}
    
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please verify your email address first"
        )
    
    # Invalidate any existing reset tokens
    existing_tokens = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.used == False
    ).all()
    
    for token in existing_tokens:
        token.used = True
        token.used_at = datetime.utcnow()
    
    # Create new reset token
    reset_token = PasswordResetToken(
        user_id=user.id,
        email=user.email
    )
    db.add(reset_token)
    db.commit()
    db.refresh(reset_token)
    
    # Send reset email
    success = email_service.send_password_reset_email(
        email=user.email,
        username=user.username,
        reset_token=reset_token.token
    )
    
    if not success:
        logger.error(f"Failed to send password reset email to {user.email}")
    
    # Always return success message for security
    return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """Reset password using reset token"""
    # Find reset token
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token
    ).first()
    
    if not reset_token or not reset_token.is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Get user
    user = db.query(User).filter(User.id == reset_token.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Validate password strength
    if len(new_password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    # Update password
    user.hashed_password = get_password_hash(new_password)
    user.updated_at = datetime.utcnow()
    
    # Mark token as used
    reset_token.used = True
    reset_token.used_at = datetime.utcnow()
    
    # Invalidate all other reset tokens for this user
    other_tokens = db.query(PasswordResetToken).filter(
        PasswordResetToken.user_id == user.id,
        PasswordResetToken.id != reset_token.id,
        PasswordResetToken.used == False
    ).all()
    
    for token in other_tokens:
        token.used = True
        token.used_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Password reset successfully"}

@router.get("/verify-reset-token")
async def verify_reset_token(
    token: str,
    db: Session = Depends(get_db)
):
    """Verify if reset token is valid (for frontend validation)"""
    reset_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token
    ).first()
    
    if not reset_token or not reset_token.is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    return {
        "valid": True,
        "email": reset_token.email,
        "expires_at": reset_token.expires_at.isoformat()
    }
