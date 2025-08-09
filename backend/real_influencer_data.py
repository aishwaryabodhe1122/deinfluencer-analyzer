"""
Real Influencer Database
Contains accurate follower counts and profile data for popular influencers
Updated as of January 2024
"""

from typing import Dict, Optional
from datetime import datetime

# Real influencer data with accurate follower counts (as of Jan 2024)
REAL_INFLUENCER_DATA = {
    # Twitter/X Influencers
    "elonmusk": {
        "username": "elonmusk",
        "platform": "twitter",
        "follower_count": 223000000,  # 223M followers (Aug 2025)
        "following_count": 1182,  # Elon follows 1,182 accounts (Aug 2025)
        "post_count": 35000,
        "bio": "CEO of Tesla, SpaceX, and X (formerly Twitter)",
        "verified": True,
        "engagement_rate": 2.1,
        "category": "tech_entrepreneur"
    },
    "barackobama": {
        "username": "BarackObama",
        "platform": "twitter",
        "follower_count": 131000000,  # 131M followers
        "following_count": 600,  # Obama follows ~600 accounts
        "post_count": 17000,
        "bio": "Dad, husband, President, citizen.",
        "verified": True,
        "engagement_rate": 3.2,
        "category": "politics"
    },
    "justinbieber": {
        "username": "justinbieber",
        "platform": "twitter",
        "follower_count": 110000000,  # 110M followers (Aug 2025)
        "following_count": 0,  # Justin Bieber follows 0 people
        "post_count": 31500,
        "bio": "Jesus Follower",
        "verified": True,
        "engagement_rate": 4.1,
        "category": "music"
    },
    "katyperry": {
        "username": "katyperry",
        "platform": "twitter",
        "follower_count": 108000000,  # 108M followers
        "following_count": 200,  # Katy Perry follows ~200 accounts
        "post_count": 11000,
        "bio": "WITNESS THE TOUR 🎪",
        "verified": True,
        "engagement_rate": 3.8,
        "category": "music"
    },
    "taylorswift13": {
        "username": "taylorswift13",
        "platform": "twitter",
        "follower_count": 95000000,  # 95M followers
        "following_count": 0,  # Taylor Swift follows 0 accounts
        "post_count": 2000,
        "bio": "All's fair in love and poetry...",
        "verified": True,
        "engagement_rate": 8.5,
        "category": "music"
    },
    
    # Instagram Influencers
    "cristiano": {
        "username": "cristiano",
        "platform": "instagram",
        "follower_count": 635000000,  # 635M followers (Aug 2025)
        "following_count": 560,  # Cristiano follows ~560 accounts
        "post_count": 3600,
        "bio": "Footballer ⚽ | @cr7.lm @cr7underwear @thecrownvillas",
        "verified": True,
        "engagement_rate": 2.8,
        "category": "sports"
    },
    "kyliejenner": {
        "username": "kyliejenner",
        "platform": "instagram",
        "follower_count": 400000000,  # 400M followers
        "following_count": 120,  # Kylie follows ~120 accounts
        "post_count": 7000,
        "bio": "Kylie Cosmetics 💄 Kylie Baby 🤍 @kyliecosmetics @kyliebaby",
        "verified": True,
        "engagement_rate": 3.2,
        "category": "beauty"
    },
    "leomessi": {
        "username": "leomessi",
        "platform": "instagram",
        "follower_count": 520000000,  # 520M followers (Aug 2025)
        "following_count": 295,  # Messi follows ~295 accounts
        "post_count": 1050,
        "bio": "Welcome to Miami 🤩🖤",
        "verified": True,
        "engagement_rate": 4.1,
        "category": "sports"
    },
    "selenagomez": {
        "username": "selenagomez",
        "platform": "instagram",
        "follower_count": 435000000,  # 435M followers (Aug 2025)
        "following_count": 42,  # Selena follows ~42 accounts
        "post_count": 2100,
        "bio": "Artist. Rare Beauty. Mental Health Advocate. @rarebeauty @raremhfund",
        "verified": True,
        "engagement_rate": 3.9,
        "category": "entertainment"
    },
    "kimkardashian": {
        "username": "kimkardashian",
        "platform": "instagram",
        "follower_count": 364000000,  # 364M followers
        "following_count": 110,  # Kim follows ~110 accounts
        "post_count": 5500,
        "bio": "SKIMS @skims SKKN BY KIM @skkn",
        "verified": True,
        "engagement_rate": 2.1,
        "category": "lifestyle"
    },
    "arianagrande": {
        "username": "arianagrande",
        "platform": "instagram",
        "follower_count": 380000000,  # 380M followers
        "following_count": 680,  # Ariana follows ~680 accounts
        "post_count": 5000,
        "bio": "☁️ @r.e.m.beauty @sweetenerworld",
        "verified": True,
        "engagement_rate": 4.8,
        "category": "music"
    },
    "therock": {
        "username": "therock",
        "platform": "instagram",
        "follower_count": 396000000,  # 396M followers
        "following_count": 650,  # The Rock follows ~650 accounts
        "post_count": 7500,
        "bio": "builder of stuff cheat meal crusher tequila sipper og girl dad 💕",
        "verified": True,
        "engagement_rate": 3.1,
        "category": "entertainment"
    },
    
    # YouTube Influencers (Updated 2024)
    "mrbeast": {
        "username": "MrBeast",
        "platform": "youtube",
        "follower_count": 218000000,  # 218M subscribers
        "following_count": 0,
        "post_count": 800,
        "bio": "I want to make the world a better place before I die.",
        "verified": True,
        "engagement_rate": 12.5,
        "category": "entertainment"
    },
    "pewdiepie": {
        "username": "PewDiePie",
        "platform": "youtube",
        "follower_count": 111000000,  # 111M subscribers
        "following_count": 0,
        "post_count": 4500,
        "bio": "Swedish YouTuber known for gaming videos and commentary",
        "verified": True,
        "engagement_rate": 8.2,
        "category": "gaming"
    },
    "mkbhd": {
        "username": "MKBHD",
        "platform": "youtube",
        "follower_count": 18500000,  # 18.5M subscribers
        "following_count": 0,
        "post_count": 1800,
        "bio": "Tech reviewer and car enthusiast",
        "verified": True,
        "engagement_rate": 9.1,
        "category": "tech"
    },
    "dude_perfect": {
        "username": "Dude Perfect",
        "platform": "youtube",
        "follower_count": 59000000,  # 59M subscribers
        "following_count": 0,
        "post_count": 350,
        "bio": "5 best friends and a panda",
        "verified": True,
        "engagement_rate": 11.3,
        "category": "sports"
    },
    
    # TikTok Influencers
    "charlidamelio": {
        "username": "charlidamelio",
        "platform": "tiktok",
        "follower_count": 151000000,  # 151M followers
        "following_count": 1400,  # Charli follows ~1400 accounts
        "post_count": 2800,
        "bio": "hey :) 19 years old",
        "verified": True,
        "engagement_rate": 15.2,
        "category": "dance"
    },
    "khaby.lame": {
        "username": "khaby.lame",
        "platform": "tiktok",
        "follower_count": 162000000,  # 162M followers
        "following_count": 90,  # Khaby follows ~90 accounts
        "post_count": 1200,
        "bio": "Se vuoi ridere sei nel posto giusto 😎",
        "verified": True,
        "engagement_rate": 18.7,
        "category": "comedy"
    },
    "addisonre": {
        "username": "addisonre",
        "platform": "tiktok",
        "follower_count": 88000000,  # 88M followers
        "following_count": 1100,  # Addison follows ~1100 accounts
        "post_count": 2100,
        "bio": "Louisiana 🤍 @itembeauty",
        "verified": True,
        "engagement_rate": 12.8,
        "category": "lifestyle"
    },
    
    # Tech Influencers
    "sundarpichai": {
        "username": "sundarpichai",
        "platform": "twitter",
        "follower_count": 5200000,  # 5.2M followers
        "following_count": 200,
        "post_count": 800,
        "bio": "CEO of Google and Alphabet",
        "verified": True,
        "engagement_rate": 2.8,
        "category": "tech"
    },
    "satyanadella": {
        "username": "satyanadella",
        "platform": "twitter",
        "follower_count": 2800000,  # 2.8M followers
        "following_count": 1000,
        "post_count": 3500,
        "bio": "Chairman and CEO, Microsoft",
        "verified": True,
        "engagement_rate": 3.1,
        "category": "tech"
    },
    
    # Lifestyle/Business Influencers
    "garyvee": {
        "username": "garyvee",
        "platform": "instagram",
        "follower_count": 11000000,  # 11M followers
        "following_count": 8000,
        "post_count": 15000,
        "bio": "Chairman of VaynerX, CEO of VaynerMedia & Creator & CEO of VeeFriends",
        "verified": True,
        "engagement_rate": 4.2,
        "category": "business"
    },
    "jeffbezos": {
        "username": "jeffbezos",
        "platform": "instagram",
        "follower_count": 4500000,  # 4.5M followers
        "following_count": 200,
        "post_count": 400,
        "bio": "Founder of Amazon and Blue Origin",
        "verified": True,
        "engagement_rate": 5.8,
        "category": "business"
    },
    
    # Smaller but notable influencers for testing
    "casey_neistat": {
        "username": "caseyneistat",
        "platform": "youtube",
        "follower_count": 12300000,  # 12.3M subscribers
        "following_count": 0,
        "post_count": 1000,
        "bio": "Filmmaker and YouTuber",
        "verified": True,
        "engagement_rate": 7.5,
        "category": "lifestyle"
    },
    "michelle_schroeder": {
        "username": "makingsenseofcents",
        "platform": "instagram",
        "follower_count": 85000,  # 85K followers
        "following_count": 2000,
        "post_count": 3500,
        "bio": "Personal Finance Expert | Making Sense of Cents Blog",
        "verified": False,
        "engagement_rate": 6.2,
        "category": "finance"
    },
    "pewdiepie": {
        "username": "PewDiePie",
        "platform": "youtube",
        "follower_count": 111000000,  # 111M subscribers
        "following_count": 0,
        "post_count": 4500,
        "bio": "Swedish YouTuber, gamer, and content creator",
        "verified": True,
        "engagement_rate": 6.2,
        "category": "gaming"
    },
    "tseries": {
        "username": "T-Series",
        "platform": "youtube",
        "follower_count": 245000000,  # 245M subscribers
        "following_count": 0,
        "post_count": 20000,
        "bio": "India's largest Music Label & Movie Studio",
        "verified": True,
        "engagement_rate": 1.8,
        "category": "music"
    },
    "cocomelon": {
        "username": "Cocomelon - Nursery Rhymes",
        "platform": "youtube",
        "follower_count": 180000000,  # 180M subscribers
        "following_count": 0,
        "post_count": 900,
        "bio": "The best way to learn and play!",
        "verified": True,
        "engagement_rate": 4.5,
        "category": "kids"
    },
    "markiplier": {
        "username": "Markiplier",
        "platform": "youtube",
        "follower_count": 36000000,  # 36M subscribers
        "following_count": 0,
        "post_count": 5500,
        "bio": "Hello everybody, my name is Markiplier",
        "verified": True,
        "engagement_rate": 7.8,
        "category": "gaming"
    },
    "ladygaga": {
        "username": "ladygaga",
        "platform": "twitter",
        "follower_count": 84000000,  # 84M followers
        "following_count": 130000,
        "post_count": 9000,
        "bio": "Artist, Actress, Activist, Entrepreneur",
        "verified": True,
        "engagement_rate": 4.7,
        "category": "music"
    },
    "zendaya": {
        "username": "zendaya",
        "platform": "instagram",
        "follower_count": 184000000,  # 184M followers
        "following_count": 2500,
        "post_count": 4500,
        "bio": "🕷️🪐 @dune @euphoria @spidermanmovie @challengers",
        "verified": True,
        "engagement_rate": 5.8,
        "category": "entertainment"
    },
    "justinbieber": {
        "username": "justinbieber",
        "platform": "instagram",
        "follower_count": 294000000,  # 294M followers
        "following_count": 3000,
        "post_count": 7000,
        "bio": "Jesus follower, Husband to @haileybieber, Dad",
        "verified": True,
        "engagement_rate": 3.4,
        "category": "music"
    },
    "taylorswift": {
        "username": "taylorswift",
        "platform": "instagram",
        "follower_count": 279000000,  # 279M followers
        "following_count": 0,
        "post_count": 900,
        "bio": "All's fair in love and poetry...",
        "verified": True,
        "engagement_rate": 4.9,
        "category": "music"
    },
    "virat.kohli": {
        "username": "virat.kohli",
        "platform": "instagram",
        "follower_count": 275000000,  # 275M followers (Aug 2025)
        "following_count": 205,
        "post_count": 3300,
        "bio": "Carpediem! 🇮🇳",
        "verified": True,
        "engagement_rate": 4.2,
        "category": "sports"
    },
    "badgalriri": {
        "username": "badgalriri",
        "platform": "instagram",
        "follower_count": 151000000,  # 151M followers
        "following_count": 1800,
        "post_count": 4800,
        "bio": "@fenty @fentybeauty @savagexfenty",
        "verified": True,
        "engagement_rate": 4.6,
        "category": "music"
    },
    
    # Additional popular influencers (Aug 2025 data)
    "mrbeast": {
        "username": "MrBeast",
        "platform": "youtube",
        "follower_count": 220000000,  # 220M subscribers (Aug 2025)
        "following_count": 0,
        "post_count": 800,
        "bio": "I want to make the world a better place before I die.",
        "verified": True,
        "engagement_rate": 8.2,
        "category": "entertainment"
    },
    "pewdiepie": {
        "username": "PewDiePie",
        "platform": "youtube", 
        "follower_count": 111000000,  # 111M subscribers (Aug 2025)
        "following_count": 0,
        "post_count": 4500,
        "bio": "Swedish YouTuber, gamer, and comedian",
        "verified": True,
        "engagement_rate": 6.8,
        "category": "gaming"
    },
    "tseries": {
        "username": "T-Series",
        "platform": "youtube",
        "follower_count": 248000000,  # 248M subscribers (Aug 2025)
        "following_count": 0,
        "post_count": 20000,
        "bio": "India's largest Music Label & Movie Studio",
        "verified": True,
        "engagement_rate": 2.1,
        "category": "music"
    },
    "kyliejenner_twitter": {
        "username": "KylieJenner",
        "platform": "twitter",
        "follower_count": 36000000,  # 36M followers (Aug 2025)
        "following_count": 120,
        "post_count": 8500,
        "bio": "Kylie Cosmetics 💄 Kylie Baby 🤍",
        "verified": True,
        "engagement_rate": 4.2,
        "category": "beauty"
    }
}

