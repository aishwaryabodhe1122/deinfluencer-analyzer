"""
Security Middleware
Provides rate limiting, security notifications, and enhanced session management
"""

from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import time
import logging
from typing import Dict, Any
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Rate limiter instance
limiter = Limiter(key_func=get_remote_address)

# In-memory storage for failed login attempts (in production, use Redis)
failed_attempts: Dict[str, Dict[str, Any]] = {}
security_events: Dict[str, list] = {}

class SecurityMiddleware:
    """Enhanced security middleware with rate limiting and monitoring"""
    
    @staticmethod
    def log_security_event(event_type: str, user_id: str = None, ip_address: str = None, details: Dict[str, Any] = None):
        """Log security events for monitoring and alerts"""
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'user_id': user_id,
            'ip_address': ip_address,
            'details': details or {}
        }
        
        # Log to file/database (simplified for demo)
        logger.warning(f"SECURITY EVENT: {event_type} - User: {user_id}, IP: {ip_address}")
        
        # Store in memory (in production, use proper storage)
        if event_type not in security_events:
            security_events[event_type] = []
        security_events[event_type].append(event)
        
        # Keep only last 100 events per type
        if len(security_events[event_type]) > 100:
            security_events[event_type] = security_events[event_type][-100:]
    
    @staticmethod
    def check_failed_attempts(identifier: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """Check if identifier (email/IP) has exceeded failed login attempts"""
        now = datetime.utcnow()
        
        if identifier not in failed_attempts:
            return False
        
        attempts = failed_attempts[identifier]
        
        # Clean old attempts outside the window
        cutoff_time = now - timedelta(minutes=window_minutes)
        attempts['timestamps'] = [
            ts for ts in attempts['timestamps'] 
            if datetime.fromisoformat(ts) > cutoff_time
        ]
        
        # Check if exceeded max attempts
        if len(attempts['timestamps']) >= max_attempts:
            SecurityMiddleware.log_security_event(
                'ACCOUNT_LOCKOUT',
                details={'identifier': identifier, 'attempts': len(attempts['timestamps'])}
            )
            return True
        
        return False
    
    @staticmethod
    def record_failed_attempt(identifier: str):
        """Record a failed login attempt"""
        now = datetime.utcnow()
        
        if identifier not in failed_attempts:
            failed_attempts[identifier] = {'timestamps': []}
        
        failed_attempts[identifier]['timestamps'].append(now.isoformat())
        
        SecurityMiddleware.log_security_event(
            'FAILED_LOGIN_ATTEMPT',
            details={'identifier': identifier}
        )
    
    @staticmethod
    def clear_failed_attempts(identifier: str):
        """Clear failed attempts after successful login"""
        if identifier in failed_attempts:
            del failed_attempts[identifier]
    
    @staticmethod
    def detect_suspicious_activity(user_id: str, ip_address: str, user_agent: str = None) -> bool:
        """Detect suspicious login patterns"""
        # Simple suspicious activity detection
        # In production, implement more sophisticated detection
        
        # Check for multiple IPs for same user in short time
        recent_logins = [
            event for event in security_events.get('USER_LOGIN', [])
            if event.get('user_id') == user_id and
            datetime.fromisoformat(event['timestamp']) > datetime.utcnow() - timedelta(hours=1)
        ]
        
        unique_ips = set(event.get('ip_address') for event in recent_logins if event.get('ip_address'))
        
        if len(unique_ips) > 3:  # More than 3 different IPs in 1 hour
            SecurityMiddleware.log_security_event(
                'SUSPICIOUS_ACTIVITY',
                user_id=user_id,
                ip_address=ip_address,
                details={'unique_ips_count': len(unique_ips), 'detection_type': 'multiple_ips'}
            )
            return True
        
        return False
    
    @staticmethod
    def get_security_stats() -> Dict[str, Any]:
        """Get security statistics for admin dashboard"""
        now = datetime.utcnow()
        last_24h = now - timedelta(hours=24)
        
        stats = {
            'failed_logins_24h': 0,
            'suspicious_activities_24h': 0,
            'account_lockouts_24h': 0,
            'total_security_events': 0
        }
        
        for event_type, events in security_events.items():
            recent_events = [
                event for event in events
                if datetime.fromisoformat(event['timestamp']) > last_24h
            ]
            
            if event_type == 'FAILED_LOGIN_ATTEMPT':
                stats['failed_logins_24h'] = len(recent_events)
            elif event_type == 'SUSPICIOUS_ACTIVITY':
                stats['suspicious_activities_24h'] = len(recent_events)
            elif event_type == 'ACCOUNT_LOCKOUT':
                stats['account_lockouts_24h'] = len(recent_events)
            
            stats['total_security_events'] += len(events)
        
        return stats

# Rate limiting decorators for different endpoints
class RateLimits:
    """Rate limiting configurations for different endpoints"""
    
    # Authentication endpoints (more restrictive)
    AUTH_LOGIN = "5/minute"  # 5 login attempts per minute
    AUTH_REGISTER = "3/minute"  # 3 registrations per minute
    AUTH_RESET_PASSWORD = "2/minute"  # 2 password reset requests per minute
    
    # API endpoints (moderate)
    API_GENERAL = "60/minute"  # 60 general API calls per minute
    API_ANALYSIS = "10/minute"  # 10 analysis requests per minute
    
    # Admin endpoints (less restrictive for admins)
    ADMIN_GENERAL = "100/minute"  # 100 admin actions per minute

# Custom rate limit exceeded handler
def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded"""
    SecurityMiddleware.log_security_event(
        'RATE_LIMIT_EXCEEDED',
        ip_address=get_remote_address(request),
        details={'endpoint': str(request.url), 'limit': str(exc.detail)}
    )
    
    response = HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={
            "error": "Rate limit exceeded",
            "message": f"Too many requests. {exc.detail}",
            "retry_after": 60
        }
    )
    return response

# Enhanced session security
class SessionSecurity:
    """Enhanced session management and security"""
    
    @staticmethod
    def validate_session_security(user_id: str, ip_address: str, user_agent: str = None) -> bool:
        """Validate session security and detect anomalies"""
        
        # Log successful login
        SecurityMiddleware.log_security_event(
            'USER_LOGIN',
            user_id=user_id,
            ip_address=ip_address,
            details={'user_agent': user_agent}
        )
        
        # Check for suspicious activity
        if SecurityMiddleware.detect_suspicious_activity(user_id, ip_address, user_agent):
            # In production, you might want to require additional verification
            # For now, just log the event
            return True
        
        return True
    
    @staticmethod
    def log_logout(user_id: str, ip_address: str):
        """Log user logout"""
        SecurityMiddleware.log_security_event(
            'USER_LOGOUT',
            user_id=user_id,
            ip_address=ip_address
        )

# Security notification system
class SecurityNotifications:
    """Security notification system for users and admins"""
    
    @staticmethod
    def should_notify_user(event_type: str, user_id: str) -> bool:
        """Determine if user should be notified of security event"""
        notification_events = [
            'SUSPICIOUS_ACTIVITY',
            'PASSWORD_CHANGED',
            'EMAIL_CHANGED',
            'ACCOUNT_LOCKOUT'
        ]
        return event_type in notification_events
    
    @staticmethod
    def should_notify_admin(event_type: str) -> bool:
        """Determine if admin should be notified of security event"""
        admin_notification_events = [
            'SUSPICIOUS_ACTIVITY',
            'ACCOUNT_LOCKOUT',
            'RATE_LIMIT_EXCEEDED',
            'MULTIPLE_FAILED_LOGINS'
        ]
        return event_type in admin_notification_events
    
    @staticmethod
    def create_security_notification(event_type: str, user_id: str = None, details: Dict[str, Any] = None):
        """Create security notification (email, in-app, etc.)"""
        # In production, integrate with email service and in-app notifications
        notification = {
            'type': 'security',
            'event_type': event_type,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat(),
            'details': details or {},
            'read': False
        }
        
        logger.info(f"SECURITY NOTIFICATION: {event_type} for user {user_id}")
        
        # Here you would typically:
        # 1. Save to database
        # 2. Send email notification
        # 3. Create in-app notification
        # 4. Send to admin dashboard if needed
        
        return notification
