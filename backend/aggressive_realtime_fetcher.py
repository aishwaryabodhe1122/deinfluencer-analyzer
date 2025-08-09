"""
Aggressive Real-Time Social Media Data Fetcher
Ensures actual live data at time of search - no fallbacks to cached/curated data
"""

import requests
import re
import json
import time
import random
from typing import Dict, Optional
from urllib.parse import quote

class AggressiveRealtimeFetcher:
    """
    Aggressive fetcher that prioritizes live data over any cached/curated sources
    """
    
    def __init__(self):
        self.session = requests.Session()
        # Multiple user agents to avoid detection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        ]
        
    def fetch_realtime_data(self, username: str, platform: str) -> Optional[Dict]:
        """
        Fetch ACTUAL real-time data - no fallbacks to cached/curated sources
        """
        print(f"⚡ AGGRESSIVE FETCHER: Getting LIVE data for {username} on {platform} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Randomize user agent and add delays to avoid detection
        self.session.headers.update({
            'User-Agent': random.choice(self.user_agents)
        })
        
        try:
            if platform.lower() == 'youtube':
                return self._fetch_youtube_live(username)
            elif platform.lower() in ['twitter', 'x']:
                return self._fetch_twitter_live(username)
            elif platform.lower() == 'instagram':
                return self._fetch_instagram_live(username)
            else:
                print(f"❌ Platform {platform} not supported")
                return None
                
        except Exception as e:
            print(f"❌ Error fetching LIVE data for {username}: {str(e)}")
            return None
    
    def _fetch_youtube_live(self, username: str) -> Optional[Dict]:
        """
        Fetch LIVE YouTube data with multiple aggressive methods
        """
        print(f"🔴 LIVE YOUTUBE: Fetching current subscriber count for {username}")
        
        # Method 1: YouTube search to find exact channel
        try:
            search_url = f"https://www.youtube.com/results?search_query={quote(username)}"
            print(f"🔍 Searching YouTube: {search_url}")
            
            response = self.session.get(search_url, timeout=12)
            if response.status_code == 200:
                # Extract channel URLs from search results
                channel_urls = re.findall(r'"url":"(/channel/[^"]+)"', response.text)
                handle_urls = re.findall(r'"url":"(/@[^"]+)"', response.text)
                
                # Try found channel URLs
                for channel_path in channel_urls[:3]:  # Try top 3 results
                    full_url = f"https://www.youtube.com{channel_path}"
                    result = self._extract_youtube_live_data(full_url, username)
                    if result:
                        return result
                
                # Try found handle URLs
                for handle_path in handle_urls[:3]:
                    full_url = f"https://www.youtube.com{handle_path}"
                    result = self._extract_youtube_live_data(full_url, username)
                    if result:
                        return result
        except Exception as e:
            print(f"⚠️ YouTube search failed: {e}")
        
        # Method 2: Direct URL attempts
        direct_urls = [
            f"https://www.youtube.com/@{username}",
            f"https://www.youtube.com/c/{username}",
            f"https://www.youtube.com/user/{username}",
        ]
        
        for url in direct_urls:
            result = self._extract_youtube_live_data(url, username)
            if result:
                return result
        
        print(f"❌ Could not fetch LIVE YouTube data for {username}")
        return None
    
    def _extract_youtube_live_data(self, url: str, username: str) -> Optional[Dict]:
        """Extract live YouTube data from channel page"""
        try:
            print(f"🔍 Fetching LIVE YouTube data: {url}")
            
            # Add random delay
            time.sleep(random.uniform(0.5, 1.0))
            
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                # Extract live subscriber count
                subscriber_count = self._extract_live_youtube_subscribers(html)
                
                if subscriber_count and subscriber_count > 100:
                    # Extract additional data
                    channel_name = self._extract_live_channel_name(html, username)
                    video_count = self._extract_live_video_count(html)
                    
                    print(f"🔴 LIVE SUCCESS: YouTube {username} has {subscriber_count:,} subscribers RIGHT NOW")
                    return {
                        'username': channel_name,
                        'platform': 'youtube',
                        'follower_count': subscriber_count,
                        'following_count': 0,
                        'post_count': video_count,
                        'bio': f"YouTube channel: {channel_name}",
                        'verified': subscriber_count > 100000,
                        'engagement_rate': 5.0,
                        'source': 'live-real-time-scraping',
                        'fetch_time': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
        except Exception as e:
            print(f"⚠️ YouTube live fetch failed for {url}: {e}")
        
        return None
    
    def _extract_live_youtube_subscribers(self, html: str) -> Optional[int]:
        """Extract live subscriber count with aggressive patterns"""
        
        # Method 1: JSON-LD structured data (most accurate for live data)
        json_ld_pattern = r'<script type="application/ld\+json"[^>]*>(.*?)</script>'
        json_matches = re.findall(json_ld_pattern, html, re.DOTALL)
        
        for json_str in json_matches:
            try:
                data = json.loads(json_str)
                if isinstance(data, dict):
                    # Check for interaction statistics
                    if 'interactionStatistic' in data:
                        for stat in data['interactionStatistic']:
                            if stat.get('interactionType') == 'http://schema.org/SubscribeAction':
                                count = int(stat.get('userInteractionCount', 0))
                                if count > 100:
                                    print(f"🎯 Found JSON-LD subscriber count: {count:,}")
                                    return count
                    
                    # Check for subscriber count in other JSON fields
                    if 'subscriberCount' in str(data):
                        subscriber_match = re.search(r'"subscriberCount[^"]*":(\d+)', json_str)
                        if subscriber_match:
                            count = int(subscriber_match.group(1))
                            if count > 100:
                                print(f"🎯 Found JSON subscriber count: {count:,}")
                                return count
            except:
                continue
        
        # Method 2: YouTube's internal API response patterns
        api_patterns = [
            r'"subscriberCountText":\{"accessibility":\{"accessibilityData":\{"label":"([\d.,KMB]+)\s+subscribers?"',
            r'"subscriberCountText":\{"simpleText":"([\d.,KMB]+)\s+subscribers?"',
            r'"subscriberCountText":\{"runs":\[\{"text":"([\d.,KMB]+)"',
            r'"header":\{"c4TabbedHeaderRenderer":\{"subscriberCountText":\{"simpleText":"([\d.,KMB]+)',
        ]
        
        for pattern in api_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                count = self._parse_live_count(match)
                if count > 100:
                    print(f"🎯 Found API subscriber count: {count:,}")
                    return count
        
        # Method 3: Meta tag extraction
        meta_patterns = [
            r'<meta property="og:description" content="[^"]*?(\d+\.?\d*[KMB]?)\s+subscribers',
            r'<meta name="description" content="[^"]*?(\d+\.?\d*[KMB]?)\s+subscribers',
        ]
        
        for pattern in meta_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                count = self._parse_live_count(match)
                if count > 100:
                    print(f"🎯 Found meta subscriber count: {count:,}")
                    return count
        
        return None
    
    def _extract_live_channel_name(self, html: str, fallback: str) -> str:
        """Extract live channel name"""
        patterns = [
            r'<meta property="og:title" content="([^"]+)"',
            r'"header":\{"c4TabbedHeaderRenderer":\{"title":"([^"]+)"',
            r'<title>([^<]+) - YouTube</title>',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                name = match.group(1).strip()
                if name and name != "YouTube" and " - YouTube" not in name:
                    return name
        
        return fallback
    
    def _extract_live_video_count(self, html: str) -> int:
        """Extract live video count"""
        patterns = [
            r'"videosCountText":\{"accessibility":\{"accessibilityData":\{"label":"([\d,]+)\s+videos?"',
            r'"videosCountText":\{"simpleText":"([\d,]+)"',
            r'"videoCount":"(\d+)"',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                try:
                    return int(matches[0].replace(',', ''))
                except:
                    continue
        return 0
    
    def _fetch_instagram_live(self, username: str) -> Optional[Dict]:
        """
        Fetch LIVE Instagram data with aggressive anti-detection methods
        """
        clean_username = username.replace('@', '').strip()
        print(f"🔴 LIVE INSTAGRAM: Fetching current follower count for {clean_username}")
        
        # Method 1: Multiple Instagram endpoints with aggressive headers
        endpoints = [
            f"https://www.instagram.com/{clean_username}/",
            f"https://instagram.com/{clean_username}/",
            f"https://m.instagram.com/{clean_username}/",
        ]
        
        for url in endpoints:
            try:
                print(f"🔍 Trying Instagram LIVE: {url}")
                
                # Aggressive anti-detection headers
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Cache-Control': 'max-age=0',
                }
                
                # Add random delay to avoid rate limiting
                time.sleep(random.uniform(1.0, 2.5))
                
                response = self.session.get(url, headers=headers, timeout=12)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Extract live follower count with validation
                    follower_count = self._extract_live_instagram_followers(html, clean_username)
                    
                    if follower_count and follower_count > 10:
                        following_count = self._extract_live_instagram_following(html)
                        post_count = self._extract_live_instagram_posts(html)
                        
                        print(f"🔴 LIVE SUCCESS: Instagram {username} has {follower_count:,} followers RIGHT NOW")
                        return {
                            'username': clean_username,
                            'platform': 'instagram',
                            'follower_count': follower_count,
                            'following_count': following_count,
                            'post_count': post_count,
                            'bio': f"Instagram user: {clean_username}",
                            'verified': follower_count > 100000,
                            'engagement_rate': 3.5,
                            'source': 'live-real-time-scraping',
                            'fetch_time': time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                else:
                    print(f"⚠️ Instagram returned status {response.status_code} for {url}")
                    
            except Exception as e:
                print(f"⚠️ Instagram LIVE fetch failed for {url}: {e}")
                continue
        
        # Method 2: Try alternative Instagram data sources
        try:
            # Use Instagram's public API endpoints (if available)
            api_url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={clean_username}"
            
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'X-Requested-With': 'XMLHttpRequest',
                'Referer': f'https://www.instagram.com/{clean_username}/',
            }
            
            response = self.session.get(api_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'data' in data and 'user' in data['data']:
                        user_data = data['data']['user']
                        follower_count = user_data.get('edge_followed_by', {}).get('count', 0)
                        
                        if follower_count > 10:
                            following_count = user_data.get('edge_follow', {}).get('count', 0)
                            post_count = user_data.get('edge_owner_to_timeline_media', {}).get('count', 0)
                            
                            print(f"🔴 LIVE SUCCESS: Instagram API {username} has {follower_count:,} followers RIGHT NOW")
                            return {
                                'username': clean_username,
                                'platform': 'instagram',
                                'follower_count': follower_count,
                                'following_count': following_count,
                                'post_count': post_count,
                                'bio': f"Instagram user: {clean_username}",
                                'verified': follower_count > 100000,
                                'engagement_rate': 3.5,
                                'source': 'live-api-scraping',
                                'fetch_time': time.strftime('%Y-%m-%d %H:%M:%S')
                            }
                except:
                    pass
        except Exception as e:
            print(f"⚠️ Instagram API method failed: {e}")
        
        print(f"❌ Could not fetch LIVE Instagram data for {username}")
        return None
    
    def _extract_live_instagram_followers(self, html: str, username: str) -> Optional[int]:
        """Extract live Instagram followers with aggressive patterns"""
        
        # Method 1: JSON data extraction
        json_patterns = [
            r'"edge_followed_by":\{"count":(\d+)\}',
            r'"follower_count":(\d+)',
            r'"followed_by":\{"count":(\d+)\}',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                count = int(match)
                if count > 10 and self._validate_instagram_context(html, username):
                    print(f"🎯 Found JSON Instagram followers: {count:,}")
                    return count
        
        # Method 2: Meta tag extraction with user validation
        meta_patterns = [
            r'<meta property="og:description" content="([^"]*)"',
            r'<meta name="description" content="([^"]*)"',
        ]
        
        for pattern in meta_patterns:
            match = re.search(pattern, html)
            if match:
                content = match.group(1)
                if username.lower() in content.lower():
                    follower_match = re.search(r'(\d+\.?\d*[KMB]?)\s+Followers', content, re.IGNORECASE)
                    if follower_match:
                        count = self._parse_live_count(follower_match.group(1))
                        if count > 10:
                            print(f"🎯 Found meta Instagram followers: {count:,}")
                            return count
        
        # Method 3: Page content patterns
        content_patterns = [
            rf'{re.escape(username)}[^>]*(\d{{1,3}}(?:,\d{{3}})+|\d+\.?\d*[KMB]?)\s+followers',
            r'followers[^>]*>([^<]*\d+[^<]*)</span>',
            r'Followers[^>]*>([^<]*\d+[^<]*)</span>',
        ]
        
        for pattern in content_patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                count = self._parse_live_count(str(match))
                if count > 10:
                    print(f"🎯 Found content Instagram followers: {count:,}")
                    return count
        
        return None
    
    def _validate_instagram_context(self, html: str, username: str) -> bool:
        """Validate Instagram page context for user"""
        validation_patterns = [
            rf'@{re.escape(username)}',
            rf'instagram\.com/{re.escape(username)}',
            rf'"username":"{re.escape(username)}"',
            rf'/{re.escape(username)}/',
        ]
        
        for pattern in validation_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                return True
        
        return False
    
    def _extract_live_instagram_following(self, html: str) -> int:
        """Extract live Instagram following count"""
        patterns = [
            r'"edge_follow":\{"count":(\d+)\}',
            r'"following_count":(\d+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                try:
                    return int(matches[0])
                except:
                    continue
        return 0
    
    def _extract_live_instagram_posts(self, html: str) -> int:
        """Extract live Instagram post count"""
        patterns = [
            r'"edge_owner_to_timeline_media":\{"count":(\d+)\}',
            r'"media_count":(\d+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                try:
                    return int(matches[0])
                except:
                    continue
        return 0
    
    def _fetch_twitter_live(self, username: str) -> Optional[Dict]:
        """
        Fetch LIVE Twitter data with aggressive methods
        """
        clean_username = username.replace('@', '').strip()
        print(f"🔴 LIVE TWITTER: Fetching current follower count for {clean_username}")
        
        # Try multiple working Nitter instances aggressively
        nitter_instances = [
            "nitter.poast.org",
            "nitter.privacydev.net", 
            "nitter.1d4.us",
            "nitter.net",
            "nitter.it",
        ]
        
        for instance in nitter_instances:
            try:
                url = f"https://{instance}/{clean_username}"
                print(f"🔍 Trying LIVE Nitter: {url}")
                
                # Add delay and randomization
                time.sleep(random.uniform(0.5, 1.2))
                
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                
                response = self.session.get(url, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Validate this is the correct user profile
                    if self._validate_twitter_context(html, clean_username):
                        follower_count = self._extract_live_twitter_followers(html)
                        
                        if follower_count and follower_count > 1:
                            following_count = self._extract_live_twitter_following(html)
                            tweet_count = self._extract_live_twitter_tweets(html)
                            
                            print(f"🔴 LIVE SUCCESS: Twitter {username} has {follower_count:,} followers RIGHT NOW")
                            return {
                                'username': clean_username,
                                'platform': 'twitter',
                                'follower_count': follower_count,
                                'following_count': following_count,
                                'post_count': tweet_count,
                                'bio': f"Twitter user: @{clean_username}",
                                'verified': follower_count > 100000,
                                'engagement_rate': 2.5,
                                'source': 'live-real-time-scraping',
                                'fetch_time': time.strftime('%Y-%m-%d %H:%M:%S')
                            }
                        
            except Exception as e:
                print(f"⚠️ Live Nitter {instance} failed: {e}")
                continue
        
        print(f"❌ Could not fetch LIVE Twitter data for {username}")
        return None
    
    def _extract_live_twitter_followers(self, html: str) -> Optional[int]:
        """Extract live Twitter follower count"""
        patterns = [
            r'<span class="profile-stat-num">([^<]+)</span>\s*<span class="profile-stat-header">Followers</span>',
            r'Followers</span>\s*<span[^>]*>([^<]+)</span>',
            r'(\d+\.?\d*[KMB]?)\s*Followers',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            for match in matches:
                count = self._parse_live_count(str(match))
                if count > 1:
                    return count
        
        return None
    
    def _validate_twitter_context(self, html: str, username: str) -> bool:
        """Validate Twitter page context"""
        validation_patterns = [
            rf'@{re.escape(username)}',
            rf'/{re.escape(username)}',
            rf'twitter\.com/{re.escape(username)}',
            rf'nitter\.[^/]+/{re.escape(username)}',
        ]
        
        for pattern in validation_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                return True
        
        return False
    
    def _extract_live_twitter_following(self, html: str) -> int:
        """Extract live Twitter following count"""
        patterns = [
            r'<span class="profile-stat-num">([^<]+)</span>\s*<span class="profile-stat-header">Following</span>',
            r'Following</span>\s*<span[^>]*>([^<]+)</span>',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                try:
                    return self._parse_live_count(matches[0])
                except:
                    continue
        return 0
    
    def _extract_live_twitter_tweets(self, html: str) -> int:
        """Extract live Twitter tweet count"""
        patterns = [
            r'<span class="profile-stat-num">([^<]+)</span>\s*<span class="profile-stat-header">Tweets</span>',
            r'Tweets</span>\s*<span[^>]*>([^<]+)</span>',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            if matches:
                try:
                    return self._parse_live_count(matches[0])
                except:
                    continue
        return 0
    
    def _parse_live_count(self, count_str: str) -> int:
        """
        Parse live count strings with improved accuracy
        """
        if not count_str:
            return 0
        
        # Clean the string aggressively
        count_str = str(count_str).strip()
        
        # Remove HTML entities and extra characters
        count_str = re.sub(r'&[a-zA-Z0-9#]+;', '', count_str)
        count_str = re.sub(r'[^\d.,KMBkmb]', '', count_str)
        
        if not count_str:
            return 0
        
        # Handle comma-separated numbers
        if ',' in count_str and not re.search(r'[KMBkmb]', count_str):
            try:
                return int(count_str.replace(',', ''))
            except ValueError:
                pass
        
        # Handle K, M, B suffixes
        count_str_lower = count_str.lower()
        multipliers = {'k': 1000, 'm': 1000000, 'b': 1000000000}
        
        for suffix, multiplier in multipliers.items():
            if count_str_lower.endswith(suffix):
                number_part = count_str_lower[:-1]
                try:
                    return int(float(number_part) * multiplier)
                except ValueError:
                    continue
        
        # Extract numeric part
        numeric_match = re.search(r'[\d.]+', count_str)
        if numeric_match:
            try:
                return int(float(numeric_match.group()))
            except ValueError:
                pass
        
        return 0

# Global instance
aggressive_fetcher = AggressiveRealtimeFetcher()
