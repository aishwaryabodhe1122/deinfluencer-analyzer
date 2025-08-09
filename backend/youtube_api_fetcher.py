"""
YouTube Data API v3 Fetcher
Fetches ACTUAL REAL-TIME subscriber counts directly from YouTube's official API
"""

import requests
import os
import time
from typing import Dict, Optional, List
from urllib.parse import quote

class YouTubeAPIFetcher:
    def __init__(self):
        # YouTube Data API v3 key (free tier: 10,000 requests/day)
        self.api_key = os.getenv("YOUTUBE_API_KEY", "AIzaSyDummy_Key_Replace_With_Real")
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
        # Backup: Use public YouTube RSS and search endpoints
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def fetch_realtime_data(self, username: str, platform: str) -> Optional[Dict]:
        """
        Fetch ACTUAL REAL-TIME YouTube data using official API
        """
        if platform.lower() != "youtube":
            return None
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"🔴 YOUTUBE API FETCHER: Getting ACTUAL LIVE data for {username} at {current_time}")
        
        # Method 1: Try YouTube Data API v3 (most reliable)
        data = self._fetch_via_youtube_api(username)
        if data:
            return data
        
        # Method 2: Try YouTube RSS feeds (reliable backup)
        data = self._fetch_via_youtube_rss(username)
        if data:
            return data
        
        # Method 3: Try YouTube search API (public endpoint)
        data = self._fetch_via_youtube_search(username)
        if data:
            return data
        
        print(f"❌ Could not fetch LIVE YouTube data for {username}")
        return None
    
    def _fetch_via_youtube_api(self, username: str) -> Optional[Dict]:
        """
        Fetch data using YouTube Data API v3 (official, most reliable)
        """
        clean_username = username.replace('@', '').strip()
        
        try:
            # Step 1: Search for the channel
            search_url = f"{self.base_url}/search"
            search_params = {
                'part': 'snippet',
                'q': clean_username,
                'type': 'channel',
                'maxResults': 5,
                'key': self.api_key
            }
            
            print(f"🔍 YouTube API: Searching for channel {clean_username}")
            response = requests.get(search_url, params=search_params, timeout=10)
            
            if response.status_code == 200:
                search_data = response.json()
                
                # Find the best matching channel
                channel_id = None
                for item in search_data.get('items', []):
                    channel_title = item['snippet']['title'].lower()
                    if clean_username.lower() in channel_title or channel_title in clean_username.lower():
                        channel_id = item['snippet']['channelId']
                        break
                
                if not channel_id and search_data.get('items'):
                    # Take the first result if no exact match
                    channel_id = search_data['items'][0]['snippet']['channelId']
                
                if channel_id:
                    # Step 2: Get channel statistics
                    stats_url = f"{self.base_url}/channels"
                    stats_params = {
                        'part': 'snippet,statistics',
                        'id': channel_id,
                        'key': self.api_key
                    }
                    
                    print(f"🔍 YouTube API: Getting stats for channel {channel_id}")
                    stats_response = requests.get(stats_url, params=stats_params, timeout=10)
                    
                    if stats_response.status_code == 200:
                        stats_data = stats_response.json()
                        
                        if stats_data.get('items'):
                            channel_info = stats_data['items'][0]
                            subscriber_count = int(channel_info['statistics'].get('subscriberCount', 0))
                            video_count = int(channel_info['statistics'].get('videoCount', 0))
                            channel_name = channel_info['snippet']['title']
                            
                            print(f"✅ SUCCESS: YouTube API data for {clean_username}: {subscriber_count:,} subscribers")
                            
                            return {
                                'username': channel_name,
                                'follower_count': subscriber_count,
                                'following_count': 0,
                                'post_count': video_count,
                                'platform': 'youtube',
                                'verified': True,
                                'engagement_rate': 0.05,
                                'source': 'youtube_api_v3'
                            }
            
            elif response.status_code == 403:
                print(f"⚠️ YouTube API quota exceeded or invalid key")
            else:
                print(f"⚠️ YouTube API error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ YouTube API error: {str(e)}")
        
        return None
    
    def _fetch_via_youtube_rss(self, username: str) -> Optional[Dict]:
        """
        Fetch data using YouTube RSS feeds (reliable backup)
        """
        clean_username = username.replace('@', '').strip()
        
        try:
            # Try different RSS feed formats
            rss_urls = [
                f"https://www.youtube.com/feeds/videos.xml?user={clean_username}",
                f"https://www.youtube.com/feeds/videos.xml?channel_id={clean_username}",
            ]
            
            for rss_url in rss_urls:
                try:
                    print(f"🔍 YouTube RSS: Trying {rss_url}")
                    response = self.session.get(rss_url, timeout=10)
                    
                    if response.status_code == 200 and 'xml' in response.headers.get('content-type', ''):
                        xml_content = response.text
                        
                        # Extract channel info from RSS
                        import re
                        
                        # Extract channel name
                        name_match = re.search(r'<name>([^<]+)</name>', xml_content)
                        channel_name = name_match.group(1) if name_match else clean_username
                        
                        # Extract channel ID for further lookup
                        channel_id_match = re.search(r'channel_id=([^"&]+)', xml_content)
                        if channel_id_match:
                            channel_id = channel_id_match.group(1)
                            
                            # Now try to get subscriber count via channel page
                            channel_data = self._get_channel_stats_from_id(channel_id)
                            if channel_data:
                                channel_data['username'] = channel_name
                                channel_data['source'] = 'youtube_rss'
                                return channel_data
                        
                        print(f"✅ Found RSS feed for {clean_username}")
                        
                except Exception as e:
                    print(f"❌ RSS error for {rss_url}: {str(e)}")
                    continue
                    
        except Exception as e:
            print(f"❌ YouTube RSS error: {str(e)}")
        
        return None
    
    def _fetch_via_youtube_search(self, username: str) -> Optional[Dict]:
        """
        Fetch data using YouTube search (public endpoint)
        """
        clean_username = username.replace('@', '').strip()
        
        try:
            # Use YouTube's public search endpoint
            search_url = f"https://www.youtube.com/results"
            params = {
                'search_query': clean_username,
                'sp': 'EgIQAg%253D%253D'  # Channel filter
            }
            
            print(f"🔍 YouTube Search: Looking for {clean_username}")
            response = self.session.get(search_url, params=params, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                # Extract channel data from search results
                import re
                
                # Look for channel renderer in search results
                channel_pattern = r'"channelRenderer":\{[^}]*?"title":\{"simpleText":"([^"]+)"[^}]*?"subscriberCountText":\{"simpleText":"([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?"'
                
                matches = re.findall(channel_pattern, html)
                for channel_name, sub_count in matches:
                    if clean_username.lower() in channel_name.lower() or channel_name.lower() in clean_username.lower():
                        count = self._parse_count(sub_count)
                        if count and count > 1000:
                            print(f"✅ SUCCESS: YouTube Search data for {clean_username}: {count:,} subscribers")
                            
                            return {
                                'username': channel_name,
                                'follower_count': count,
                                'following_count': 0,
                                'post_count': 0,
                                'platform': 'youtube',
                                'verified': True,
                                'engagement_rate': 0.05,
                                'source': 'youtube_search'
                            }
                
        except Exception as e:
            print(f"❌ YouTube Search error: {str(e)}")
        
        return None
    
    def _get_channel_stats_from_id(self, channel_id: str) -> Optional[Dict]:
        """
        Get channel statistics from channel ID
        """
        try:
            # Try to get channel page and extract subscriber count
            channel_url = f"https://www.youtube.com/channel/{channel_id}/about"
            response = self.session.get(channel_url, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # Extract subscriber count from about page
                import re
                patterns = [
                    r'"subscriberCountText":\{"simpleText":"([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?"',
                    r'([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?',
                ]
                
                for pattern in patterns:
                    matches = re.findall(pattern, html, re.IGNORECASE)
                    if matches:
                        for match in matches:
                            count = self._parse_count(match)
                            if count and count > 1000:
                                return {
                                    'follower_count': count,
                                    'following_count': 0,
                                    'post_count': 0,
                                    'platform': 'youtube',
                                    'verified': True,
                                    'engagement_rate': 0.05
                                }
        
        except Exception as e:
            print(f"❌ Channel stats error: {str(e)}")
        
        return None
    
    def _parse_count(self, count_str: str) -> Optional[int]:
        """
        Parse subscriber count string to integer
        """
        if not count_str:
            return None
            
        count_str = count_str.replace(',', '').replace(' ', '').strip().upper()
        
        try:
            if 'K' in count_str:
                return int(float(count_str.replace('K', '')) * 1000)
            elif 'M' in count_str:
                return int(float(count_str.replace('M', '')) * 1000000)
            elif 'B' in count_str:
                return int(float(count_str.replace('B', '')) * 1000000000)
            else:
                return int(float(count_str))
        except:
            return None

# Create global instance
youtube_api_fetcher = YouTubeAPIFetcher()
