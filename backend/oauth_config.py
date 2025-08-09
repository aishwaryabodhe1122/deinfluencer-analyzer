"""
OAuth Configuration Module
Handles Google and GitHub OAuth integration for social authentication
"""

import os
from typing import Dict, Any, Optional
import httpx
import json

# Optional OAuth imports - gracefully handle missing dependencies
try:
    from authlib.integrations.starlette_client import OAuth
    from starlette.config import Config
    OAUTH_AVAILABLE = True
except ImportError:
    print("Warning: OAuth dependencies not installed. Social authentication will be disabled.")
    OAUTH_AVAILABLE = False
    OAuth = None
    Config = None

# Load environment variables and OAuth configuration
if OAUTH_AVAILABLE:
    config = Config('.env')
    oauth = OAuth(config)
    
    # Check if we have valid OAuth credentials for all platforms
    google_client_id = config('GOOGLE_CLIENT_ID', default='')
    google_client_secret = config('GOOGLE_CLIENT_SECRET', default='')
    github_client_id = config('GITHUB_CLIENT_ID', default='')
    github_client_secret = config('GITHUB_CLIENT_SECRET', default='')
    facebook_client_id = config('FACEBOOK_CLIENT_ID', default='')
    facebook_client_secret = config('FACEBOOK_CLIENT_SECRET', default='')
    linkedin_client_id = config('LINKEDIN_CLIENT_ID', default='')
    linkedin_client_secret = config('LINKEDIN_CLIENT_SECRET', default='')
    twitter_client_id = config('TWITTER_CLIENT_ID', default='')
    twitter_client_secret = config('TWITTER_CLIENT_SECRET', default='')
    
    # Check which platforms have valid credentials
    has_google_creds = google_client_id and google_client_secret
    has_github_creds = github_client_id and github_client_secret
    has_facebook_creds = facebook_client_id and facebook_client_secret
    has_linkedin_creds = linkedin_client_id and linkedin_client_secret
    has_twitter_creds = twitter_client_id and twitter_client_secret
    
    # Only consider OAuth available if we have at least one set of valid credentials
    if not (has_google_creds or has_github_creds or has_facebook_creds or has_linkedin_creds or has_twitter_creds):
        print("Warning: OAuth credentials not configured. Social authentication will be disabled.")
        OAUTH_AVAILABLE = False
        oauth = None
else:
    config = None
    oauth = None

# OAuth provider registration (only if OAuth is available and we have credentials)
if OAUTH_AVAILABLE and oauth and config:
    google_client_id = config('GOOGLE_CLIENT_ID', default='')
    google_client_secret = config('GOOGLE_CLIENT_SECRET', default='')
    github_client_id = config('GITHUB_CLIENT_ID', default='')
    github_client_secret = config('GITHUB_CLIENT_SECRET', default='')
    facebook_client_id = config('FACEBOOK_CLIENT_ID', default='')
    facebook_client_secret = config('FACEBOOK_CLIENT_SECRET', default='')
    linkedin_client_id = config('LINKEDIN_CLIENT_ID', default='')
    linkedin_client_secret = config('LINKEDIN_CLIENT_SECRET', default='')
    twitter_client_id = config('TWITTER_CLIENT_ID', default='')
    twitter_client_secret = config('TWITTER_CLIENT_SECRET', default='')
    
    # Only register providers for which we have credentials
    if google_client_id and google_client_secret:
        oauth.register(
            name='google',
            client_id=google_client_id,
            client_secret=google_client_secret,
            server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
            client_kwargs={
                'scope': 'openid email profile'
            }
        )
    
    if github_client_id and github_client_secret:
        oauth.register(
            name='github',
            client_id=github_client_id,
            client_secret=github_client_secret,
            access_token_url='https://github.com/login/oauth/access_token',
            authorize_url='https://github.com/login/oauth/authorize',
            api_base_url='https://api.github.com/',
            client_kwargs={'scope': 'user:email'},
        )
    
    # Facebook/Meta OAuth (Instagram uses Facebook's OAuth system)
    if facebook_client_id and facebook_client_secret:
        oauth.register(
            name='facebook',
            client_id=facebook_client_id,
            client_secret=facebook_client_secret,
            access_token_url='https://graph.facebook.com/oauth/access_token',
            authorize_url='https://www.facebook.com/dialog/oauth',
            api_base_url='https://graph.facebook.com/',
            client_kwargs={'scope': 'email public_profile'},
        )
        
        # Instagram uses Facebook's OAuth system with additional scope
        oauth.register(
            name='instagram',
            client_id=facebook_client_id,
            client_secret=facebook_client_secret,
            access_token_url='https://graph.facebook.com/oauth/access_token',
            authorize_url='https://www.facebook.com/dialog/oauth',
            api_base_url='https://graph.facebook.com/',
            client_kwargs={'scope': 'email public_profile instagram_basic'},
        )
    
    # LinkedIn OAuth
    if linkedin_client_id and linkedin_client_secret:
        oauth.register(
            name='linkedin',
            client_id=linkedin_client_id,
            client_secret=linkedin_client_secret,
            access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
            authorize_url='https://www.linkedin.com/oauth/v2/authorization',
            api_base_url='https://api.linkedin.com/',
            client_kwargs={'scope': 'r_liteprofile r_emailaddress'},
        )
    
    # X (Twitter) OAuth 2.0
    if twitter_client_id and twitter_client_secret:
        oauth.register(
            name='twitter',
            client_id=twitter_client_id,
            client_secret=twitter_client_secret,
            access_token_url='https://api.twitter.com/2/oauth2/token',
            authorize_url='https://twitter.com/i/oauth2/authorize',
            api_base_url='https://api.twitter.com/',
            client_kwargs={
                'scope': 'tweet.read users.read',
                'code_challenge_method': 'S256'
            },
        )

