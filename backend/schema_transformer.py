"""
Schema Transformation Layer
Converts platform-specific data to canonical schemas for uniform processing
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import re
from canonical_schemas import (
    CanonicalInfluencer, CanonicalPost, CanonicalMediaItem, CanonicalEngagement,
    CanonicalHashtag, CanonicalMention, CanonicalAnalysisResult,
    PlatformType, MediaType, ContentCategory, EngagementType, VerificationStatus,
    generate_canonical_post_id, generate_canonical_influencer_id
)

class SchemaTransformer:
    """
    Transforms platform-specific data into canonical schemas
    """
    
    def __init__(self):
        # Platform-specific field mappings
        self.platform_mappings = {
            PlatformType.INSTAGRAM: {
                'follower_field': 'followers_count',
                'following_field': 'following_count',
                'post_count_field': 'media_count',
                'engagement_fields': ['like_count', 'comment_count', 'share_count'],
                'verification_field': 'is_verified'
            },
            PlatformType.TWITTER: {
                'follower_field': 'followers_count',
                'following_field': 'following_count',
                'post_count_field': 'tweet_count',
                'engagement_fields': ['like_count', 'retweet_count', 'reply_count'],
                'verification_field': 'verified'
            },
            PlatformType.YOUTUBE: {
                'follower_field': 'subscriber_count',
                'following_field': 'subscription_count',
                'post_count_field': 'video_count',
                'engagement_fields': ['like_count', 'comment_count', 'view_count'],
                'verification_field': 'is_verified'
            },
            PlatformType.TIKTOK: {
                'follower_field': 'follower_count',
                'following_field': 'following_count',
                'post_count_field': 'video_count',
                'engagement_fields': ['like_count', 'comment_count', 'share_count'],
                'verification_field': 'verified'
            },
            PlatformType.FACEBOOK: {
                'follower_field': 'followers_count',
                'following_field': 'following_count',
                'post_count_field': 'posts_count',
                'engagement_fields': ['like_count', 'comment_count', 'share_count'],
                'verification_field': 'is_verified'
            },
            PlatformType.LINKEDIN: {
                'follower_field': 'follower_count',
                'following_field': 'connection_count',
                'post_count_field': 'post_count',
                'engagement_fields': ['like_count', 'comment_count', 'share_count'],
                'verification_field': 'is_verified'
            }
        }
    
    def transform_influencer_profile(self, platform_data: Dict[str, Any], platform: PlatformType) -> CanonicalInfluencer:
        """
        Transform platform-specific influencer data to canonical format
        """
        try:
            mapping = self.platform_mappings.get(platform, {})
            
            # Extract core fields with fallbacks
            username = self._extract_field(platform_data, ['username', 'handle', 'screen_name', 'user_name'], '')
            display_name = self._extract_field(platform_data, ['display_name', 'name', 'full_name', 'title'], username)
            bio = self._extract_field(platform_data, ['bio', 'description', 'about', 'summary'], '')
            
            # Extract follower metrics
            follower_count = self._extract_numeric_field(platform_data, [mapping.get('follower_field', 'followers_count'), 'followers', 'follower_count'], 0)
            following_count = self._extract_numeric_field(platform_data, [mapping.get('following_field', 'following_count'), 'following', 'friends_count'], 0)
            post_count = self._extract_numeric_field(platform_data, [mapping.get('post_count_field', 'post_count'), 'posts', 'statuses_count'], 0)
            
            # Extract verification status
            is_verified = self._extract_field(platform_data, [mapping.get('verification_field', 'verified'), 'is_verified', 'verified'], False)
            verification_status = VerificationStatus.VERIFIED if is_verified else VerificationStatus.UNVERIFIED
            
            # Extract engagement rate if available
            engagement_rate = self._extract_numeric_field(platform_data, ['engagement_rate', 'avg_engagement_rate'], None)
            
            # Extract timestamps
            created_at = self._parse_timestamp(platform_data.get('created_at'))
            last_post_at = self._parse_timestamp(platform_data.get('last_post_at'))
            
            # Extract URLs
            profile_image_url = self._extract_field(platform_data, ['profile_image_url', 'avatar_url', 'profile_pic_url', 'picture'], None)
            banner_image_url = self._extract_field(platform_data, ['banner_url', 'cover_photo_url', 'header_image'], None)
            website_url = self._extract_field(platform_data, ['website', 'url', 'external_url'], None)
            
            # Create canonical influencer
            canonical_influencer = CanonicalInfluencer(
                influencer_id=generate_canonical_influencer_id(platform, username),
                platform_user_id=str(platform_data.get('id', platform_data.get('user_id', username))),
                platform=platform,
                username=username,
                display_name=display_name,
                bio=bio,
                profile_image_url=profile_image_url,
                banner_image_url=banner_image_url,
                verification_status=verification_status,
                account_type=self._extract_field(platform_data, ['account_type', 'user_type'], None),
                account_created_at=created_at,
                follower_count=follower_count,
                following_count=following_count,
                post_count=post_count,
                average_engagement_rate=engagement_rate,
                website_url=website_url,
                location=self._extract_field(platform_data, ['location', 'country', 'region'], None),
                last_post_at=last_post_at,
                data_updated_at=datetime.now(timezone.utc),
                platform_metadata=self._extract_platform_metadata(platform_data, platform),
                raw_data=platform_data
            )
            
            return canonical_influencer
            
        except Exception as e:
            raise ValueError(f"Failed to transform {platform} influencer data: {str(e)}")
    
    def transform_post_data(self, platform_data: Dict[str, Any], platform: PlatformType, influencer_id: str) -> CanonicalPost:
        """
        Transform platform-specific post data to canonical format
        """
        try:
            # Extract core identifiers
            platform_post_id = str(platform_data.get('id', platform_data.get('post_id', '')))
            post_id = generate_canonical_post_id(platform, platform_post_id)
            
            # Extract content
            content_text = self._extract_field(platform_data, ['text', 'caption', 'description', 'content', 'message'], '')
            
            # Extract timestamps
            created_at = self._parse_timestamp(platform_data.get('created_at', platform_data.get('timestamp')))
            if not created_at:
                created_at = datetime.now(timezone.utc)
            
            # Extract engagement metrics
            engagements = self._extract_engagement_metrics(platform_data, platform)
            total_engagement = sum(eng.count for eng in engagements)
            
            # Extract media items
            media_items = self._extract_media_items(platform_data, platform)
            
            # Extract hashtags and mentions
            hashtags = self._extract_hashtags(content_text)
            mentions = self._extract_mentions(content_text, platform_data)
            
            # Determine content category
            content_category = self._classify_content(content_text, platform_data)
            is_sponsored = self._detect_sponsored_content(content_text, platform_data)
            
            # Extract location data
            location = self._extract_location_data(platform_data)
            
            # Extract reach and impression data
            reach = self._extract_numeric_field(platform_data, ['reach', 'impressions', 'views'], None)
            impressions = self._extract_numeric_field(platform_data, ['impressions', 'views', 'reach'], None)
            
            # Create canonical post
            canonical_post = CanonicalPost(
                post_id=post_id,
                platform_post_id=platform_post_id,
                platform=platform,
                content_text=content_text,
                media_items=media_items,
                hashtags=hashtags,
                mentions=mentions,
                content_category=content_category,
                is_sponsored=is_sponsored,
                sponsor_info=self._extract_sponsor_info(platform_data),
                engagements=engagements,
                total_engagement=total_engagement,
                engagement_rate=self._calculate_engagement_rate(total_engagement, platform_data),
                created_at=created_at,
                updated_at=self._parse_timestamp(platform_data.get('updated_at')),
                location=location,
                language=self._detect_language(content_text),
                reach=reach,
                impressions=impressions,
                platform_metadata=self._extract_platform_metadata(platform_data, platform),
                raw_data=platform_data
            )
            
            return canonical_post
            
        except Exception as e:
            raise ValueError(f"Failed to transform {platform} post data: {str(e)}")
    
    def transform_analysis_result(self, analysis_data: Dict[str, Any], influencer_id: str) -> CanonicalAnalysisResult:
        """
        Transform analysis results to canonical format
        """
        try:
            return CanonicalAnalysisResult(
                influencer_id=influencer_id,
                overall_authenticity_score=analysis_data.get('overall_score', 0.0),
                engagement_authenticity=analysis_data.get('engagement_quality', 0.0),
                content_authenticity=analysis_data.get('content_authenticity', 0.0),
                follower_authenticity=analysis_data.get('follower_authenticity', 0.0),
                posting_pattern_authenticity=analysis_data.get('consistency_score', 0.0),
                red_flags=analysis_data.get('red_flags', []),
                positive_indicators=analysis_data.get('positive_indicators', []),
                recommendations=analysis_data.get('recommendations', []),
                risk_level=self._determine_risk_level(analysis_data.get('overall_score', 0.0)),
                trustworthiness_rating=self._determine_trustworthiness(analysis_data.get('overall_score', 0.0)),
                analyzed_posts_count=analysis_data.get('posts_analyzed', 0),
                analysis_confidence=analysis_data.get('confidence', 0.8),
                data_quality_score=analysis_data.get('data_quality', 0.8),
                platform_coverage=analysis_data.get('platforms_analyzed', [])
            )
        except Exception as e:
            raise ValueError(f"Failed to transform analysis result: {str(e)}")
    
    # ===== HELPER METHODS =====
    
    def _extract_field(self, data: Dict[str, Any], field_names: List[str], default: Any = None) -> Any:
        """Extract field value using multiple possible field names"""
        for field_name in field_names:
            if field_name in data and data[field_name] is not None:
                return data[field_name]
        return default
    
    def _extract_numeric_field(self, data: Dict[str, Any], field_names: List[str], default: Optional[float] = None) -> Optional[float]:
        """Extract numeric field value"""
        value = self._extract_field(data, field_names, default)
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default
    
    def _parse_timestamp(self, timestamp_str: Any) -> Optional[datetime]:
        """Parse timestamp string to datetime object"""
        if not timestamp_str:
            return None
        
        if isinstance(timestamp_str, datetime):
            return timestamp_str
        
        try:
            # Try different timestamp formats
            formats = [
                '%Y-%m-%dT%H:%M:%S.%fZ',
                '%Y-%m-%dT%H:%M:%SZ',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(str(timestamp_str), fmt).replace(tzinfo=timezone.utc)
                except ValueError:
                    continue
            
            # If all formats fail, try parsing as Unix timestamp
            return datetime.fromtimestamp(float(timestamp_str), tz=timezone.utc)
            
        except (ValueError, TypeError):
            return None
    
    def _extract_engagement_metrics(self, data: Dict[str, Any], platform: PlatformType) -> List[CanonicalEngagement]:
        """Extract engagement metrics for the platform"""
        engagements = []
        mapping = self.platform_mappings.get(platform, {})
        
        # Platform-specific engagement extraction
        if platform == PlatformType.INSTAGRAM:
            engagements.extend([
                CanonicalEngagement(engagement_type=EngagementType.LIKE, count=self._extract_numeric_field(data, ['likes', 'like_count'], 0)),
                CanonicalEngagement(engagement_type=EngagementType.COMMENT, count=self._extract_numeric_field(data, ['comments', 'comment_count'], 0)),
                CanonicalEngagement(engagement_type=EngagementType.SHARE, count=self._extract_numeric_field(data, ['shares', 'share_count'], 0)),
                CanonicalEngagement(engagement_type=EngagementType.SAVE, count=self._extract_numeric_field(data, ['saves', 'save_count'], 0))
            ])
        elif platform == PlatformType.TWITTER:
            engagements.extend([
                CanonicalEngagement(engagement_type=EngagementType.LIKE, count=self._extract_numeric_field(data, ['likes', 'favorite_count'], 0)),
                CanonicalEngagement(engagement_type=EngagementType.RETWEET, count=self._extract_numeric_field(data, ['retweets', 'retweet_count'], 0)),
                CanonicalEngagement(engagement_type=EngagementType.COMMENT, count=self._extract_numeric_field(data, ['replies', 'reply_count'], 0))
            ])
        elif platform == PlatformType.YOUTUBE:
            engagements.extend([
                CanonicalEngagement(engagement_type=EngagementType.LIKE, count=self._extract_numeric_field(data, ['likes', 'like_count'], 0)),
                CanonicalEngagement(engagement_type=EngagementType.COMMENT, count=self._extract_numeric_field(data, ['comments', 'comment_count'], 0)),
                CanonicalEngagement(engagement_type=EngagementType.VIEW, count=self._extract_numeric_field(data, ['views', 'view_count'], 0))
            ])
        elif platform == PlatformType.TIKTOK:
            engagements.extend([
                CanonicalEngagement(engagement_type=EngagementType.LIKE, count=self._extract_numeric_field(data, ['likes', 'like_count'], 0)),
                CanonicalEngagement(engagement_type=EngagementType.COMMENT, count=self._extract_numeric_field(data, ['comments', 'comment_count'], 0)),
                CanonicalEngagement(engagement_type=EngagementType.SHARE, count=self._extract_numeric_field(data, ['shares', 'share_count'], 0)),
                CanonicalEngagement(engagement_type=EngagementType.VIEW, count=self._extract_numeric_field(data, ['views', 'view_count'], 0))
            ])
        
        # Filter out zero engagements
        return [eng for eng in engagements if eng.count > 0]
    
    def _extract_media_items(self, data: Dict[str, Any], platform: PlatformType) -> List[CanonicalMediaItem]:
        """Extract media items from post data"""
        media_items = []
        
        # Extract media based on platform
        media_data = data.get('media', data.get('attachments', []))
        if not isinstance(media_data, list):
            media_data = [media_data] if media_data else []
        
        for i, media in enumerate(media_data):
            if not media:
                continue
                
            media_type = self._determine_media_type(media, platform)
            media_item = CanonicalMediaItem(
                media_id=str(media.get('id', f"{platform}_{i}")),
                media_type=media_type,
                url=media.get('url', media.get('media_url')),
                thumbnail_url=media.get('thumbnail_url', media.get('preview_url')),
                duration_seconds=self._extract_numeric_field(media, ['duration', 'duration_seconds'], None),
                width=self._extract_numeric_field(media, ['width'], None),
                height=self._extract_numeric_field(media, ['height'], None),
                alt_text=media.get('alt_text', media.get('description')),
                metadata=media
            )
            media_items.append(media_item)
        
        return media_items
    
    def _determine_media_type(self, media: Dict[str, Any], platform: PlatformType) -> MediaType:
        """Determine media type from media data"""
        media_type_str = media.get('type', media.get('media_type', '')).lower()
        
        if 'video' in media_type_str or 'mp4' in media_type_str:
            return MediaType.VIDEO
        elif 'image' in media_type_str or 'photo' in media_type_str or 'jpg' in media_type_str or 'png' in media_type_str:
            return MediaType.IMAGE
        elif 'audio' in media_type_str or 'mp3' in media_type_str:
            return MediaType.AUDIO
        elif 'carousel' in media_type_str or 'album' in media_type_str:
            return MediaType.CAROUSEL
        else:
            return MediaType.IMAGE  # Default fallback
    
    def _extract_hashtags(self, text: str) -> List[CanonicalHashtag]:
        """Extract hashtags from text content"""
        if not text:
            return []
        
        hashtag_pattern = r'#(\w+)'
        hashtags = re.findall(hashtag_pattern, text.lower())
        
        return [CanonicalHashtag(tag=tag) for tag in set(hashtags)]
    
    def _extract_mentions(self, text: str, data: Dict[str, Any]) -> List[CanonicalMention]:
        """Extract mentions from text content"""
        if not text:
            return []
        
        mention_pattern = r'@(\w+)'
        mentions = re.findall(mention_pattern, text.lower())
        
        return [CanonicalMention(username=mention, mention_type="mention") for mention in set(mentions)]
    
    def _classify_content(self, text: str, data: Dict[str, Any]) -> ContentCategory:
        """Classify content category"""
        if not text:
            return ContentCategory.UNKNOWN
        
        text_lower = text.lower()
        
        # Check for sponsored content indicators
        sponsored_keywords = ['#ad', '#sponsored', '#partnership', 'paid partnership', 'sponsored by']
        if any(keyword in text_lower for keyword in sponsored_keywords):
            return ContentCategory.SPONSORED
        
        # Check for promotional content
        promo_keywords = ['buy now', 'discount', 'sale', 'promo code', 'link in bio']
        if any(keyword in text_lower for keyword in promo_keywords):
            return ContentCategory.PROMOTIONAL
        
        # Check for educational content
        edu_keywords = ['how to', 'tutorial', 'learn', 'tips', 'guide']
        if any(keyword in text_lower for keyword in edu_keywords):
            return ContentCategory.EDUCATIONAL
        
        # Default to organic
        return ContentCategory.ORGANIC
    
    def _detect_sponsored_content(self, text: str, data: Dict[str, Any]) -> bool:
        """Detect if content is sponsored"""
        if not text:
            return False
        
        sponsored_indicators = [
            '#ad', '#sponsored', '#partnership', 'paid partnership',
            'sponsored by', 'in collaboration with', 'thanks to',
            'gifted', 'pr package', 'brand ambassador'
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in sponsored_indicators)
    
    def _extract_sponsor_info(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract sponsor information if available"""
        sponsor_info = {}
        
        if 'sponsor' in data:
            sponsor_info['sponsor'] = data['sponsor']
        
        if 'brand_partner' in data:
            sponsor_info['brand_partner'] = data['brand_partner']
        
        return sponsor_info if sponsor_info else None
    
    def _extract_location_data(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Extract location data"""
        location_fields = ['location', 'place', 'geo', 'coordinates']
        
        for field in location_fields:
            if field in data and data[field]:
                return data[field]
        
        return None
    
    def _detect_language(self, text: str) -> Optional[str]:
        """Detect content language"""
        if not text:
            return None
        
        # Simple language detection (could be enhanced with proper language detection library)
        # For now, assume English
        return 'en'
    
    def _calculate_engagement_rate(self, total_engagement: int, data: Dict[str, Any]) -> Optional[float]:
        """Calculate engagement rate if follower count is available"""
        follower_count = self._extract_numeric_field(data, ['follower_count', 'followers'], None)
        
        if follower_count and follower_count > 0:
            return (total_engagement / follower_count) * 100
        
        return None
    
    def _extract_platform_metadata(self, data: Dict[str, Any], platform: PlatformType) -> Dict[str, Any]:
        """Extract platform-specific metadata"""
        # Remove common fields that are already mapped to canonical schema
        common_fields = {
            'id', 'username', 'name', 'bio', 'followers_count', 'following_count',
            'created_at', 'verified', 'profile_image_url', 'text', 'caption',
            'likes', 'comments', 'shares', 'retweets'
        }
        
        metadata = {}
        for key, value in data.items():
            if key not in common_fields:
                metadata[key] = value
        
        return metadata
    
    def _determine_risk_level(self, authenticity_score: float) -> str:
        """Determine risk level based on authenticity score"""
        if authenticity_score >= 8.0:
            return "Low"
        elif authenticity_score >= 6.0:
            return "Medium"
        elif authenticity_score >= 4.0:
            return "High"
        else:
            return "Critical"
    
    def _determine_trustworthiness(self, authenticity_score: float) -> str:
        """Determine trustworthiness rating"""
        if authenticity_score >= 8.5:
            return "Highly Trustworthy"
        elif authenticity_score >= 7.0:
            return "Trustworthy"
        elif authenticity_score >= 5.0:
            return "Questionable"
        else:
            return "Not Recommended"

# Global transformer instance
schema_transformer = SchemaTransformer()