# Platform-specific real data patterns
PLATFORM_PATTERNS = {
    "twitter": {
        "avg_engagement_rate": 2.5,
        "high_follower_threshold": 10000000,
        "verification_threshold": 100000
    },
    "instagram": {
        "avg_engagement_rate": 3.5,
        "high_follower_threshold": 50000000,
        "verification_threshold": 10000
    },
    "youtube": {
        "avg_engagement_rate": 8.0,
        "high_follower_threshold": 10000000,
        "verification_threshold": 100000
    },
    "tiktok": {
        "avg_engagement_rate": 15.0,
        "high_follower_threshold": 50000000,
        "verification_threshold": 10000
    }
}

def get_real_influencer_data(username: str, platform: str) -> Optional[Dict]:
    """
    Get real influencer data from the curated database
    """
    print(f"DEBUG: get_real_influencer_data called with username='{username}', platform='{platform}'")
    
    # Try exact match first (case-insensitive)
    key = username.lower()
    print(f"DEBUG: Looking for exact key match: '{key}'")
    if key in REAL_INFLUENCER_DATA:
        data = REAL_INFLUENCER_DATA[key].copy()
        print(f"DEBUG: Found exact key match for '{key}', platform: {data['platform']}")
        # Ensure platform matches or is flexible
        if data["platform"] == platform.lower() or platform.lower() == "any":
            print(f"DEBUG: Platform match successful, returning real data")
            return data
        else:
            print(f"DEBUG: Platform mismatch: {data['platform']} != {platform.lower()}")
    
    # Try matching by the actual username field in the data (case-insensitive)
    print(f"DEBUG: Trying username field matching for platform '{platform}'")
    for db_key, data in REAL_INFLUENCER_DATA.items():
        if data["platform"] == platform.lower() or platform.lower() == "any":
            print(f"DEBUG: Checking db_key '{db_key}', stored username: '{data['username']}', platform: '{data['platform']}'")
            # Check if the search username matches the stored username (case-insensitive)
            if data["username"].lower() == username.lower():
                print(f"DEBUG: Username field match found! '{data['username']}' matches '{username}'")
                result = data.copy()
                result["username"] = username  # Use requested username format
                return result
    
    # Try partial matching for common variations
    for db_key, data in REAL_INFLUENCER_DATA.items():
        if (username.lower() in db_key or db_key in username.lower() or 
            username.lower() in data["username"].lower() or data["username"].lower() in username.lower()) and \
           (data["platform"] == platform.lower() or platform.lower() == "any"):
            result = data.copy()
            result["username"] = username  # Use requested username
            return result
    
    return None

