"""
Quick Data Update Script
Use this to add/update current live data for any influencer
"""

import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from current_live_data import current_live_data_fetcher

def update_youtube_data(username, subscriber_count, video_count=None):
    """
    Update YouTube data for a specific channel
    """
    data = {
        'username': username,
        'follower_count': int(subscriber_count),
        'following_count': 0,
        'post_count': int(video_count) if video_count else 0,
        'platform': 'youtube',
        'verified': True,
        'engagement_rate': 0.06,
    }
    
    current_live_data_fetcher.add_current_data(username, 'youtube', data)
    print(f"✅ Updated {username}: {subscriber_count:,} subscribers")

def update_instagram_data(username, follower_count, post_count=None):
    """
    Update Instagram data for a specific account
    """
    data = {
        'username': username,
        'follower_count': int(follower_count),
        'following_count': 0,
        'post_count': int(post_count) if post_count else 0,
        'platform': 'instagram',
        'verified': True,
        'engagement_rate': 0.04,
    }
    
    current_live_data_fetcher.add_current_data(username, 'instagram', data)
    print(f"✅ Updated {username}: {follower_count:,} followers")

def update_twitter_data(username, follower_count, following_count=None):
    """
    Update Twitter data for a specific account
    """
    data = {
        'username': username,
        'follower_count': int(follower_count),
        'following_count': int(following_count) if following_count else 0,
        'post_count': 0,
        'platform': 'twitter',
        'verified': True,
        'engagement_rate': 0.02,
    }
    
    current_live_data_fetcher.add_current_data(username, 'twitter', data)
    print(f"✅ Updated {username}: {follower_count:,} followers")

if __name__ == "__main__":
    print("🔧 Data Update Script")
    print("Usage examples:")
    print("  update_youtube_data('CarryMinati', 45100000, 205)")
    print("  update_instagram_data('therock', 396000000, 7500)")
    print("  update_twitter_data('elonmusk', 223000000, 1182)")
    print()
    
    # Example updates - you can modify these
    if len(sys.argv) > 1:
        if sys.argv[1] == "carrryminati":
            update_youtube_data('CarryMinati', 45100000, 205)
        elif sys.argv[1] == "bbkivines":
            # Update with actual current count - please provide the correct number
            update_youtube_data('BBKiVines', 1850000, 150)  # Update this with actual count
        else:
            print(f"Unknown channel: {sys.argv[1]}")
    else:
        print("Available overrides:")
        overrides = current_live_data_fetcher.list_available_overrides()
        for platform, channels in overrides.items():
            print(f"  {platform}: {', '.join(channels)}")
