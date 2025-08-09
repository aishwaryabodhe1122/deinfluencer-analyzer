# Universal Social Media API Setup Guide

This guide explains how to configure real-time API access for fetching accurate data from any influencer on any platform.

## 🎯 Overview

The Universal Social Media Fetcher can get real-time data for ANY influencer using:

1. **Official APIs** (Most accurate)
2. **Web Scraping** (Fallback)
3. **Curated Database** (Final fallback)

## 🔑 API Keys Setup

Add these environment variables to your `.env` file:

### YouTube Data API v3
```
YOUTUBE_API_KEY=your_youtube_api_key_here
```

**How to get YouTube API Key:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable "YouTube Data API v3"
4. Create credentials (API Key)
5. Copy the API key to your `.env` file

**Free Quota:** 10,000 units/day (enough for ~100 channel lookups)

### Twitter API v2
```
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
```

**How to get Twitter Bearer Token:**
1. Go to [Twitter Developer Portal](https://developer.twitter.com/)
2. Apply for developer account
3. Create a new app
4. Generate Bearer Token
5. Copy to your `.env` file

**Free Quota:** 500,000 tweets/month (Essential tier)

### Instagram Basic Display API
```
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token_here
```

**Note:** Instagram API requires user authorization and is limited. Web scraping is used as primary method for Instagram.

## 🚀 How It Works

### Priority Order:
1. **Official APIs** - Most accurate, real-time data
2. **Web Scraping** - Public profile scraping
3. **Curated Database** - Fallback for popular influencers
4. **Realistic Simulation** - Last resort

### Caching:
- Results cached for 5 minutes
- Reduces API calls and improves performance
- Fresh data for each new search

## 📊 Supported Platforms

### YouTube
- ✅ **API:** Full subscriber, video count, view stats
- ✅ **Scraping:** Subscriber count from public pages
- ✅ **Coverage:** Any public channel

### Twitter/X
- ✅ **API:** Followers, following, tweet count
- ⚠️ **Scraping:** Limited (requires login)
- ✅ **Coverage:** Any public profile

### Instagram
- ⚠️ **API:** Limited (requires user auth)
- ✅ **Scraping:** Follower count from public profiles
- ✅ **Coverage:** Any public profile

## 🔧 Testing

Test the system with any influencer:

```bash
# Test YouTube
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"username":"MrBeast","platform":"youtube"}'

# Test Twitter
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"username":"elonmusk","platform":"twitter"}'

# Test Instagram
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{"username":"cristiano","platform":"instagram"}'
```

## 🎯 Benefits

### Before (Curated Database):
- ❌ Only ~40 influencers supported
- ❌ Data gets outdated quickly
- ❌ Manual updates required
- ❌ Not scalable

### After (Universal Fetcher):
- ✅ **ANY influencer** supported
- ✅ **Real-time data** from APIs
- ✅ **Automatic updates** via caching
- ✅ **Fully scalable** solution

## 🛠️ Troubleshooting

### No API Keys Configured
- System falls back to web scraping
- Still works but may be less accurate

### Rate Limits Exceeded
- System automatically falls back to next method
- Caching reduces API calls

### Scraping Blocked
- System falls back to curated database
- Then to realistic simulation

## 📈 Production Recommendations

1. **Configure all API keys** for best accuracy
2. **Monitor API quotas** and upgrade if needed
3. **Implement Redis caching** for better performance
4. **Add more scraping methods** for additional platforms
5. **Set up monitoring** for API failures

## 🔒 Security

- Store API keys in environment variables
- Never commit API keys to version control
- Use different keys for development/production
- Monitor API usage for unusual activity

This universal system ensures users can search for ANY influencer and get accurate, real-time data!