class SocialAuthProvider:
    """Handle social authentication providers"""
    
    @staticmethod
    async def get_google_user_info(token: str) -> Optional[Dict[str, Any]]:
        """Fetch user information from Google using access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'https://www.googleapis.com/oauth2/v2/userinfo',
                    headers={'Authorization': f'Bearer {token}'}
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Error fetching Google user info: {str(e)}")
            return None
    
    @staticmethod
    async def get_github_user_info(token: str) -> Optional[Dict[str, Any]]:
        """Fetch user information from GitHub using access token"""
        try:
            async with httpx.AsyncClient() as client:
                # Get user profile
                user_response = await client.get(
                    'https://api.github.com/user',
                    headers={'Authorization': f'token {token}'}
                )
                
                if user_response.status_code != 200:
                    return None
                
                user_data = user_response.json()
                
                # Get user email (GitHub may not provide email in profile)
                email_response = await client.get(
                    'https://api.github.com/user/emails',
                    headers={'Authorization': f'token {token}'}
                )
                
                if email_response.status_code == 200:
                    emails = email_response.json()
                    # Find primary email
                    primary_email = next(
                        (email['email'] for email in emails if email['primary']), 
                        user_data.get('email')
                    )
                    user_data['email'] = primary_email
                
                return user_data
        except Exception as e:
            print(f"Error fetching GitHub user info: {str(e)}")
            return None
    
    @staticmethod
    async def get_facebook_user_info(token: str) -> Optional[Dict[str, Any]]:
        """Fetch user information from Facebook using access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'https://graph.facebook.com/me?fields=id,name,email,picture',
                    headers={'Authorization': f'Bearer {token}'}
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Error fetching Facebook user info: {str(e)}")
            return None
    
    @staticmethod
    async def get_instagram_user_info(token: str) -> Optional[Dict[str, Any]]:
        """Fetch user information from Instagram using access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'https://graph.facebook.com/me?fields=id,name,email,picture',
                    headers={'Authorization': f'Bearer {token}'}
                )
                if response.status_code == 200:
                    return response.json()
                return None
        except Exception as e:
            print(f"Error fetching Instagram user info: {str(e)}")
            return None
    
    @staticmethod
    async def get_linkedin_user_info(token: str) -> Optional[Dict[str, Any]]:
        """Fetch user information from LinkedIn using access token"""
        try:
            async with httpx.AsyncClient() as client:
                # Get user profile
                profile_response = await client.get(
                    'https://api.linkedin.com/v2/people/~?projection=(id,firstName,lastName,profilePicture(displayImage~:playableStreams))',
                    headers={'Authorization': f'Bearer {token}'}
                )
                
                if profile_response.status_code != 200:
                    return None
                
                profile_data = profile_response.json()
                
                # Get user email
                email_response = await client.get(
                    'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))',
                    headers={'Authorization': f'Bearer {token}'}
                )
                
                user_data = {
                    'id': profile_data.get('id'),
                    'firstName': profile_data.get('firstName', {}).get('localized', {}),
                    'lastName': profile_data.get('lastName', {}).get('localized', {}),
                }
                
                if email_response.status_code == 200:
                    email_data = email_response.json()
                    elements = email_data.get('elements', [])
                    if elements:
                        user_data['email'] = elements[0].get('handle~', {}).get('emailAddress')
                
                return user_data
        except Exception as e:
            print(f"Error fetching LinkedIn user info: {str(e)}")
            return None
    
    @staticmethod
    async def get_twitter_user_info(token: str) -> Optional[Dict[str, Any]]:
        """Fetch user information from Twitter using access token"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'https://api.twitter.com/2/users/me?user.fields=id,name,username,profile_image_url',
                    headers={'Authorization': f'Bearer {token}'}
                )
                if response.status_code == 200:
                    return response.json().get('data', {})
                return None
        except Exception as e:
            print(f"Error fetching Twitter user info: {str(e)}")
            return None
    
    @staticmethod
    def normalize_user_data(provider: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize user data from different providers to a common format"""
        if provider == 'google':
            return {
                'email': user_data.get('email'),
                'full_name': user_data.get('name'),
                'username': user_data.get('email', '').split('@')[0],  # Use email prefix as username
                'avatar_url': user_data.get('picture'),
                'provider': 'google',
                'provider_id': user_data.get('id'),
                'verified': user_data.get('verified_email', False)
            }
        elif provider == 'github':
            return {
                'email': user_data.get('email'),
                'full_name': user_data.get('name') or user_data.get('login'),
                'username': user_data.get('login'),
                'avatar_url': user_data.get('avatar_url'),
                'provider': 'github',
                'provider_id': str(user_data.get('id')),
                'verified': True  # GitHub emails are generally verified
            }
        elif provider == 'facebook':
            return {
                'email': user_data.get('email'),
                'full_name': user_data.get('name'),
                'username': user_data.get('email', '').split('@')[0] if user_data.get('email') else user_data.get('name', '').replace(' ', '').lower(),
                'avatar_url': user_data.get('picture', {}).get('data', {}).get('url'),
                'provider': 'facebook',
                'provider_id': str(user_data.get('id')),
                'verified': True  # Facebook emails are generally verified
            }
        elif provider == 'instagram':
            return {
                'email': user_data.get('email'),
                'full_name': user_data.get('name'),
                'username': user_data.get('email', '').split('@')[0] if user_data.get('email') else user_data.get('name', '').replace(' ', '').lower(),
                'avatar_url': user_data.get('picture', {}).get('data', {}).get('url'),
                'provider': 'instagram',
                'provider_id': str(user_data.get('id')),
                'verified': True  # Instagram emails are generally verified
            }
        elif provider == 'linkedin':
            # LinkedIn has a complex name structure
            first_name_data = user_data.get('firstName', {}).get('localized', {})
            last_name_data = user_data.get('lastName', {}).get('localized', {})
            first_name = list(first_name_data.values())[0] if first_name_data else ''
            last_name = list(last_name_data.values())[0] if last_name_data else ''
            full_name = f"{first_name} {last_name}".strip()
            
            return {
                'email': user_data.get('email'),
                'full_name': full_name,
                'username': user_data.get('email', '').split('@')[0] if user_data.get('email') else full_name.replace(' ', '').lower(),
                'avatar_url': None,  # LinkedIn profile pictures require additional API calls
                'provider': 'linkedin',
                'provider_id': str(user_data.get('id')),
                'verified': True  # LinkedIn emails are generally verified
            }
        elif provider == 'twitter':
            return {
                'email': None,  # Twitter API v2 doesn't provide email in basic scope
                'full_name': user_data.get('name'),
                'username': user_data.get('username'),
                'avatar_url': user_data.get('profile_image_url'),
                'provider': 'twitter',
                'provider_id': str(user_data.get('id')),
                'verified': False  # No email verification info available
            }
        else:
            return {}

# Social auth provider instance
social_auth_provider = SocialAuthProvider()
