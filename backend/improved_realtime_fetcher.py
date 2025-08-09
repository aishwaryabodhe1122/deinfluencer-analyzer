"""
Improved Real-Time Social Media Data Fetcher
Accurate, reliable real-time data fetching for any influencer
"""

import requests
import re
import json
import time
from typing import Dict, Optional
from urllib.parse import quote

class ImprovedRealtimeFetcher:
    """
    Improved real-time data fetcher with accurate scraping methods
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def fetch_realtime_data(self, username: str, platform: str) -> Optional[Dict]:
        """
        Fetch real-time data for any influencer on any platform
        """
        print(f"🔍 IMPROVED FETCHER: Getting REAL-TIME data for {username} on {platform}")
        
        try:
            if platform.lower() == 'youtube':
                return self._fetch_youtube_realtime(username)
            elif platform.lower() in ['twitter', 'x']:
                return self._fetch_twitter_realtime(username)
            elif platform.lower() == 'instagram':
                return self._fetch_instagram_realtime(username)
            else:
                print(f"❌ Platform {platform} not supported")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching real-time data for {username}: {str(e)}")
            return None
    
    def _fetch_youtube_realtime(self, username: str) -> Optional[Dict]:
        """
        Fetch real-time YouTube data using improved methods
        """
        # Try different YouTube URL formats
        url_formats = [
            f"https://www.youtube.com/@{username}",
            f"https://www.youtube.com/c/{username}",
            f"https://www.youtube.com/user/{username}",
            f"https://www.youtube.com/{username}",
            f"https://www.youtube.com/channel/{username}"
        ]
        
        for url in url_formats:
            try:
                print(f"🔍 Trying YouTube URL: {url}")
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Extract channel data from various sources
                    subscriber_count = self._extract_youtube_subscribers(html)
                    video_count = self._extract_youtube_videos(html)
                    channel_name = self._extract_youtube_channel_name(html, username)
                    
                    if subscriber_count and subscriber_count > 1000:
                        print(f"✅ SUCCESS: Real-time YouTube data for {username}: {subscriber_count:,} subscribers")
                        return {
                            'username': channel_name,
                            'platform': 'youtube',
                            'follower_count': subscriber_count,
                            'following_count': 0,
                            'post_count': video_count,
                            'bio': f"YouTube channel: {channel_name}",
                            'verified': subscriber_count > 100000,
                            'engagement_rate': 5.0,
                            'source': 'real-time-scraping',
                            'fetch_time': 'live'
                        }
                        
            except Exception as e:
                print(f"⚠️ YouTube URL {url} failed: {e}")
                continue
        
        print(f"❌ Could not fetch YouTube data for {username}")
        return None
    
    def _extract_youtube_subscribers(self, html: str) -> Optional[int]:
        """Extract subscriber count from YouTube HTML"""
        patterns = [
            # Current YouTube patterns (2024/2025)
            r'"subscriberCountText":\{"accessibility":\{"accessibilityData":\{"label":"([\d.,KMB]+)\s+subscribers?"',
            r'"subscriberCountText":\{"simpleText":"([\d.,KMB]+)\s+subscribers?"',
            r'"subscriberCountText":\{"runs":\[\{"text":"([\d.,KMB]+)"',
            # JSON-LD structured data
            r'"interactionCount":"(\d+)"',
            # Meta tags
            r'<meta property="og:description" content="[^"]*(\d+\.?\d*[KMB]?)\s+subscribers',
            # Page title
            r'<title>[^<]*(\d+\.?\d*[KMB]?)\s+subscribers',
            # Alternative formats
            r'subscribers","simpleText":"([\d.,KMB]+)',
            r'"subscriberCount":"(\d+)"',
            # Fallback patterns
            r'(\d+\.?\d*[KMB]?)\s+subscribers',
            r'subscribers[^>]*>([^<]*\d+[^<]*)</span>',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                count = self._parse_count_string(match)
                if count > 1000:  # Reasonable minimum for YouTube
                    return count
        
        return None
    
    def _extract_youtube_videos(self, html: str) -> int:
        """Extract video count from YouTube HTML"""
        patterns = [
            r'"videosCountText":\{"runs":\[\{"text":"([\d,]+)"',
            r'"videoCount":"(\d+)"',
            r'videos[^>]*>([^<]*\d+[^<]*)</span>',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                try:
                    return int(matches[0].replace(',', ''))
                except:
                    continue
        return 0
    
    def _extract_youtube_channel_name(self, html: str, fallback: str) -> str:
        """Extract channel name from YouTube HTML"""
        patterns = [
            r'<meta property="og:title" content="([^"]+)"',
            r'"channelMetadataRenderer":\{"title":"([^"]+)"',
            r'<title>([^<]+) - YouTube</title>',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                name = match.group(1).strip()
                if name and name != "YouTube":
                    return name
        
        return fallback
    
    def _fetch_instagram_realtime(self, username: str) -> Optional[Dict]:
        """
        Fetch real-time Instagram data using public endpoints
        """
        try:
            # Clean username
            clean_username = username.replace('@', '').strip()
            
            # Try Instagram public profile page
            url = f"https://www.instagram.com/{clean_username}/"
            print(f"🔍 Trying Instagram URL: {url}")
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # Extract follower count
                follower_count = self._extract_instagram_followers(html)
                following_count = self._extract_instagram_following(html)
                post_count = self._extract_instagram_posts(html)
                
                if follower_count and follower_count > 10:
                    print(f"✅ SUCCESS: Real-time Instagram data for {username}: {follower_count:,} followers")
                    return {
                        'username': clean_username,
                        'platform': 'instagram',
                        'follower_count': follower_count,
                        'following_count': following_count,
                        'post_count': post_count,
                        'bio': f"Instagram user: {clean_username}",
                        'verified': follower_count > 100000,
                        'engagement_rate': 3.5,
                        'source': 'real-time-scraping',
                        'fetch_time': 'live'
                    }
                    
        except Exception as e:
            print(f"⚠️ Instagram scraping failed: {e}")
        
        print(f"❌ Could not fetch Instagram data for {username}")
        return None
    
    def _extract_instagram_followers(self, html: str) -> Optional[int]:
        """Extract follower count from Instagram HTML"""
        patterns = [
            # Current Instagram patterns
            r'"edge_followed_by":\{"count":(\d+)\}',
            r'"follower_count":(\d+)',
            r'content="(\d+) Followers',
            r'Followers</span><span[^>]*>([^<]+)</span>',
            r'(\d+\.?\d*[KMB]?)\s+followers',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                count = self._parse_count_string(str(match))
                if count > 10:  # Reasonable minimum
                    return count
        
        return None
    
    def _extract_instagram_following(self, html: str) -> int:
        """Extract following count from Instagram HTML"""
        patterns = [
            r'"edge_follow":\{"count":(\d+)\}',
            r'"following_count":(\d+)',
            r'Following</span><span[^>]*>([^<]+)</span>',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                try:
                    return self._parse_count_string(matches[0])
                except:
                    continue
        return 0
    
    def _extract_instagram_posts(self, html: str) -> int:
        """Extract post count from Instagram HTML"""
        patterns = [
            r'"edge_owner_to_timeline_media":\{"count":(\d+)\}',
            r'"media_count":(\d+)',
            r'Posts</span><span[^>]*>([^<]+)</span>',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                try:
                    return self._parse_count_string(matches[0])
                except:
                    continue
        return 0
    
    def _fetch_twitter_realtime(self, username: str) -> Optional[Dict]:
        """
        Fetch real-time Twitter data using multiple methods
        """
        # Clean username
        clean_username = username.replace('@', '').strip()
        
        # Try multiple Nitter instances (more reliable than direct Twitter)
        nitter_instances = [
            "nitter.net",
            "nitter.it", 
            "nitter.unixfox.eu",
            "nitter.fdn.fr",
            "nitter.1d4.us",
            "nitter.kavin.rocks"
        ]
        
        for instance in nitter_instances:
            try:
                url = f"https://{instance}/{clean_username}"
                print(f"🔍 Trying Nitter: {url}")
                
                response = self.session.get(url, timeout=8)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Extract Twitter data from Nitter
                    follower_count = self._extract_twitter_followers(html)
                    following_count = self._extract_twitter_following(html)
                    tweet_count = self._extract_twitter_tweets(html)
                    
                    if follower_count and follower_count > 1:
                        print(f"✅ SUCCESS: Real-time Twitter data for {username}: {follower_count:,} followers")
                        return {
                            'username': clean_username,
                            'platform': 'twitter',
                            'follower_count': follower_count,
                            'following_count': following_count,
                            'post_count': tweet_count,
                            'bio': f"Twitter user: @{clean_username}",
                            'verified': follower_count > 100000,
                            'engagement_rate': 2.5,
                            'source': 'real-time-scraping',
                            'fetch_time': 'live'
                        }
                        
            except Exception as e:
                print(f"⚠️ Nitter {instance} failed: {e}")
                continue
        
        print(f"❌ Could not fetch Twitter data for {username}")
        return None
    
    def _extract_twitter_followers(self, html: str) -> Optional[int]:
        """Extract follower count from Twitter/Nitter HTML"""
        patterns = [
            # Nitter patterns
            r'class="profile-stat-num"[^>]*>([^<]+)</span>\s*<span[^>]*>Followers',
            r'Followers</span>\s*<span[^>]*>([^<]+)</span>',
            r'(\d+\.?\d*[KMB]?)\s*Followers',
            # Direct Twitter patterns (if accessible)
            r'"followers_count":(\d+)',
            r'Followers[^>]*>([^<]*\d+[^<]*)</span>',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                count = self._parse_count_string(str(match))
                if count > 1:  # Any positive count is valid
                    return count
        
        return None
    
    def _extract_twitter_following(self, html: str) -> int:
        """Extract following count from Twitter/Nitter HTML"""
        patterns = [
            r'class="profile-stat-num"[^>]*>([^<]+)</span>\s*<span[^>]*>Following',
            r'Following</span>\s*<span[^>]*>([^<]+)</span>',
            r'(\d+\.?\d*[KMB]?)\s*Following',
            r'"friends_count":(\d+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                try:
                    return self._parse_count_string(matches[0])
                except:
                    continue
        return 0
    
    def _extract_twitter_tweets(self, html: str) -> int:
        """Extract tweet count from Twitter/Nitter HTML"""
        patterns = [
            r'class="profile-stat-num"[^>]*>([^<]+)</span>\s*<span[^>]*>Tweets',
            r'Tweets</span>\s*<span[^>]*>([^<]+)</span>',
            r'(\d+\.?\d*[KMB]?)\s*Tweets',
            r'"statuses_count":(\d+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                try:
                    return self._parse_count_string(matches[0])
                except:
                    continue
        return 0
    
    def _parse_count_string(self, count_str: str) -> int:
        """
        Parse count strings like '1.2M', '500K', '1,234' to integers
        """
        if not count_str:
            return 0
        
        # Clean the string
        count_str = str(count_str).replace(',', '').strip().lower()
        
        # Remove any HTML entities or extra characters
        count_str = re.sub(r'[^\d.kmb]', '', count_str)
        
        if not count_str:
            return 0
        
        # Handle K, M, B suffixes
        multipliers = {'k': 1000, 'm': 1000000, 'b': 1000000000}
        
        for suffix, multiplier in multipliers.items():
            if count_str.endswith(suffix):
                number_part = count_str[:-1]
                try:
                    return int(float(number_part) * multiplier)
                except ValueError:
                    return 0
        
        # Try to parse as regular number
        try:
            return int(float(count_str))
        except ValueError:
            return 0

# Global instance
improved_fetcher = ImprovedRealtimeFetcher()
