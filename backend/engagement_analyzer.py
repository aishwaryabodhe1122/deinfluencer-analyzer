"""
Advanced Engagement Pattern Analysis Module
Detects bot activity, engagement spikes, and suspicious patterns
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from scipy import stats
import math

class EngagementPatternAnalyzer:
    """
    Advanced analyzer for detecting suspicious engagement patterns
    """
    
    def __init__(self):
        # Thresholds for different platforms
        self.platform_thresholds = {
            "instagram": {
                "normal_engagement_variance": 0.4,
                "suspicious_spike_multiplier": 5.0,
                "bot_comment_ratio": 0.1,  # Comments should be at least 10% of likes
                "rapid_engagement_window": 300  # 5 minutes in seconds
            },
            "twitter": {
                "normal_engagement_variance": 0.6,
                "suspicious_spike_multiplier": 8.0,
                "bot_comment_ratio": 0.05,  # Twitter has lower comment ratios
                "rapid_engagement_window": 180  # 3 minutes
            },
            "youtube": {
                "normal_engagement_variance": 0.5,
                "suspicious_spike_multiplier": 4.0,
                "bot_comment_ratio": 0.02,  # YouTube comments are less frequent
                "rapid_engagement_window": 600  # 10 minutes
            },
            "tiktok": {
                "normal_engagement_variance": 0.7,
                "suspicious_spike_multiplier": 6.0,
                "bot_comment_ratio": 0.15,  # TikTok has high comment engagement
                "rapid_engagement_window": 120  # 2 minutes
            }
        }
    
    def analyze_engagement_patterns(self, posts: List[Dict], platform: str) -> Dict:
        """
        Main function to analyze engagement patterns across posts
        """
        if not posts or len(posts) < 3:
            return self._default_pattern_analysis()
        
        try:
            # Extract engagement metrics
            engagement_data = self._extract_engagement_metrics(posts)
            
            # Perform various pattern analyses
            variance_analysis = self._analyze_engagement_variance(engagement_data, platform)
            spike_analysis = self._detect_engagement_spikes(engagement_data, platform)
            ratio_analysis = self._analyze_comment_like_ratios(engagement_data, platform)
            timing_analysis = self._analyze_posting_timing(posts)
            consistency_analysis = self._analyze_engagement_consistency(engagement_data)
            
            # Calculate overall pattern score
            pattern_score = self._calculate_pattern_score(
                variance_analysis, spike_analysis, ratio_analysis, 
                timing_analysis, consistency_analysis
            )
            
            return {
                "pattern_score": pattern_score,
                "variance_analysis": variance_analysis,
                "spike_analysis": spike_analysis,
                "ratio_analysis": ratio_analysis,
                "timing_analysis": timing_analysis,
                "consistency_analysis": consistency_analysis,
                "red_flags": self._identify_red_flags(
                    variance_analysis, spike_analysis, ratio_analysis, timing_analysis
                ),
                "authenticity_indicators": self._identify_authenticity_indicators(
                    variance_analysis, ratio_analysis, timing_analysis
                )
            }
            
        except Exception as e:
            print(f"Error in engagement pattern analysis: {str(e)}")
            return self._default_pattern_analysis()
    
    def _extract_engagement_metrics(self, posts: List[Dict]) -> pd.DataFrame:
        """
        Extract engagement metrics from posts into a structured format
        """
        data = []
        for post in posts:
            likes = post.get('likes', 0)
            comments = post.get('comments', 0)
            shares = post.get('shares', post.get('retweets', 0))
            created_at = post.get('created_at', datetime.now().isoformat())
            
            # Parse datetime
            try:
                if isinstance(created_at, str):
                    post_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                else:
                    post_time = created_at
            except:
                post_time = datetime.now()
            
            total_engagement = likes + (comments * 3) + (shares * 2)  # Weighted engagement
            
            data.append({
                'likes': likes,
                'comments': comments,
                'shares': shares,
                'total_engagement': total_engagement,
                'comment_like_ratio': comments / max(likes, 1),
                'post_time': post_time,
                'is_sponsored': post.get('is_sponsored', False)
            })
        
        return pd.DataFrame(data)
    
    def _analyze_engagement_variance(self, data: pd.DataFrame, platform: str) -> Dict:
        """
        Analyze variance in engagement patterns
        """
        if len(data) < 3:
            return {"score": 5.0, "variance": 0.5, "is_suspicious": False}
        
        engagements = data['total_engagement'].values
        mean_engagement = np.mean(engagements)
        
        if mean_engagement == 0:
            return {"score": 3.0, "variance": 0.0, "is_suspicious": True}
        
        # Calculate coefficient of variation
        std_engagement = np.std(engagements)
        coefficient_of_variation = std_engagement / mean_engagement
        
        threshold = self.platform_thresholds[platform]["normal_engagement_variance"]
        
        # Score based on variance (moderate variance is good, too low or too high is suspicious)
        if 0.2 <= coefficient_of_variation <= threshold:
            score = 8.5  # Good variance indicates authentic audience
        elif coefficient_of_variation < 0.1:
            score = 3.0  # Too consistent, might be bots
        elif coefficient_of_variation > threshold * 2:
            score = 4.0  # Too inconsistent, might indicate purchased engagement
        else:
            score = 6.0  # Moderate concerns
        
        return {
            "score": score,
            "variance": coefficient_of_variation,
            "is_suspicious": coefficient_of_variation < 0.1 or coefficient_of_variation > threshold * 2,
            "mean_engagement": mean_engagement,
            "std_engagement": std_engagement
        }
    
    def _detect_engagement_spikes(self, data: pd.DataFrame, platform: str) -> Dict:
        """
        Detect suspicious engagement spikes that might indicate bot activity
        """
        if len(data) < 5:
            return {"score": 7.0, "spikes_detected": 0, "suspicious_spikes": []}
        
        engagements = data['total_engagement'].values
        mean_engagement = np.mean(engagements)
        std_engagement = np.std(engagements)
        
        if std_engagement == 0:
            return {"score": 5.0, "spikes_detected": 0, "suspicious_spikes": []}
        
        # Detect spikes using z-score
        z_scores = np.abs(stats.zscore(engagements))
        spike_threshold = self.platform_thresholds[platform]["suspicious_spike_multiplier"]
        
        spikes = []
        for i, z_score in enumerate(z_scores):
            if z_score > spike_threshold:
                spikes.append({
                    "post_index": i,
                    "engagement": engagements[i],
                    "z_score": z_score,
                    "is_sponsored": data.iloc[i]['is_sponsored']
                })
        
        # Score based on number and severity of spikes
        num_spikes = len(spikes)
        total_posts = len(data)
        spike_ratio = num_spikes / total_posts
        
        if spike_ratio == 0:
            score = 9.0  # No spikes is good
        elif spike_ratio <= 0.1:
            score = 7.5  # Few spikes might be normal viral content
        elif spike_ratio <= 0.2:
            score = 5.0  # Moderate spikes are concerning
        else:
            score = 2.0  # Many spikes indicate artificial engagement
        
        # Reduce score if spikes are on non-sponsored content (more suspicious)
        non_sponsored_spikes = [s for s in spikes if not s['is_sponsored']]
        if len(non_sponsored_spikes) > len(spikes) * 0.7:
            score *= 0.8
        
        return {
            "score": score,
            "spikes_detected": num_spikes,
            "spike_ratio": spike_ratio,
            "suspicious_spikes": spikes,
            "avg_spike_severity": np.mean([s['z_score'] for s in spikes]) if spikes else 0
        }
    
    def _analyze_comment_like_ratios(self, data: pd.DataFrame, platform: str) -> Dict:
        """
        Analyze comment-to-like ratios to detect bot activity
        """
        if len(data) == 0:
            return {"score": 5.0, "avg_ratio": 0.0, "is_suspicious": False}
        
        ratios = data['comment_like_ratio'].values
        avg_ratio = np.mean(ratios)
        
        expected_ratio = self.platform_thresholds[platform]["bot_comment_ratio"]
        
        # Score based on how close the ratio is to expected values
        if avg_ratio >= expected_ratio * 0.5:
            if avg_ratio <= expected_ratio * 3:
                score = 8.5  # Good ratio
            else:
                score = 6.0  # High ratio, might be engagement pods
        else:
            score = 4.0  # Low ratio, might indicate bot likes
        
        # Check for consistency in ratios
        ratio_variance = np.var(ratios) if len(ratios) > 1 else 0
        if ratio_variance < 0.001:  # Very consistent ratios are suspicious
            score *= 0.7
        
        return {
            "score": score,
            "avg_ratio": avg_ratio,
            "expected_ratio": expected_ratio,
            "ratio_variance": ratio_variance,
            "is_suspicious": avg_ratio < expected_ratio * 0.3 or ratio_variance < 0.001
        }
    
    def _analyze_posting_timing(self, posts: List[Dict]) -> Dict:
        """
        Analyze posting time patterns to detect automated behavior
        """
        if len(posts) < 5:
            return {"score": 7.0, "pattern_detected": "insufficient_data"}
        
        try:
            # Extract posting hours
            posting_hours = []
            posting_intervals = []
            
            prev_time = None
            for post in posts:
                created_at = post.get('created_at', datetime.now().isoformat())
                try:
                    if isinstance(created_at, str):
                        post_time = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                    else:
                        post_time = created_at
                    
                    posting_hours.append(post_time.hour)
                    
                    if prev_time:
                        interval = abs((post_time - prev_time).total_seconds() / 3600)  # Hours
                        posting_intervals.append(interval)
                    
                    prev_time = post_time
                    
                except:
                    continue
            
            if not posting_hours:
                return {"score": 5.0, "pattern_detected": "parse_error"}
            
            # Analyze hour distribution
            hour_variance = np.var(posting_hours)
            
            # Analyze interval patterns
            if posting_intervals:
                interval_variance = np.var(posting_intervals)
                avg_interval = np.mean(posting_intervals)
                
                # Check for suspiciously regular intervals
                if len(posting_intervals) > 3:
                    interval_cv = np.std(posting_intervals) / max(avg_interval, 1)
                    
                    if interval_cv < 0.1:  # Very regular posting
                        score = 3.0
                        pattern = "automated_regular"
                    elif interval_cv > 2.0:  # Very irregular
                        score = 6.0
                        pattern = "irregular"
                    else:
                        score = 8.0  # Natural variation
                        pattern = "natural"
                else:
                    score = 7.0
                    pattern = "insufficient_intervals"
            else:
                score = 5.0
                pattern = "no_intervals"
                interval_variance = 0
                avg_interval = 0
            
            # Check for posting at unusual hours (3-6 AM consistently might indicate automation)
            night_posts = sum(1 for h in posting_hours if 3 <= h <= 6)
            if night_posts > len(posting_hours) * 0.5:
                score *= 0.8  # Penalty for too many night posts
            
            return {
                "score": score,
                "pattern_detected": pattern,
                "hour_variance": hour_variance,
                "interval_variance": interval_variance,
                "avg_interval_hours": avg_interval,
                "night_post_ratio": night_posts / len(posting_hours) if posting_hours else 0
            }
            
        except Exception as e:
            print(f"Error in timing analysis: {str(e)}")
            return {"score": 5.0, "pattern_detected": "analysis_error"}
    
    def _analyze_engagement_consistency(self, data: pd.DataFrame) -> Dict:
        """
        Analyze consistency of engagement across different post types
        """
        if len(data) < 3:
            return {"score": 7.0, "consistency": "insufficient_data"}
        
        # Separate sponsored and organic posts
        sponsored_posts = data[data['is_sponsored'] == True]
        organic_posts = data[data['is_sponsored'] == False]
        
        if len(sponsored_posts) == 0 or len(organic_posts) == 0:
            return {"score": 7.0, "consistency": "single_type"}
        
        # Compare engagement patterns
        sponsored_avg = sponsored_posts['total_engagement'].mean()
        organic_avg = organic_posts['total_engagement'].mean()
        
        if organic_avg == 0:
            ratio = float('inf')
        else:
            ratio = sponsored_avg / organic_avg
        
        # Suspicious if sponsored posts get significantly more engagement than organic
        if ratio > 3.0:
            score = 3.0  # Very suspicious
            consistency = "sponsored_inflated"
        elif ratio > 1.5:
            score = 5.0  # Moderately suspicious
            consistency = "sponsored_higher"
        elif ratio < 0.3:
            score = 6.0  # Organic much higher (normal but worth noting)
            consistency = "organic_higher"
        else:
            score = 8.0  # Balanced engagement
            consistency = "balanced"
        
        return {
            "score": score,
            "consistency": consistency,
            "sponsored_avg": sponsored_avg,
            "organic_avg": organic_avg,
            "engagement_ratio": ratio
        }
    
    def _calculate_pattern_score(self, variance_analysis: Dict, spike_analysis: Dict, 
                                ratio_analysis: Dict, timing_analysis: Dict, 
                                consistency_analysis: Dict) -> float:
        """
        Calculate overall engagement pattern score
        """
        scores = [
            variance_analysis["score"] * 0.25,
            spike_analysis["score"] * 0.25,
            ratio_analysis["score"] * 0.20,
            timing_analysis["score"] * 0.15,
            consistency_analysis["score"] * 0.15
        ]
        
        return round(sum(scores), 2)
    
    def _identify_red_flags(self, variance_analysis: Dict, spike_analysis: Dict,
                           ratio_analysis: Dict, timing_analysis: Dict) -> List[str]:
        """
        Identify specific red flags in engagement patterns
        """
        red_flags = []
        
        if variance_analysis.get("is_suspicious", False):
            if variance_analysis["variance"] < 0.1:
                red_flags.append("Suspiciously consistent engagement (possible bot activity)")
            else:
                red_flags.append("Extremely inconsistent engagement patterns")
        
        if spike_analysis["spike_ratio"] > 0.2:
            red_flags.append(f"High number of engagement spikes ({spike_analysis['spikes_detected']} spikes detected)")
        
        if ratio_analysis.get("is_suspicious", False):
            red_flags.append("Unusual comment-to-like ratios (possible fake engagement)")
        
        if timing_analysis["pattern_detected"] == "automated_regular":
            red_flags.append("Suspiciously regular posting intervals (possible automation)")
        
        if timing_analysis.get("night_post_ratio", 0) > 0.5:
            red_flags.append("High frequency of posts during unusual hours")
        
        return red_flags
    
    def _identify_authenticity_indicators(self, variance_analysis: Dict, 
                                        ratio_analysis: Dict, timing_analysis: Dict) -> List[str]:
        """
        Identify positive authenticity indicators
        """
        indicators = []
        
        if 0.2 <= variance_analysis.get("variance", 0) <= 0.6:
            indicators.append("Natural variation in engagement levels")
        
        if ratio_analysis["avg_ratio"] >= ratio_analysis["expected_ratio"] * 0.7:
            indicators.append("Healthy comment-to-like ratios")
        
        if timing_analysis["pattern_detected"] == "natural":
            indicators.append("Natural posting time patterns")
        
        return indicators
    
    def _default_pattern_analysis(self) -> Dict:
        """
        Return default analysis when insufficient data
        """
        return {
            "pattern_score": 5.0,
            "variance_analysis": {"score": 5.0, "variance": 0.5, "is_suspicious": False},
            "spike_analysis": {"score": 5.0, "spikes_detected": 0, "suspicious_spikes": []},
            "ratio_analysis": {"score": 5.0, "avg_ratio": 0.05, "is_suspicious": False},
            "timing_analysis": {"score": 5.0, "pattern_detected": "insufficient_data"},
            "consistency_analysis": {"score": 5.0, "consistency": "insufficient_data"},
            "red_flags": [],
            "authenticity_indicators": []
        }

# Global instance
engagement_analyzer = EngagementPatternAnalyzer()