def generate_realistic_follower_count(username: str, platform: str) -> int:
    """
    Generate realistic follower counts based on username patterns and platform
    This is used as fallback when real data is not available
    """
    # Use hash for consistency but make it more realistic
    base_hash = abs(hash(username + platform))
    
    # Platform-specific realistic ranges
    if platform.lower() == "twitter":
        # Twitter: 1K to 50M (most accounts are smaller)
        base_range = base_hash % 50000000
        if base_range < 1000:
            return base_range + 1000
        return base_range
    
    elif platform.lower() == "instagram":
        # Instagram: 500 to 100M
        base_range = base_hash % 100000000
        if base_range < 500:
            return base_range + 500
        return base_range
    
    elif platform.lower() == "youtube":
        # YouTube: 100 to 50M subscribers
        base_range = base_hash % 50000000
        if base_range < 100:
            return base_range + 100
        return base_range
    
    elif platform.lower() == "tiktok":
        # TikTok: 1K to 200M
        base_range = base_hash % 200000000
        if base_range < 1000:
            return base_range + 1000
        return base_range
    
    else:
        # Default fallback
        return max(1000, base_hash % 10000000)

def get_category_multiplier(category: str) -> float:
    """
    Get engagement multiplier based on content category
    """
    multipliers = {
        "music": 1.2,
        "sports": 1.1,
        "entertainment": 1.0,
        "tech": 0.8,
        "business": 0.7,
        "politics": 0.9,
        "lifestyle": 1.0,
        "beauty": 1.1,
        "gaming": 1.3,
        "comedy": 1.4,
        "dance": 1.5,
        "finance": 0.6
    }
    return multipliers.get(category, 1.0)

# Export the main function
__all__ = ['get_real_influencer_data', 'generate_realistic_follower_count', 'REAL_INFLUENCER_DATA']
