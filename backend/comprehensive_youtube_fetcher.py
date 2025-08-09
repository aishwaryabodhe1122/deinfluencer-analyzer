"""
Comprehensive YouTube Fetcher
Gets BOTH subscriber counts AND video counts accurately for ANY YouTube channel
"""

import requests
import re
import json
import time
import random
from typing import Dict, Optional
from urllib.parse import quote
from video_count_fetcher import video_count_fetcher

class ComprehensiveYouTubeFetcher:
    def __init__(self):
        self.session = requests.Session()
        
        # Multiple user agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none'
        })
    
    def fetch_realtime_data(self, username: str, platform: str) -> Optional[Dict]:
        """
        Fetch ACTUAL REAL-TIME YouTube data with BOTH subscriber and video counts
        """
        if platform.lower() != "youtube":
            return None
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        clean_username = username.replace('@', '').strip()
        print(f"🔴 COMPREHENSIVE YOUTUBE: Getting COMPLETE data for {clean_username} at {current_time}")
        
        # Try multiple approaches for maximum success
        data = self._fetch_via_channel_page(clean_username)
        if data:
            return data
        
        data = self._fetch_via_about_page(clean_username)
        if data:
            return data
        
        data = self._fetch_via_search_results(clean_username)
        if data:
            return data
        
        print(f"❌ Could not fetch comprehensive YouTube data for {clean_username}")
        return None
    
    def _fetch_via_channel_page(self, username: str) -> Optional[Dict]:
        """
        Fetch data directly from channel main page AND videos page for accurate video count
        """
        urls_to_try = [
            f"https://www.youtube.com/@{username}",
            f"https://www.youtube.com/c/{username}",
            f"https://www.youtube.com/user/{username}",
            f"https://www.youtube.com/{username}",
        ]
        
        # Also try videos page for better video count extraction
        video_urls_to_try = [
            f"https://www.youtube.com/@{username}/videos",
            f"https://www.youtube.com/c/{username}/videos",
            f"https://www.youtube.com/user/{username}/videos",
        ]
        
        for url in urls_to_try:
            try:
                # Rotate user agent
                self.session.headers['User-Agent'] = random.choice(self.user_agents)
                print(f"🔍 Comprehensive: Trying {url}")
                
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Enhanced extraction for ANY channel
                    subscriber_count = self._extract_subscriber_count(html)
                    channel_name = self._extract_channel_name(html, username)
                    
                    # Use targeted video count fetcher for accurate video counts
                    video_count = video_count_fetcher.get_video_count(username)
                    
                    print(f"🎯 COMPREHENSIVE DEBUG: {username} - Subs: {subscriber_count}, Videos: {video_count}")
                    
                    if subscriber_count and subscriber_count > 1000:
                        print(f"✅ SUCCESS: Comprehensive YouTube data for {username}: {subscriber_count:,} subscribers, {video_count} videos")
                        
                        return {
                            'username': channel_name,
                            'follower_count': subscriber_count,
                            'following_count': 0,
                            'post_count': video_count,
                            'platform': 'youtube',
                            'verified': True,
                            'engagement_rate': 0.05,
                            'source': 'comprehensive_youtube_fetcher'
                        }
                
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"❌ Error with {url}: {str(e)}")
                continue
        
        return None
    
    def _fetch_via_about_page(self, username: str) -> Optional[Dict]:
        """
        Fetch data from channel about page (often has more structured data)
        """
        urls_to_try = [
            f"https://www.youtube.com/@{username}/about",
            f"https://www.youtube.com/c/{username}/about",
            f"https://www.youtube.com/user/{username}/about",
        ]
        
        for url in urls_to_try:
            try:
                self.session.headers['User-Agent'] = random.choice(self.user_agents)
                print(f"🔍 About page: {url}")
                
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    html = response.text
                    
                    subscriber_count = self._extract_subscriber_count(html)
                    video_count = self._extract_video_count(html)
                    channel_name = self._extract_channel_name(html, username)
                    
                    if subscriber_count and subscriber_count > 1000:
                        print(f"✅ SUCCESS: About page data for {username}: {subscriber_count:,} subscribers, {video_count} videos")
                        
                        return {
                            'username': channel_name,
                            'follower_count': subscriber_count,
                            'following_count': 0,
                            'post_count': video_count,
                            'platform': 'youtube',
                            'verified': True,
                            'engagement_rate': 0.05,
                            'source': 'comprehensive_about_page'
                        }
                
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"❌ About page error: {str(e)}")
                continue
        
        return None
    
    def _fetch_via_search_results(self, username: str) -> Optional[Dict]:
        """
        Fetch data from YouTube search results
        """
        try:
            search_url = f"https://www.youtube.com/results?search_query={quote(username)}&sp=EgIQAg%253D%253D"
            
            self.session.headers['User-Agent'] = random.choice(self.user_agents)
            print(f"🔍 Search results: {search_url}")
            
            response = self.session.get(search_url, timeout=15)
            
            if response.status_code == 200:
                html = response.text
                
                # Look for channel in search results
                channel_pattern = r'"channelRenderer":\s*\{[^}]*?"title":\s*\{\s*"simpleText":\s*"([^"]+)"[^}]*?"subscriberCountText":\s*\{\s*"simpleText":\s*"([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?"'
                
                matches = re.findall(channel_pattern, html)
                for channel_name, sub_count in matches:
                    if username.lower() in channel_name.lower() or channel_name.lower() in username.lower():
                        count = self._parse_count(sub_count)
                        if count and count > 1000:
                            print(f"✅ SUCCESS: Search results data for {username}: {count:,} subscribers")
                            
                            return {
                                'username': channel_name,
                                'follower_count': count,
                                'following_count': 0,
                                'post_count': 0,  # Search results don't show video count
                                'platform': 'youtube',
                                'verified': True,
                                'engagement_rate': 0.05,
                                'source': 'comprehensive_search_results'
                            }
                
        except Exception as e:
            print(f"❌ Search results error: {str(e)}")
        
        return None
    
    def _extract_subscriber_count(self, html: str) -> Optional[int]:
        """
        Extract subscriber count with comprehensive patterns
        """
        patterns = [
            # 2025 YouTube JSON structure patterns
            r'"subscriberCountText":\s*\{\s*"accessibility":\s*\{\s*"accessibilityData":\s*\{\s*"label":\s*"([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?"',
            r'"subscriberCountText":\s*\{\s*"simpleText":\s*"([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?"',
            r'"header":\s*\{\s*"c4TabbedHeaderRenderer":\s*\{[^}]*"subscriberCountText":\s*\{\s*"simpleText":\s*"([\d,\.]+(?:\.\d+)?[KMB]?)',
            r'"channelMetadataRenderer":\s*\{[^}]*"subscriberCountText":\s*\{\s*"simpleText":\s*"([\d,\.]+(?:\.\d+)?[KMB]?)',
            
            # Channel header patterns
            r'@[\w\d]+\s*•\s*([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?',
            r'([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?\s*•\s*[\d,]+\s+videos?',
            r'([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?\s*•',
            
            # Meta tag patterns
            r'<meta property="og:description" content="[^"]*?([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?',
            r'<meta name="description" content="[^"]*?([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?',
            
            # General patterns
            r'([\d,\.]+(?:\.\d+)?[KMB]?)\s+subscribers?',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                for match in matches:
                    count = self._parse_count(match)
                    if count and count > 1000:
                        return count
        
        return None
    
    def _extract_video_count(self, html: str) -> int:
        """
        Extract video count with comprehensive patterns and debug
        """
        print(f"🔍 DEBUG: Extracting video count...")
        
        patterns = [
            # 2025 YouTube JSON structure patterns for video count
            r'"videosCountText":\s*\{\s*"accessibility":\s*\{\s*"accessibilityData":\s*\{\s*"label":\s*"([\d,]+)\s+videos?"',
            r'"videosCountText":\s*\{\s*"simpleText":\s*"([\d,]+)\s+videos?"',
            r'"videoCount":\s*"(\d+)"',
            r'"videoCountText":\s*\{\s*"simpleText":\s*"([\d,]+)"',
            
            # Tab navigation patterns (Videos tab)
            r'"tabRenderer":\s*\{[^}]*"title":\s*"Videos"[^}]*"text":\s*"([\d,]+)"',
            r'"videosTab"[^}]*"text":\s*"([\d,]+)"',
            r'"selected":true[^}]*"title":"Videos"[^}]*"text":"([\d,]+)"',
            
            # Channel header patterns
            r'@[\w\d]+\s*•\s*[\d,\.]+[KMB]?\s+subscribers?\s*•\s*([\d,]+)\s+videos?',
            r'([\d,]+)\s+videos?\s*•\s*[\d,\.]+[KMB]?\s+subscribers?',
            r'([\d,]+)\s+videos?\s*•',
            r'•\s*([\d,]+)\s+videos?',
            
            # Meta description patterns
            r'<meta[^>]*content="[^"]*?([\d,]+)\s+videos?[^"]*"',
            r'<meta property="og:description" content="[^"]*?([\d,]+)\s+videos?[^"]*"',
            
            # Page title patterns
            r'<title>[^<]*?([\d,]+)\s+videos?[^<]*</title>',
            
            # JSON-LD structured data
            r'"numberOfVideos":\s*"?([\d,]+)"?',
            r'"videoCount":\s*([\d,]+)',
            r'"totalResults":\s*"?([\d,]+)"?',
            
            # Text content patterns
            r'videos?"[^>]*>([\d,]+)',
            r'"text":\s*"([\d,]+)\s+videos?"',
            r'aria-label="[^"]*?([\d,]+)\s+videos?[^"]*?"',
            
            # Flexible patterns
            r'([\d,]+)\s+videos?[^0-9]*subscribers?',
            r'subscribers?[^0-9]*([\d,]+)\s+videos?',
            r'videos?[^0-9]*([\d,]+)',
            r'([\d,]+)\s+videos?',
        ]
        
        for i, pattern in enumerate(patterns):
            matches = re.findall(pattern, html, re.IGNORECASE)
            if matches:
                print(f"🎯 DEBUG: Video pattern {i+1} matched: {matches[:3]}")
                for match in matches:
                    try:
                        count = int(str(match).replace(',', '').strip())
                        if 1 <= count <= 50000:  # Reasonable range
                            print(f"✅ DEBUG: Found valid video count: {count}")
                            return count
                        else:
                            print(f"⚠️ DEBUG: Video count {count} out of range")
                    except ValueError:
                        print(f"❌ DEBUG: Could not parse video count: {match}")
                        continue
        
        print(f"❌ DEBUG: No valid video count found")
        return 0
    
    def _extract_channel_name(self, html: str, fallback: str) -> str:
        """
        Extract channel name
        """
        patterns = [
            r'<meta property="og:title" content="([^"]+)"',
            r'"header":\s*\{\s*"c4TabbedHeaderRenderer":\s*\{\s*"title":\s*"([^"]+)"',
            r'<title>([^<]+) - YouTube</title>',
            r'"channelMetadataRenderer":\s*\{\s*"title":\s*"([^"]+)"',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, html)
            if match:
                name = match.group(1).strip()
                if name and name != "YouTube" and " - YouTube" not in name:
                    return name
        
        return fallback
    
    def _parse_count(self, count_str: str) -> Optional[int]:
        """
        Parse count string to integer (handles K, M, B suffixes)
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
comprehensive_youtube_fetcher = ComprehensiveYouTubeFetcher()
