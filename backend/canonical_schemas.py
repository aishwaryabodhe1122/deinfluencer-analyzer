"""
Canonical Schema Definitions for Multi-Platform Influencer Data
Normalizes all platform-specific data into unified schemas for downstream processing
"""

from typing import List, Dict, Optional, Union, Any
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
import uuid

class PlatformType(str, Enum):
    """Supported social media platforms"""
    INSTAGRAM = "instagram"
    YOUTUBE = "youtube"
    TWITTER = "twitter"
    TIKTOK = "tiktok"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"

class MediaType(str, Enum):
    """Supported media types across all platforms"""
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    CAROUSEL = "carousel"  # Multiple images/videos
    STORY = "story"        # Temporary content
    LIVE = "live"          # Live streaming
    REEL = "reel"          # Short-form video
    POLL = "poll"          # Interactive polls

class ContentCategory(str, Enum):
    """Content classification categories"""
    ORGANIC = "organic"
    SPONSORED = "sponsored"
    PARTNERSHIP = "partnership"
    AFFILIATE = "affiliate"
    PROMOTIONAL = "promotional"
    EDUCATIONAL = "educational"
    ENTERTAINMENT = "entertainment"
    PERSONAL = "personal"
    NEWS = "news"
    UNKNOWN = "unknown"

class EngagementType(str, Enum):
    """Types of engagement across platforms"""
    LIKE = "like"
    COMMENT = "comment"
    SHARE = "share"
    RETWEET = "retweet"
    REACTION = "reaction"  # Facebook reactions
    VIEW = "view"
    SAVE = "save"
    CLICK = "click"
    FOLLOW = "follow"
    MENTION = "mention"
    TAG = "tag"

class VerificationStatus(str, Enum):
    """Account verification status"""
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    BUSINESS = "business"
    CREATOR = "creator"
    GOVERNMENT = "government"
    UNKNOWN = "unknown"

# ===== CANONICAL SCHEMAS =====

class CanonicalMediaItem(BaseModel):
    """Unified media item schema for all platforms"""
    media_id: str = Field(..., description="Unique identifier for the media item")
    media_type: MediaType = Field(..., description="Type of media content")
    url: Optional[str] = Field(None, description="Direct URL to media content")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail/preview URL")
    duration_seconds: Optional[float] = Field(None, description="Duration for video/audio content")
    width: Optional[int] = Field(None, description="Media width in pixels")
    height: Optional[int] = Field(None, description="Media height in pixels")
    file_size_bytes: Optional[int] = Field(None, description="File size in bytes")
    alt_text: Optional[str] = Field(None, description="Alternative text description")
    caption: Optional[str] = Field(None, description="Media-specific caption")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Platform-specific metadata")

class CanonicalEngagement(BaseModel):
    """Unified engagement data schema"""
    engagement_type: EngagementType = Field(..., description="Type of engagement")
    count: int = Field(..., description="Total count of this engagement type")
    rate: Optional[float] = Field(None, description="Engagement rate (count/followers)")
    recent_activity: Optional[List[Dict]] = Field(None, description="Recent engagement activity")
    growth_trend: Optional[str] = Field(None, description="Trend: increasing, decreasing, stable")
    authenticity_score: Optional[float] = Field(None, description="Authenticity score for this engagement type")

class CanonicalHashtag(BaseModel):
    """Unified hashtag schema"""
    tag: str = Field(..., description="Hashtag text without #")
    usage_count: Optional[int] = Field(None, description="How many times used by this influencer")
    trending_score: Optional[float] = Field(None, description="Trending popularity score")
    category: Optional[str] = Field(None, description="Hashtag category")
    relevance_score: Optional[float] = Field(None, description="Relevance to influencer's content")

class CanonicalMention(BaseModel):
    """Unified mention/tag schema"""
    username: str = Field(..., description="Mentioned user's username")
    display_name: Optional[str] = Field(None, description="Mentioned user's display name")
    platform_id: Optional[str] = Field(None, description="Platform-specific user ID")
    mention_type: str = Field(..., description="Type: mention, tag, collaboration")
    context: Optional[str] = Field(None, description="Context around the mention")

