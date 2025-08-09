"""
Email Service for User Verification and Notifications
Handles email verification, password reset, and notification emails
"""

import smtplib
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional
from decouple import config
import logging

# Email configuration
SMTP_SERVER = config('SMTP_SERVER', default='smtp.gmail.com')
SMTP_PORT = config('SMTP_PORT', default=587, cast=int)
SMTP_USERNAME = config('SMTP_USERNAME', default='')
SMTP_PASSWORD = config('SMTP_PASSWORD', default='')
FROM_EMAIL = config('FROM_EMAIL', default='noreply@nexora.com')
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')

# Email service availability
EMAIL_AVAILABLE = bool(SMTP_USERNAME and SMTP_PASSWORD)

logger = logging.getLogger(__name__)

class EmailService:
    """Email service for sending verification and notification emails"""
    
    def __init__(self):
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        self.username = SMTP_USERNAME
        self.password = SMTP_PASSWORD
        self.from_email = FROM_EMAIL
        
    def _send_email(self, to_email: str, subject: str, html_content: str, text_content: str = None) -> bool:
        """Send email using SMTP"""
        if not EMAIL_AVAILABLE:
            logger.warning("Email service not configured. Skipping email send.")
            return False
            
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
                
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
                
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_verification_email(self, email: str, username: str, verification_token: str) -> bool:
        """Send email verification email to new user"""
        verification_url = f"{FRONTEND_URL}/verify-email?token={verification_token}"
        
        subject = "Welcome to Nexora - Verify Your Email"
        
        # HTML email template
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Verify Your Email - Nexora</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); color: #d4af37; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #d4af37; color: #1a1a1a; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .logo {{ font-size: 28px; font-weight: bold; margin-bottom: 10px; }}
                .tagline {{ font-size: 16px; opacity: 0.9; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">Nexora</div>
                    <div class="tagline">Next Gen Trust Aura</div>
                </div>
                <div class="content">
                    <h2>Welcome to Nexora, {username}!</h2>
                    <p>Thank you for joining Nexora, the next generation platform for analyzing influencer authenticity and trust.</p>
                    <p>To complete your registration and start analyzing influencers, please verify your email address by clicking the button below:</p>
                    <div style="text-align: center;">
                        <a href="{verification_url}" class="button">Verify Email Address</a>
                    </div>
                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; background: #e9ecef; padding: 10px; border-radius: 5px; font-family: monospace;">
                        {verification_url}
                    </p>
                    <p><strong>This verification link will expire in 24 hours.</strong></p>
                    <p>If you didn't create an account with Nexora, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Nexora. All rights reserved.</p>
                    <p>Building trust in the digital influence ecosystem.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Text fallback
        text_content = f"""
        Welcome to Nexora, {username}!
        
        Thank you for joining Nexora, the next generation platform for analyzing influencer authenticity and trust.
        
        To complete your registration, please verify your email address by visiting:
        {verification_url}
        
        This verification link will expire in 24 hours.
        
        If you didn't create an account with Nexora, please ignore this email.
        
        Best regards,
        The Nexora Team
        """
        
        return self._send_email(email, subject, html_content, text_content)
    
    def send_password_reset_email(self, email: str, username: str, reset_token: str) -> bool:
        """Send password reset email"""
        reset_url = f"{FRONTEND_URL}/reset-password?token={reset_token}"
        
        subject = "Nexora - Password Reset Request"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Password Reset - Nexora</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); color: #d4af37; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #d4af37; color: #1a1a1a; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .logo {{ font-size: 28px; font-weight: bold; margin-bottom: 10px; }}
                .tagline {{ font-size: 16px; opacity: 0.9; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">Nexora</div>
                    <div class="tagline">Next Gen Trust Aura</div>
                </div>
                <div class="content">
                    <h2>Password Reset Request</h2>
                    <p>Hello {username},</p>
                    <p>We received a request to reset your password for your Nexora account.</p>
                    <p>Click the button below to reset your password:</p>
                    <div style="text-align: center;">
                        <a href="{reset_url}" class="button">Reset Password</a>
                    </div>
                    <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; background: #e9ecef; padding: 10px; border-radius: 5px; font-family: monospace;">
                        {reset_url}
                    </p>
                    <div class="warning">
                        <strong>Important:</strong>
                        <ul>
                            <li>This reset link will expire in 1 hour</li>
                            <li>If you didn't request this reset, please ignore this email</li>
                            <li>Your password will not be changed unless you click the link above</li>
                        </ul>
                    </div>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Nexora. All rights reserved.</p>
                    <p>Building trust in the digital influence ecosystem.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Password Reset Request - Nexora
        
        Hello {username},
        
        We received a request to reset your password for your Nexora account.
        
        To reset your password, please visit:
        {reset_url}
        
        This reset link will expire in 1 hour.
        
        If you didn't request this reset, please ignore this email.
        Your password will not be changed unless you click the link above.
        
        Best regards,
        The Nexora Team
        """
        
        return self._send_email(email, subject, html_content, text_content)
    
    def send_welcome_email(self, email: str, username: str, role: str) -> bool:
        """Send welcome email after successful verification"""
        subject = "Welcome to Nexora - Your Account is Ready!"
        
        # Role-specific content
        role_content = {
            'consumer': {
                'title': 'Start Analyzing Influencers',
                'features': [
                    'Search and analyze influencers across multiple platforms',
                    'Get detailed authenticity scores and insights',
                    'Save your favorite influencers for quick access',
                    'View your analysis history'
                ]
            },
            'brand': {
                'title': 'Empower Your Marketing Campaigns',
                'features': [
                    'Analyze potential brand partners and collaborators',
                    'Export detailed reports for your team',
                    'Track campaign performance and authenticity',
                    'Access advanced analytics and insights'
                ]
            },
            'admin': {
                'title': 'Manage the Nexora Platform',
                'features': [
                    'Full administrative access to user management',
                    'System analytics and performance monitoring',
                    'Platform configuration and settings',
                    'Advanced reporting and data export'
                ]
            }
        }
        
        role_info = role_content.get(role, role_content['consumer'])
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome to Nexora</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%); color: #d4af37; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #d4af37; color: #1a1a1a; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 14px; }}
                .logo {{ font-size: 28px; font-weight: bold; margin-bottom: 10px; }}
                .tagline {{ font-size: 16px; opacity: 0.9; }}
                .features {{ background: #e9ecef; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .features ul {{ margin: 0; padding-left: 20px; }}
                .features li {{ margin: 10px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="logo">Nexora</div>
                    <div class="tagline">Next Gen Trust Aura</div>
                </div>
                <div class="content">
                    <h2>🎉 Welcome to Nexora, {username}!</h2>
                    <p>Your email has been verified and your account is now active. You're ready to start using Nexora!</p>
                    
                    <h3>{role_info['title']}</h3>
                    <div class="features">
                        <p><strong>With your {role.title()} account, you can:</strong></p>
                        <ul>
                            {''.join([f'<li>{feature}</li>' for feature in role_info['features']])}
                        </ul>
                    </div>
                    
                    <div style="text-align: center;">
                        <a href="{FRONTEND_URL}/dashboard" class="button">Go to Dashboard</a>
                    </div>
                    
                    <p>Need help getting started? Check out our <a href="{FRONTEND_URL}/help">Help Center</a> or contact our support team.</p>
                    
                    <p>Thank you for choosing Nexora to build trust in the digital influence ecosystem!</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 Nexora. All rights reserved.</p>
                    <p>Building trust in the digital influence ecosystem.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(email, subject, html_content)

# Global email service instance
email_service = EmailService()
