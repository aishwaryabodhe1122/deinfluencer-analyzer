"""
Multi-Platform API Endpoints
Showcases unified schema capabilities across all supported platforms
"""

from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from database import get_db
from unified_data_manager import unified_data_manager
from canonical_schemas import PlatformType, CanonicalInfluencer
from pydantic import BaseModel

router = APIRouter(prefix="/api/multi-platform", tags=["multi-platform"])

class MultiPlatformRequest(BaseModel):
    username: str
    platforms: Optional[List[str]] = None  # If None, search all platforms

class MultiPlatformResponse(BaseModel):
    username: str
    platforms_found: List[str]
    total_followers: int
    total_posts: int
    cross_platform_consistency: float
    unified_authenticity_score: float
    platform_profiles: Dict[str, Any]
    aggregated_insights: List[str]
    risk_assessment: str

@router.post("/analyze", response_model=MultiPlatformResponse)
async def analyze_multi_platform(
    request: MultiPlatformRequest,
    db: Session = Depends(get_db)
):
    """
    Analyze influencer across all supported platforms using unified schema
    """
    try:
        # Get cross-platform metrics
        cross_platform_metrics = await unified_data_manager.aggregate_cross_platform_metrics(
            request.username
        )
        
        if not cross_platform_metrics:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not find influencer '{request.username}' on any platform"
            )
        
        # Get detailed profiles from all platforms
        multi_platform_profiles = await unified_data_manager.get_multi_platform_profile(
            request.username
        )
        
        # Filter out None profiles
        valid_profiles = {
            platform.value: profile for platform, profile in multi_platform_profiles.items() 
            if profile is not None
        }
        
        if not valid_profiles:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No valid profiles found for '{request.username}'"
            )
        
        # Calculate unified authenticity score (average across platforms)
        authenticity_scores = []
        aggregated_insights = []
        
        for platform_str, profile in valid_profiles.items():
            try:
                platform_enum = PlatformType(platform_str)
                analysis_result = await unified_data_manager.perform_unified_analysis(
                    request.username, platform_enum, include_cross_platform=False
                )
                
                if analysis_result:
                    authenticity_scores.append(analysis_result.overall_authenticity_score)
                    aggregated_insights.extend(analysis_result.red_flags[:2])  # Top 2 red flags per platform
                    aggregated_insights.extend(analysis_result.positive_indicators[:2])  # Top 2 positive indicators
                    
            except Exception as e:
                print(f"Error analyzing {platform_str}: {str(e)}")
                continue
        
        unified_authenticity_score = sum(authenticity_scores) / len(authenticity_scores) if authenticity_scores else 0.0
        
        # Determine risk assessment
        if unified_authenticity_score >= 8.0:
            risk_assessment = "Low Risk - Highly Authentic"
        elif unified_authenticity_score >= 6.0:
            risk_assessment = "Medium Risk - Generally Authentic"
        elif unified_authenticity_score >= 4.0:
            risk_assessment = "High Risk - Authenticity Concerns"
        else:
            risk_assessment = "Critical Risk - Not Recommended"
        
        # Add multi-platform specific insights
        platform_count = len(valid_profiles)
        if platform_count >= 4:
            aggregated_insights.append("🌟 Excellent multi-platform presence indicates established influencer")
        elif platform_count >= 2:
            aggregated_insights.append("✅ Good cross-platform presence")
        
        if cross_platform_metrics.get('is_verified_anywhere'):
            aggregated_insights.append("✅ Verified on at least one platform")
        
        consistency_score = cross_platform_metrics.get('cross_platform_consistency', 0.0)
        if consistency_score > 0.8:
            aggregated_insights.append("✅ High consistency across platforms")
        elif consistency_score < 0.5:
            aggregated_insights.append("⚠️ Low consistency across platforms may indicate different personas")
        
        # Convert profiles to serializable format
        serializable_profiles = {}
        for platform_str, profile in valid_profiles.items():
            serializable_profiles[platform_str] = {
                'username': profile.username,
                'display_name': profile.display_name,
                'follower_count': profile.follower_count,
                'following_count': profile.following_count,
                'post_count': profile.post_count,
                'verified': profile.verification_status.value == 'verified',
                'engagement_rate': profile.average_engagement_rate,
                'bio': profile.bio[:100] + '...' if profile.bio and len(profile.bio) > 100 else profile.bio,
                'authenticity_score': next(
                    (score for score, prof in zip(authenticity_scores, valid_profiles.values()) if prof == profile),
                    0.0
                )
            }
        
        return MultiPlatformResponse(
            username=request.username,
            platforms_found=list(valid_profiles.keys()),
            total_followers=cross_platform_metrics.get('total_followers', 0),
            total_posts=cross_platform_metrics.get('total_posts', 0),
            cross_platform_consistency=consistency_score,
            unified_authenticity_score=unified_authenticity_score,
            platform_profiles=serializable_profiles,
            aggregated_insights=list(set(aggregated_insights))[:10],  # Remove duplicates, limit to 10
            risk_assessment=risk_assessment
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Multi-platform analysis failed: {str(e)}"
        )

@router.get("/platforms")
async def get_supported_platforms():
    """
    Get list of all supported platforms
    """
    return {
        "supported_platforms": [platform.value for platform in PlatformType],
        "total_platforms": len(PlatformType),
        "features": [
            "Unified data schema across all platforms",
            "Cross-platform consistency analysis",
            "Aggregated authenticity scoring",
            "Multi-media content analysis",
            "Real-time data normalization"
        ]
    }

@router.get("/schema/influencer")
async def get_influencer_schema():
    """
    Get the canonical influencer schema definition
    """
    return {
        "schema_name": "CanonicalInfluencer",
        "description": "Unified influencer profile schema for all platforms",
        "supported_platforms": [platform.value for platform in PlatformType],
        "key_features": [
            "Cross-platform ID mapping",
            "Unified engagement metrics",
            "Normalized verification status",
            "Audience insights aggregation",
            "Platform-specific metadata preservation"
        ],
        "sample_fields": {
            "influencer_id": "Unique canonical identifier",
            "platform": "Primary platform",
            "cross_platform_ids": "IDs across other platforms",
            "follower_count": "Normalized follower count",
            "authenticity_score": "Overall authenticity score",
            "audience_insights": "Demographic and behavior data"
        }
    }

@router.get("/schema/post")
async def get_post_schema():
    """
    Get the canonical post schema definition
    """
    return {
        "schema_name": "CanonicalPost",
        "description": "Unified post schema for all platforms and media types",
        "supported_media_types": [
            "text", "image", "video", "audio", "document", 
            "carousel", "story", "live", "reel", "poll"
        ],
        "key_features": [
            "Multi-media support",
            "Unified engagement metrics",
            "Content classification",
            "Hashtag and mention extraction",
            "Authenticity scoring per post"
        ],
        "sample_fields": {
            "post_id": "Unique canonical post identifier",
            "platform": "Source platform",
            "content_text": "Text content",
            "media_items": "All media attachments",
            "engagements": "Normalized engagement metrics",
            "content_category": "Organic, sponsored, promotional, etc.",
            "authenticity_score": "Post-level authenticity score"
        }
    }