class CanonicalPost(BaseModel):
    """Unified post schema for all platforms and media types"""
    # Core Identifiers
    post_id: str = Field(..., description="Unique canonical post identifier")
    platform_post_id: str = Field(..., description="Original platform-specific post ID")
    platform: PlatformType = Field(..., description="Source platform")
    
    # Content
    content_text: Optional[str] = Field(None, description="Text content of the post")
    media_items: List[CanonicalMediaItem] = Field(default_factory=list, description="All media attachments")
    hashtags: List[CanonicalHashtag] = Field(default_factory=list, description="Hashtags used")
    mentions: List[CanonicalMention] = Field(default_factory=list, description="User mentions/tags")
    
    # Classification
    content_category: ContentCategory = Field(default=ContentCategory.UNKNOWN, description="Content classification")
    is_sponsored: bool = Field(default=False, description="Whether content is sponsored")
    sponsor_info: Optional[Dict[str, Any]] = Field(None, description="Sponsor/brand information")
    
    # Engagement Metrics
    engagements: List[CanonicalEngagement] = Field(default_factory=list, description="All engagement metrics")
    total_engagement: int = Field(default=0, description="Sum of all engagements")
    engagement_rate: Optional[float] = Field(None, description="Overall engagement rate")
    
    # Temporal Data
    created_at: datetime = Field(..., description="Post creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    published_at: Optional[datetime] = Field(None, description="Publication timestamp (if different)")
    
    # Location & Context
    location: Optional[Dict[str, Any]] = Field(None, description="Geographic location data")
    language: Optional[str] = Field(None, description="Content language code")
    audience_targeting: Optional[Dict[str, Any]] = Field(None, description="Audience targeting info")
    
    # Analytics & Insights
    reach: Optional[int] = Field(None, description="Total reach/impressions")
    impressions: Optional[int] = Field(None, description="Total impressions")
    click_through_rate: Optional[float] = Field(None, description="CTR for links")
    save_rate: Optional[float] = Field(None, description="Save/bookmark rate")
    
    # Quality Metrics
    authenticity_score: Optional[float] = Field(None, description="Post authenticity score")
    quality_score: Optional[float] = Field(None, description="Content quality score")
    spam_probability: Optional[float] = Field(None, description="Probability of being spam")
    
    # Platform-Specific Data
    platform_metadata: Dict[str, Any] = Field(default_factory=dict, description="Platform-specific fields")
    raw_data: Optional[Dict[str, Any]] = Field(None, description="Original raw platform data")

class CanonicalAudienceInsight(BaseModel):
    """Unified audience analytics schema"""
    demographic_breakdown: Dict[str, Any] = Field(default_factory=dict, description="Age, gender, location demographics")
    interest_categories: List[str] = Field(default_factory=list, description="Audience interest categories")
    engagement_patterns: Dict[str, Any] = Field(default_factory=dict, description="When audience is most active")
    authenticity_metrics: Dict[str, Any] = Field(default_factory=dict, description="Fake vs real follower analysis")
    growth_analysis: Dict[str, Any] = Field(default_factory=dict, description="Follower growth patterns")

class CanonicalInfluencer(BaseModel):
    """Unified influencer profile schema for all platforms"""
    # Core Identifiers
    influencer_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique canonical influencer ID")
    platform_user_id: str = Field(..., description="Platform-specific user ID")
    platform: PlatformType = Field(..., description="Primary platform")
    cross_platform_ids: Dict[PlatformType, str] = Field(default_factory=dict, description="IDs across other platforms")
    
    # Profile Information
    username: str = Field(..., description="Platform username/handle")
    display_name: Optional[str] = Field(None, description="Display name")
    bio: Optional[str] = Field(None, description="Profile biography/description")
    profile_image_url: Optional[str] = Field(None, description="Profile picture URL")
    banner_image_url: Optional[str] = Field(None, description="Banner/cover image URL")
    
    # Verification & Status
    verification_status: VerificationStatus = Field(default=VerificationStatus.UNKNOWN, description="Account verification")
    account_type: Optional[str] = Field(None, description="Personal, business, creator, etc.")
    account_created_at: Optional[datetime] = Field(None, description="Account creation date")
    
    # Follower Metrics
    follower_count: int = Field(default=0, description="Total followers")
    following_count: int = Field(default=0, description="Total following")
    post_count: int = Field(default=0, description="Total posts")
    
    # Engagement Metrics
    average_engagement_rate: Optional[float] = Field(None, description="Average engagement rate")
    total_engagements: Optional[int] = Field(None, description="Total lifetime engagements")
    engagement_breakdown: List[CanonicalEngagement] = Field(default_factory=list, description="Engagement by type")
    
    # Content Analytics
    posting_frequency: Optional[float] = Field(None, description="Posts per day/week")
    content_categories: List[ContentCategory] = Field(default_factory=list, description="Primary content categories")
    sponsored_content_ratio: Optional[float] = Field(None, description="Ratio of sponsored content")
    
    # Audience Insights
    audience_insights: Optional[CanonicalAudienceInsight] = Field(None, description="Audience demographics and behavior")
    
    # Authenticity Metrics
    authenticity_score: Optional[float] = Field(None, description="Overall authenticity score")
    bot_probability: Optional[float] = Field(None, description="Probability of being a bot account")
    fake_follower_percentage: Optional[float] = Field(None, description="Estimated fake follower percentage")
    
    # Contact & Business Info
    email: Optional[str] = Field(None, description="Contact email")
    website_url: Optional[str] = Field(None, description="Website URL")
    business_category: Optional[str] = Field(None, description="Business/industry category")
    location: Optional[str] = Field(None, description="Geographic location")
    
    # Temporal Data
    last_post_at: Optional[datetime] = Field(None, description="Timestamp of most recent post")
    last_analyzed_at: Optional[datetime] = Field(None, description="Last analysis timestamp")
    data_updated_at: datetime = Field(default_factory=datetime.now, description="Data last updated")
    
    # Platform-Specific Data
    platform_metadata: Dict[str, Any] = Field(default_factory=dict, description="Platform-specific fields")
    raw_data: Optional[Dict[str, Any]] = Field(None, description="Original raw platform data")

class CanonicalAnalysisResult(BaseModel):
    """Unified analysis result schema"""
    analysis_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique analysis ID")
    influencer_id: str = Field(..., description="Canonical influencer ID")
    analysis_timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    
    # Authenticity Scores
    overall_authenticity_score: float = Field(..., description="Overall authenticity score (0-10)")
    engagement_authenticity: float = Field(..., description="Engagement authenticity score")
    content_authenticity: float = Field(..., description="Content authenticity score")
    follower_authenticity: float = Field(..., description="Follower authenticity score")
    posting_pattern_authenticity: float = Field(..., description="Posting pattern authenticity score")
    
    # Detailed Analysis
    red_flags: List[str] = Field(default_factory=list, description="Identified red flags")
    positive_indicators: List[str] = Field(default_factory=list, description="Positive authenticity indicators")
    recommendations: List[str] = Field(default_factory=list, description="Actionable recommendations")
    
    # Risk Assessment
    risk_level: str = Field(..., description="Low, Medium, High, Critical")
    trustworthiness_rating: str = Field(..., description="Highly Trustworthy, Trustworthy, Questionable, Not Recommended")
    
    # Supporting Data
    analyzed_posts_count: int = Field(default=0, description="Number of posts analyzed")
    analysis_confidence: float = Field(..., description="Confidence level of analysis (0-1)")
    data_quality_score: float = Field(..., description="Quality of input data (0-1)")
    
    # Metadata
    analysis_version: str = Field(default="1.0", description="Analysis algorithm version")
    platform_coverage: List[PlatformType] = Field(default_factory=list, description="Platforms included in analysis")

# ===== UTILITY FUNCTIONS =====

def generate_canonical_post_id(platform: PlatformType, platform_post_id: str) -> str:
    """Generate a canonical post ID from platform-specific data"""
    return f"{platform.value}_{platform_post_id}_{uuid.uuid4().hex[:8]}"

def generate_canonical_influencer_id(platform: PlatformType, username: str) -> str:
    """Generate a canonical influencer ID from platform-specific data"""
    return f"{platform.value}_{username}_{uuid.uuid4().hex[:8]}"

# ===== SCHEMA VALIDATION =====

class SchemaValidator:
    """Validates canonical schema compliance"""
    
    @staticmethod
    def validate_influencer(data: Dict[str, Any]) -> CanonicalInfluencer:
        """Validate and create canonical influencer from raw data"""
        try:
            return CanonicalInfluencer(**data)
        except Exception as e:
            raise ValueError(f"Invalid influencer data: {str(e)}")
    
    @staticmethod
    def validate_post(data: Dict[str, Any]) -> CanonicalPost:
        """Validate and create canonical post from raw data"""
        try:
            return CanonicalPost(**data)
        except Exception as e:
            raise ValueError(f"Invalid post data: {str(e)}")
    
    @staticmethod
    def validate_analysis_result(data: Dict[str, Any]) -> CanonicalAnalysisResult:
        """Validate and create canonical analysis result from raw data"""
        try:
            return CanonicalAnalysisResult(**data)
        except Exception as e:
            raise ValueError(f"Invalid analysis result data: {str(e)}")

# Global validator instance
schema_validator = SchemaValidator()
