"""
Targeted Video Count Fetcher
Specifically designed to get accurate video counts for ANY YouTube channel
"""

import requests
import re
import time
import random
from typing import Optional
from urllib.parse import quote

class VideoCountFetcher:
    def __init__(self):
        self.session = requests.Session()
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache'
        })
    
    def get_video_count(self, username: str) -> int:
        """
        Get accurate video count for ANY YouTube channel
        """
        clean_username = username.replace('@', '').strip()
        print(f"🎬 VIDEO COUNT: Getting video count for {clean_username}")
        
        # Try videos page first (most reliable for video count)
        video_count = self._fetch_from_videos_page(clean_username)
        if video_count > 0:
            return video_count
        
        # Try main channel page
        video_count = self._fetch_from_main_page(clean_username)
        if video_count > 0:
            return video_count
        
        # Try about page
        video_count = self._fetch_from_about_page(clean_username)
        if video_count > 0:
            return video_count
        
        print(f"❌ Could not fetch video count for {clean_username}")
        return 0
    
    def _fetch_from_videos_page(self, username: str) -> int:
        """
        Fetch video count from /videos page (most reliable)
        """
        video_urls = [
            f"https://www.youtube.com/@{username}/videos",
            f"https://www.youtube.com/c/{username}/videos",
            f"https://www.youtube.com/user/{username}/videos",
        ]
        
        for url in video_urls:
            try:
                self.session.headers['User-Agent'] = random.choice(self.user_agents)
                print(f"🎬 Trying videos page: {url}")
                
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Enhanced patterns for videos page
                    video_patterns = [
                        # Videos page specific patterns
                        r'"gridVideoRenderer"',  # Count video renderers
                        r'"videoRenderer"',      # Count video renderers
                        r'"richItemRenderer"',   # Count video items
                        
                        # Text patterns on videos page
                        r'([\d,]+)\s+videos?\s+•',
                        r'•\s*([\d,]+)\s+videos?',
                        r'"text":\s*"([\d,]+)\s+videos?"',
                        r'"label":\s*"([\d,]+)\s+videos?"',
                        
                        # Tab patterns
                        r'"selected":true[^}]*"text":"([\d,]+)"',
                        r'"tabRenderer"[^}]*"title":"Videos"[^}]*"text":"([\d,]+)"',
                    ]
                    
                    # Method 1: Count video renderers (most accurate)
                    video_renderers = len(re.findall(r'"gridVideoRenderer"|"videoRenderer"', html))
                    if video_renderers > 0:
                        # This gives us videos on current page, but we need total
                        # Look for pagination or total count
                        total_pattern = r'"totalResults":\s*"?(\d+)"?'
                        total_match = re.search(total_pattern, html)
                        if total_match:
                            total_count = int(total_match.group(1))
                            if 1 <= total_count <= 50000:
                                print(f"✅ VIDEO COUNT: Found total from pagination: {total_count}")
                                return total_count
                    
                    # Method 2: Extract from text patterns
                    for pattern in video_patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        if matches:
                            for match in matches:
                                try:
                                    if isinstance(match, str) and not match.isdigit():
                                        continue
                                    count = int(str(match).replace(',', '').strip())
                                    if 1 <= count <= 50000:
                                        print(f"✅ VIDEO COUNT: Found from pattern: {count}")
                                        return count
                                except:
                                    continue
                
                time.sleep(random.uniform(0.5, 1.0))
                
            except Exception as e:
                print(f"❌ Videos page error: {str(e)}")
                continue
        
        return 0
    
    def _fetch_from_main_page(self, username: str) -> int:
        """
        Fetch video count from main channel page
        """
        main_urls = [
            f"https://www.youtube.com/@{username}",
            f"https://www.youtube.com/c/{username}",
            f"https://www.youtube.com/user/{username}",
        ]
        
        for url in main_urls:
            try:
                self.session.headers['User-Agent'] = random.choice(self.user_agents)
                print(f"🎬 Trying main page: {url}")
                
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # Look for video count in channel header
                    patterns = [
                        r'([\d,]+)\s+videos?\s*•\s*[\d,\.]+[KMB]?\s+subscribers?',
                        r'@[\w\d]+\s*•\s*[\d,\.]+[KMB]?\s+subscribers?\s*•\s*([\d,]+)\s+videos?',
                        r'"videosCountText":\s*\{\s*"simpleText":\s*"([\d,]+)"',
                        r'"videoCount":\s*"(\d+)"',
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        if matches:
                            for match in matches:
                                try:
                                    count = int(str(match).replace(',', '').strip())
                                    if 1 <= count <= 50000:
                                        print(f"✅ VIDEO COUNT: Found from main page: {count}")
                                        return count
                                except:
                                    continue
                
                time.sleep(random.uniform(0.5, 1.0))
                
            except Exception as e:
                print(f"❌ Main page error: {str(e)}")
                continue
        
        return 0
    
    def _fetch_from_about_page(self, username: str) -> int:
        """
        Fetch video count from about page
        """
        about_urls = [
            f"https://www.youtube.com/@{username}/about",
            f"https://www.youtube.com/c/{username}/about",
            f"https://www.youtube.com/user/{username}/about",
        ]
        
        for url in about_urls:
            try:
                self.session.headers['User-Agent'] = random.choice(self.user_agents)
                print(f"🎬 Trying about page: {url}")
                
                response = self.session.get(url, timeout=15)
                
                if response.status_code == 200:
                    html = response.text
                    
                    # About page often has more structured data
                    patterns = [
                        r'"videoCount":\s*"(\d+)"',
                        r'"numberOfVideos":\s*"?(\d+)"?',
                        r'([\d,]+)\s+videos?',
                    ]
                    
                    for pattern in patterns:
                        matches = re.findall(pattern, html, re.IGNORECASE)
                        if matches:
                            for match in matches:
                                try:
                                    count = int(str(match).replace(',', '').strip())
                                    if 1 <= count <= 50000:
                                        print(f"✅ VIDEO COUNT: Found from about page: {count}")
                                        return count
                                except:
                                    continue
                
                time.sleep(random.uniform(0.5, 1.0))
                
            except Exception as e:
                print(f"❌ About page error: {str(e)}")
                continue
        
        return 0

# Create global instance
video_count_fetcher = VideoCountFetcher()
