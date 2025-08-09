# OAuth Social Authentication Setup Guide

## Current Issue
Social login buttons are redirecting to the landing page because OAuth credentials are not configured. This guide will help you set up social authentication for all 6 platforms.

## Quick Fix for Testing

### Step 1: Copy Environment File
```bash
# In the backend directory
cp .env.example .env
```

### Step 2: Add Basic Configuration
Add these minimal settings to your `.env` file to get started:

```bash
# JWT Secret (required)
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random

# Database (if not already configured)
DATABASE_URL=sqlite:///./nexora.db

# Frontend URL
FRONTEND_URL=http://localhost:3000
```

## OAuth Provider Setup

### 1. Google OAuth 2.0

**Create OAuth App:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Set application type to "Web application"
6. Add authorized redirect URI: `http://localhost:8000/api/auth/google/callback`

**Add to .env:**
```bash
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### 2. GitHub OAuth

**Create OAuth App:**
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in:
   - Application name: "Nexora"
   - Homepage URL: `http://localhost:3000`
   - Authorization callback URL: `http://localhost:8000/api/auth/github/callback`

**Add to .env:**
```bash
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

### 3. Meta/Facebook OAuth

**Create Facebook App:**
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app → "Consumer" type
3. Add "Facebook Login" product
4. In Facebook Login settings:
   - Valid OAuth Redirect URIs: `http://localhost:8000/api/auth/facebook/callback`

**Add to .env:**
```bash
FACEBOOK_CLIENT_ID=your-facebook-app-id
FACEBOOK_CLIENT_SECRET=your-facebook-app-secret
```

### 4. LinkedIn OAuth

**Create LinkedIn App:**
1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create a new app
3. Add "Sign In with LinkedIn" product
4. In Auth settings:
   - Authorized redirect URLs: `http://localhost:8000/api/auth/linkedin/callback`

**Add to .env:**
```bash
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
```

### 5. Twitter/X OAuth

**Create Twitter App:**
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Create a new project and app
3. Enable OAuth 2.0
4. Add callback URL: `http://localhost:8000/api/auth/twitter/callback`

**Add to .env:**
```bash
TWITTER_CLIENT_ID=your-twitter-client-id
TWITTER_CLIENT_SECRET=your-twitter-client-secret
```

## Email Service Setup (Optional)

For email verification and password reset:

### Gmail SMTP Setup:
1. Enable 2-factor authentication on your Gmail account
2. Generate an "App Password" for Nexora
3. Add to .env:

```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-16-character-app-password
FROM_EMAIL=noreply@nexora.com
```

## Testing the Setup

### 1. Restart Backend Server
```bash
# In backend directory
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Test Social Login
1. Go to `http://localhost:3000`
2. Click "Get Started" or "Sign In"
3. Try clicking any social login button
4. Should redirect to the OAuth provider instead of back to landing page

## Troubleshooting

### Social Login Still Redirecting to Landing Page?

**Check Backend Logs:**
- Look for "OAuth credentials not configured" message
- Verify `.env` file is in the backend directory
- Ensure environment variables are loaded correctly

**Verify OAuth Configuration:**
```bash
# Test if OAuth is available
curl http://localhost:8000/api/auth/google/login
# Should redirect to Google OAuth, not back to frontend
```

### Common Issues:

1. **"OAuth unavailable" error:**
   - Check `.env` file exists and has correct credentials
   - Restart backend server after adding credentials

2. **"Invalid redirect URI" error:**
   - Verify callback URLs match exactly in OAuth provider settings
   - Use `http://localhost:8000/api/auth/{provider}/callback`

3. **"Client ID not found" error:**
   - Double-check client ID and secret are correct
   - Ensure no extra spaces in .env file

## Current Status

✅ **Backend OAuth System:** Fully implemented for all 6 platforms
✅ **Frontend UI:** Professional social login buttons ready
✅ **Error Handling:** Improved user feedback for missing credentials
❌ **OAuth Credentials:** Need to be configured in .env file

## Next Steps

1. **Immediate:** Add at least Google and GitHub credentials to test social login
2. **Complete:** Set up all 6 OAuth providers for full functionality
3. **Optional:** Configure email service for verification emails
4. **Production:** Use environment-specific redirect URLs and secure secrets

Once OAuth credentials are configured, the social login buttons will work properly and redirect users through the OAuth flow instead of back to the landing page.
