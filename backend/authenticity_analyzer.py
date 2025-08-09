"""
Advanced Authenticity Analysis Module
Calculates authenticity scores based on real influencer data patterns
Integrates engagement pattern analysis and content quality analysis
"""

import math
from typing import Dict, List
from datetime import datetime
from schemas import InfluencerProfile, AuthenticityScore
from engagement_analyzer import engagement_analyzer
from content_analyzer import content_analyzer

class AuthenticityAnalyzer:
    """
    Advanced authenticity analyzer using real data patterns and ML-inspired algorithms
    """
    
    def __init__(self):
        # Benchmark ranges for different platforms
        self.platform_benchmarks = {
            "instagram": {
                "engagement_rate": {"excellent": 6.0, "good": 3.0, "poor": 1.0},
                "follower_following_ratio": {"excellent": 100, "good": 10, "poor": 2},
                "posts_per_month": {"excellent": 20, "good": 10, "poor": 2}
            },
            "twitter": {
                "engagement_rate": {"excellent": 3.0, "good": 1.5, "poor": 0.5},
                "follower_following_ratio": {"excellent": 50, "good": 5, "poor": 1},
                "posts_per_month": {"excellent": 100, "good": 30, "poor": 5}
            },
            "youtube": {
                "engagement_rate": {"excellent": 8.0, "good": 4.0, "poor": 1.0},
                "follower_following_ratio": {"excellent": 1000, "good": 100, "poor": 10},
                "posts_per_month": {"excellent": 8, "good": 4, "poor": 1}
            },
            "tiktok": {
                "engagement_rate": {"excellent": 15.0, "good": 8.0, "poor": 3.0},
                "follower_following_ratio": {"excellent": 200, "good": 20, "poor": 5},
                "posts_per_month": {"excellent": 30, "good": 15, "poor": 3}
            }
        }
    
    def analyze_authenticity(self, profile: InfluencerProfile, recent_posts: List[Dict] = None) -> AuthenticityScore:
        """
        Main authenticity analysis function with advanced pattern and content analysis
        """
        platform = profile.platform.lower()
        benchmarks = self.platform_benchmarks.get(platform, self.platform_benchmarks["instagram"])
        
        # Perform advanced analysis on posts
        engagement_pattern_analysis = None
        content_quality_analysis = None
        
        if recent_posts:
            # Advanced engagement pattern analysis
            engagement_pattern_analysis = engagement_analyzer.analyze_engagement_patterns(recent_posts, platform)
            
            # Advanced content quality analysis
            content_quality_analysis = content_analyzer.analyze_content_quality(recent_posts, platform)
        
        # Calculate individual scores (enhanced with advanced analysis)
        engagement_quality = self._calculate_engagement_quality(profile, recent_posts, benchmarks, engagement_pattern_analysis)
        content_authenticity = self._calculate_content_authenticity(profile, recent_posts, content_quality_analysis)
        sponsored_ratio = self._calculate_sponsored_ratio(recent_posts)
        follower_authenticity = self._calculate_follower_authenticity(profile, benchmarks)
        consistency_score = self._calculate_consistency_score(profile, recent_posts)
        
        # Calculate weighted overall score
        overall_score = (
            engagement_quality * 0.25 +
            content_authenticity * 0.25 +
            sponsored_ratio * 0.20 +
            follower_authenticity * 0.20 +
            consistency_score * 0.10
        )
        
        return AuthenticityScore(
            overall_score=round(overall_score, 2),
            engagement_quality=round(engagement_quality, 2),
            content_authenticity=round(content_authenticity, 2),
            sponsored_ratio=round(sponsored_ratio, 2),
            follower_authenticity=round(follower_authenticity, 2),
            consistency_score=round(consistency_score, 2),
            last_updated=datetime.now()
        )
    
    def _calculate_engagement_quality(self, profile: InfluencerProfile, recent_posts: List[Dict], benchmarks: Dict, engagement_pattern_analysis: Dict = None) -> float:
        """
        Calculate engagement quality score based on engagement rate, patterns, and advanced analysis
        """
        try:
            # Get engagement rate from profile or calculate from recent posts
            engagement_rate = getattr(profile, 'engagement_rate', None)
            
            if not engagement_rate and recent_posts:
                total_engagement = 0
                total_posts = len(recent_posts)
                
                for post in recent_posts:
                    likes = post.get('likes', 0)
                    comments = post.get('comments', 0)
                    total_engagement += likes + (comments * 5)  # Comments weighted more
                
                if total_posts > 0 and profile.follower_count and profile.follower_count > 0:
                    engagement_rate = (total_engagement / total_posts) / profile.follower_count * 100
                else:
                    engagement_rate = 2.0  # Default
            
            if not engagement_rate:
                engagement_rate = 2.0  # Default fallback
            
            # Score based on platform benchmarks
            excellent_threshold = benchmarks["engagement_rate"]["excellent"]
            good_threshold = benchmarks["engagement_rate"]["good"]
            poor_threshold = benchmarks["engagement_rate"]["poor"]
            
            if engagement_rate >= excellent_threshold:
                base_score = 9.0 + min(1.0, (engagement_rate - excellent_threshold) / excellent_threshold)
            elif engagement_rate >= good_threshold:
                base_score = 6.0 + 3.0 * (engagement_rate - good_threshold) / (excellent_threshold - good_threshold)
            elif engagement_rate >= poor_threshold:
                base_score = 3.0 + 3.0 * (engagement_rate - poor_threshold) / (good_threshold - poor_threshold)
            else:
                base_score = max(1.0, 3.0 * engagement_rate / poor_threshold)
            
            # Penalty for suspiciously high engagement (bot activity)
            if engagement_rate > excellent_threshold * 3:
                base_score *= 0.6  # Significant penalty for unrealistic engagement
            
            # Apply advanced engagement pattern analysis if available
            if engagement_pattern_analysis:
                pattern_score = engagement_pattern_analysis.get('pattern_score', 5.0)
                
                # Weight the pattern analysis (30% of final score)
                enhanced_score = (base_score * 0.7) + (pattern_score * 0.3)
                
                # Additional penalties for red flags
                red_flags = engagement_pattern_analysis.get('red_flags', [])
                if len(red_flags) > 2:
                    enhanced_score *= 0.8  # Penalty for multiple red flags
                elif len(red_flags) > 0:
                    enhanced_score *= 0.9  # Minor penalty for some red flags
                
                # Bonus for authenticity indicators
                auth_indicators = engagement_pattern_analysis.get('authenticity_indicators', [])
                if len(auth_indicators) > 1:
                    enhanced_score *= 1.1  # Bonus for multiple positive indicators
                
                return min(10.0, max(0.0, enhanced_score))
            
            return min(10.0, max(0.0, base_score))
            
        except Exception as e:
            print(f"Error calculating engagement quality: {str(e)}")
            return 5.0  # Default score
    
    def _calculate_content_authenticity(self, profile: InfluencerProfile, recent_posts: List[Dict], content_quality_analysis: Dict = None) -> float:
        """
        Calculate content authenticity based on posting patterns, content variety, and advanced NLP analysis
        """
        try:
            score = 7.0  # Base score
            
            # Bio analysis
            bio = getattr(profile, 'bio', '') or ''
            bio_lower = bio.lower()
            
            # Positive indicators
            authentic_keywords = ['authentic', 'real', 'genuine', 'honest', 'personal', 'family', 'life']
            for keyword in authentic_keywords:
                if keyword in bio_lower:
                    score += 0.3
            
            # Negative indicators
            spam_keywords = ['dm for collab', 'business inquiries', 'pr packages', 'brand partnerships']
            for keyword in spam_keywords:
                if keyword in bio_lower:
                    score -= 0.5
            
            # Apply advanced content quality analysis if available
            if content_quality_analysis:
                quality_score = content_quality_analysis.get('quality_score', 5.0)
                
                # Weight the content analysis (40% of final score)
                enhanced_score = (score * 0.6) + (quality_score * 0.4)
                
                # Additional penalties for content flags
                content_flags = content_quality_analysis.get('content_flags', [])
                if len(content_flags) > 2:
                    enhanced_score *= 0.7  # Significant penalty for multiple content issues
                elif len(content_flags) > 0:
                    enhanced_score *= 0.85  # Minor penalty for some content issues
                
                # Bonus for quality indicators
                quality_indicators = content_quality_analysis.get('quality_indicators', [])
                if len(quality_indicators) > 2:
                    enhanced_score *= 1.15  # Bonus for multiple quality indicators
                elif len(quality_indicators) > 0:
                    enhanced_score *= 1.05  # Small bonus for some quality indicators
                
                # Additional analysis from content modules
                authenticity_analysis = content_quality_analysis.get('authenticity_analysis', {})
                if authenticity_analysis.get('score', 0) > 7.0:
                    enhanced_score *= 1.1  # Bonus for high authenticity in content
                
                spam_analysis = content_quality_analysis.get('spam_analysis', {})
                if spam_analysis.get('score', 10) < 5.0:
                    enhanced_score *= 0.8  # Penalty for high spam indicators
                
                return min(10.0, max(0.0, enhanced_score))
            
            # Fallback to basic post analysis if no advanced analysis available
            if recent_posts:
                sponsored_posts = sum(1 for post in recent_posts if post.get('is_sponsored', False))
                total_posts = len(recent_posts)
                
                if total_posts > 0:
                    sponsored_ratio = sponsored_posts / total_posts
                    
                    # Penalty for too many sponsored posts
                    if sponsored_ratio > 0.5:
                        score -= 2.0
                    elif sponsored_ratio > 0.3:
                        score -= 1.0
                    
                    # Bonus for variety in engagement
                    engagement_variance = self._calculate_engagement_variance(recent_posts)
                    if engagement_variance > 0.3:  # Good variance indicates authentic audience
                        score += 1.0
                    elif engagement_variance < 0.1:  # Low variance might indicate bots
                        score -= 1.0
            
            # Verification bonus (but not too much - can be bought)
            if getattr(profile, 'verified', False):
                score += 0.5
            
            return min(10.0, max(0.0, score))
            
        except Exception as e:
            print(f"Error calculating content authenticity: {str(e)}")
            return 5.0
    
    def _calculate_sponsored_ratio(self, recent_posts: List[Dict]) -> float:
        """
        Calculate score based on sponsored content ratio (lower ratio = higher score)
        """
        try:
            if not recent_posts:
                return 7.0  # Default score when no data
            
            sponsored_posts = sum(1 for post in recent_posts if post.get('is_sponsored', False))
            total_posts = len(recent_posts)
            
            if total_posts == 0:
                return 7.0
            
            sponsored_ratio = sponsored_posts / total_posts
            
            # Score inversely related to sponsored ratio
            if sponsored_ratio == 0:
                return 10.0  # Perfect score for no sponsored content
            elif sponsored_ratio <= 0.1:
                return 9.0  # Excellent - very few sponsored posts
            elif sponsored_ratio <= 0.2:
                return 7.5  # Good - reasonable amount
            elif sponsored_ratio <= 0.3:
                return 6.0  # Moderate
            elif sponsored_ratio <= 0.5:
                return 4.0  # Poor - too many sponsored posts
            else:
                return 2.0  # Very poor - mostly sponsored content
                
        except Exception as e:
            print(f"Error calculating sponsored ratio: {str(e)}")
            return 5.0
    
    def _calculate_follower_authenticity(self, profile: InfluencerProfile, benchmarks: Dict) -> float:
        """
        Calculate follower authenticity based on follower/following ratios and growth patterns
        """
        try:
            follower_count = profile.follower_count
            following_count = profile.following_count
            
            if following_count == 0:
                following_count = 1  # Avoid division by zero
            
            ratio = follower_count / following_count
            
            # Cap the ratio to prevent extreme values (max 100x excellent threshold)
            excellent_ratio = benchmarks["follower_following_ratio"]["excellent"]
            good_ratio = benchmarks["follower_following_ratio"]["good"]
            poor_ratio = benchmarks["follower_following_ratio"]["poor"]
            
            # Use logarithmic scaling for very high ratios to prevent score inflation
            max_reasonable_ratio = excellent_ratio * 100  # 100x excellent threshold
            
            if ratio >= max_reasonable_ratio:
                # For extremely high ratios, use logarithmic scaling
                base_score = 9.5 + min(0.5, math.log10(ratio / max_reasonable_ratio) * 0.1)
            elif ratio >= excellent_ratio:
                base_score = 9.0 + min(1.0, (ratio - excellent_ratio) / excellent_ratio * 0.5)
            elif ratio >= good_ratio:
                base_score = 6.0 + 3.0 * (ratio - good_ratio) / (excellent_ratio - good_ratio)
            elif ratio >= poor_ratio:
                base_score = 3.0 + 3.0 * (ratio - poor_ratio) / (good_ratio - poor_ratio)
            else:
                base_score = max(1.0, 3.0 * ratio / poor_ratio)
            
            # Adjustments based on absolute numbers
            if follower_count < 1000:
                base_score *= 0.8  # Small accounts are harder to verify
            elif follower_count > 10000000:
                base_score *= 0.9  # Very large accounts might have some fake followers
            
            # Penalty for suspicious patterns
            if following_count > follower_count * 2:  # Following way more than followers
                base_score *= 0.7
            
            return min(10.0, max(0.0, base_score))
            
        except Exception as e:
            print(f"Error calculating follower authenticity: {str(e)}")
            return 5.0
    
    def _calculate_consistency_score(self, profile: InfluencerProfile, recent_posts: List[Dict]) -> float:
        """
        Calculate consistency score based on posting frequency and engagement patterns
        """
        try:
            score = 7.0  # Base score
            
            # Post frequency analysis
            if recent_posts and len(recent_posts) > 1:
                # Calculate posting frequency
                posts_per_week = len(recent_posts) / 4  # Assuming recent_posts covers ~4 weeks
                
                platform = profile.platform.lower()
                
                # Optimal posting frequency by platform
                optimal_frequency = {
                    "instagram": {"min": 3, "max": 7},  # 3-7 posts per week
                    "twitter": {"min": 7, "max": 21},   # 1-3 tweets per day
                    "youtube": {"min": 1, "max": 3},    # 1-3 videos per week
                    "tiktok": {"min": 3, "max": 14}     # 3-14 videos per week
                }
                
                freq_range = optimal_frequency.get(platform, optimal_frequency["instagram"])
                
                if freq_range["min"] <= posts_per_week <= freq_range["max"]:
                    score += 1.5  # Bonus for optimal frequency
                elif posts_per_week < freq_range["min"] / 2:
                    score -= 1.0  # Penalty for too infrequent posting
                elif posts_per_week > freq_range["max"] * 2:
                    score -= 1.0  # Penalty for spam-like posting
                
                # Engagement consistency
                engagement_consistency = self._calculate_engagement_consistency(recent_posts)
                score += engagement_consistency
            
            return min(10.0, max(0.0, score))
            
        except Exception as e:
            print(f"Error calculating consistency score: {str(e)}")
            return 5.0
    
    def _calculate_engagement_variance(self, posts: List[Dict]) -> float:
        """
        Calculate variance in engagement across posts
        """
        if len(posts) < 2:
            return 0.5  # Default variance
        
        engagements = []
        for post in posts:
            likes = post.get('likes', 0)
            comments = post.get('comments', 0)
            engagement = likes + (comments * 5)
            engagements.append(engagement)
        
        if not engagements:
            return 0.5
        
        mean_engagement = sum(engagements) / len(engagements)
        if mean_engagement == 0:
            return 0.5
        
        variance = sum((x - mean_engagement) ** 2 for x in engagements) / len(engagements)
        coefficient_of_variation = (variance ** 0.5) / mean_engagement
        
        return min(1.0, coefficient_of_variation)
    
    def _calculate_engagement_consistency(self, posts: List[Dict]) -> float:
        """
        Calculate engagement consistency bonus/penalty
        """
        if len(posts) < 3:
            return 0.0
        
        variance = self._calculate_engagement_variance(posts)
        
        # Moderate variance is good (indicates authentic audience)
        if 0.2 <= variance <= 0.6:
            return 1.0  # Good variance
        elif variance < 0.1:
            return -1.0  # Too consistent (might be bots)
        elif variance > 0.8:
            return -0.5  # Too inconsistent
        else:
            return 0.0  # Default case for other variance ranges
    def generate_insights(self, profile: InfluencerProfile, score: AuthenticityScore, recent_posts: List[Dict] = None) -> List[str]:
        """
        Generate detailed insights based on the authenticity analysis including advanced pattern analysis
        """
        insights = []
        
        # Overall score insights
        if score.overall_score >= 8.0:
            insights.append("🟢 Highly authentic influencer with genuine engagement")
        elif score.overall_score >= 6.0:
            insights.append("🟡 Generally authentic with some areas for improvement")
        elif score.overall_score >= 4.0:
            insights.append("🟠 Moderate authenticity concerns detected")
        else:
            insights.append("🔴 Significant authenticity issues identified")
        
        # Add advanced analysis insights if posts are available
        if recent_posts:
            platform = profile.platform.lower()
            
            # Get advanced engagement pattern insights
            try:
                engagement_analysis = engagement_analyzer.analyze_engagement_patterns(recent_posts, platform)
                
                # Add engagement pattern red flags
                red_flags = engagement_analysis.get('red_flags', [])
                for flag in red_flags[:3]:  # Limit to top 3 red flags
                    insights.append(f"🚩 {flag}")
                
                # Add engagement authenticity indicators
                auth_indicators = engagement_analysis.get('authenticity_indicators', [])
                for indicator in auth_indicators[:2]:  # Limit to top 2 indicators
                    insights.append(f"✅ {indicator}")
                
                # Specific engagement pattern insights
                pattern_score = engagement_analysis.get('pattern_score', 5.0)
                if pattern_score >= 8.0:
                    insights.append("📊 Excellent engagement patterns indicate authentic audience interaction")
                elif pattern_score <= 3.0:
                    insights.append("📊 Concerning engagement patterns detected - possible artificial inflation")
                
            except Exception as e:
                print(f"Error generating engagement insights: {str(e)}")
            
            # Get advanced content quality insights
            try:
                content_analysis = content_analyzer.analyze_content_quality(recent_posts, platform)
                
                # Add content quality flags
                content_flags = content_analysis.get('content_flags', [])
                for flag in content_flags[:2]:  # Limit to top 2 content flags
                    insights.append(f"⚠️ {flag}")
                
                # Add content quality indicators
                quality_indicators = content_analysis.get('quality_indicators', [])
                for indicator in quality_indicators[:2]:  # Limit to top 2 indicators
                    insights.append(f"✨ {indicator}")
                
                # Specific content insights
                quality_score = content_analysis.get('quality_score', 5.0)
                if quality_score >= 8.0:
                    insights.append("📝 High-quality, authentic content with personal storytelling")
                elif quality_score <= 3.0:
                    insights.append("📝 Content shows heavy promotional focus with limited authenticity")
                
                # Hashtag usage insights
                hashtag_analysis = content_analysis.get('hashtag_analysis', {})
                avg_hashtags = hashtag_analysis.get('avg_hashtag_count', 0)
                if avg_hashtags > 15:
                    insights.append("#️⃣ Excessive hashtag usage may indicate spam-like behavior")
                elif avg_hashtags < 2 and platform in ['instagram', 'tiktok']:
                    insights.append("#️⃣ Low hashtag usage may limit content discoverability")
                
            except Exception as e:
                print(f"Error generating content insights: {str(e)}")
        
        # Engagement insights
        if score.engagement_quality >= 8.0:
            insights.append("✅ Excellent engagement rates indicate genuine audience connection")
        elif score.engagement_quality <= 4.0:
            insights.append("⚠️ Low engagement rates may suggest inactive or fake followers")
        
        # Content insights
        if score.content_authenticity >= 8.0:
            insights.append("✅ Content appears genuine and personal")
        elif score.content_authenticity <= 4.0:
            insights.append("⚠️ Content shows signs of heavy commercialization")
        
        # Sponsored content insights
        if score.sponsored_ratio >= 8.0:
            insights.append("✅ Minimal sponsored content maintains authenticity")
        elif score.sponsored_ratio <= 4.0:
            insights.append("⚠️ High ratio of sponsored content may impact trust")
        
        # Follower insights
        if score.follower_authenticity >= 8.0:
            insights.append("✅ Healthy follower-to-following ratio suggests organic growth")
        elif score.follower_authenticity <= 4.0:
            insights.append("⚠️ Follower patterns may indicate purchased or fake followers")
        
        # Platform-specific insights
        platform = profile.platform.lower()
        if platform == "instagram" and profile.follower_count > 100000:
            insights.append("📸 Large Instagram following - check for engagement pod activity")
        elif platform == "twitter" and getattr(profile, 'engagement_rate', 0) > 10:
            insights.append("🐦 Unusually high Twitter engagement - verify authenticity")
        elif platform == "tiktok" and score.consistency_score <= 5.0:
            insights.append("🎵 Inconsistent TikTok posting pattern detected")
        
        return insights
    
    def generate_recommendations(self, profile: InfluencerProfile, score: AuthenticityScore) -> List[str]:
        """
        Generate actionable recommendations based on the analysis
        """
        recommendations = []
        
        if score.overall_score >= 8.0:
            recommendations.append("✅ This influencer appears highly trustworthy for partnerships")
            recommendations.append("💡 Consider long-term collaboration opportunities")
        elif score.overall_score >= 6.0:
            recommendations.append("✅ Generally reliable influencer with minor concerns")
            recommendations.append("💡 Monitor engagement patterns before major campaigns")
        elif score.overall_score >= 4.0:
            recommendations.append("⚠️ Proceed with caution - request additional verification")
            recommendations.append("💡 Consider smaller test campaigns first")
        else:
            recommendations.append("❌ High risk - not recommended for partnerships")
            recommendations.append("💡 Look for alternative influencers with better authenticity scores")
        
        # Specific recommendations based on weak areas
        if score.engagement_quality <= 5.0:
            recommendations.append("🔍 Verify audience quality and engagement authenticity")
        
        if score.sponsored_ratio <= 5.0:
            recommendations.append("📝 Request disclosure of recent brand partnerships")
        
        if score.follower_authenticity <= 5.0:
            recommendations.append("👥 Audit follower quality using third-party tools")
        
        return recommendations

# Global analyzer instance
authenticity_analyzer = AuthenticityAnalyzer()
