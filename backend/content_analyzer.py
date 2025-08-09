"""
Advanced Content Quality Analysis Module
Uses NLP to analyze post content for authenticity indicators
"""

import re
import string
from typing import List, Dict, Tuple, Optional
from collections import Counter
import math

class ContentQualityAnalyzer:
    """
    Advanced NLP-based content analyzer for detecting authentic vs artificial content
    """
    
    def __init__(self):
        # Spam/promotional keywords that indicate low authenticity
        self.spam_keywords = {
            'promotional': [
                'buy now', 'limited time', 'exclusive offer', 'don\'t miss out',
                'click link', 'swipe up', 'dm for price', 'link in bio',
                'use my code', 'discount code', 'promo code', 'affiliate',
                'sponsored by', 'paid partnership', 'brand ambassador'
            ],
            'generic': [
                'amazing', 'incredible', 'unbelievable', 'life-changing',
                'must have', 'game changer', 'obsessed', 'literally dying',
                'can\'t even', 'so blessed', 'living my best life'
            ],
            'engagement_bait': [
                'like if you agree', 'comment below', 'tag a friend',
                'double tap', 'follow for more', 'turn on notifications',
                'what do you think', 'let me know', 'your thoughts'
            ]
        }
        
        # Authentic content indicators
        self.authentic_indicators = {
            'personal': [
                'my family', 'my kids', 'my husband', 'my wife', 'my mom',
                'my dad', 'growing up', 'when i was', 'learned that',
                'realized', 'grateful for', 'thankful', 'appreciate'
            ],
            'storytelling': [
                'yesterday', 'today', 'last week', 'remember when',
                'funny story', 'happened to me', 'experience',
                'journey', 'struggle', 'challenge', 'overcome'
            ],
            'genuine_emotion': [
                'nervous', 'excited', 'scared', 'proud', 'disappointed',
                'surprised', 'confused', 'frustrated', 'hopeful',
                'worried', 'relieved', 'overwhelmed'
            ]
        }
        
        # Platform-specific content patterns
        self.platform_patterns = {
            'instagram': {
                'optimal_hashtag_count': (5, 15),
                'optimal_caption_length': (50, 300),
                'authentic_hashtag_ratio': 0.7  # 70% should be relevant, not generic
            },
            'twitter': {
                'optimal_hashtag_count': (1, 3),
                'optimal_caption_length': (20, 200),
                'authentic_hashtag_ratio': 0.8
            },
            'tiktok': {
                'optimal_hashtag_count': (3, 8),
                'optimal_caption_length': (10, 150),
                'authentic_hashtag_ratio': 0.6
            },
            'youtube': {
                'optimal_hashtag_count': (0, 5),
                'optimal_caption_length': (100, 1000),
                'authentic_hashtag_ratio': 0.9
            }
        }
    
    def analyze_content_quality(self, posts: List[Dict], platform: str) -> Dict:
        """
        Main function to analyze content quality across posts
        """
        if not posts:
            return self._default_content_analysis()
        
        try:
            # Extract text content from posts
            content_texts = self._extract_content_texts(posts)
            
            if not content_texts:
                return self._default_content_analysis()
            
            # Perform various content analyses
            authenticity_analysis = self._analyze_content_authenticity(content_texts)
            spam_analysis = self._analyze_spam_indicators(content_texts)
            diversity_analysis = self._analyze_content_diversity(content_texts)
            hashtag_analysis = self._analyze_hashtag_usage(posts, platform)
            language_analysis = self._analyze_language_quality(content_texts)
            
            # Calculate overall content quality score
            quality_score = self._calculate_content_quality_score(
                authenticity_analysis, spam_analysis, diversity_analysis,
                hashtag_analysis, language_analysis
            )
            
            return {
                "quality_score": quality_score,
                "authenticity_analysis": authenticity_analysis,
                "spam_analysis": spam_analysis,
                "diversity_analysis": diversity_analysis,
                "hashtag_analysis": hashtag_analysis,
                "language_analysis": language_analysis,
                "content_flags": self._identify_content_flags(
                    authenticity_analysis, spam_analysis, hashtag_analysis
                ),
                "quality_indicators": self._identify_quality_indicators(
                    authenticity_analysis, diversity_analysis, language_analysis
                )
            }
            
        except Exception as e:
            print(f"Error in content quality analysis: {str(e)}")
            return self._default_content_analysis()
    
    def _extract_content_texts(self, posts: List[Dict]) -> List[str]:
        """
        Extract text content from posts
        """
        texts = []
        for post in posts:
            caption = post.get('caption', '')
            if caption and isinstance(caption, str):
                # Clean up the text
                cleaned_text = self._clean_text(caption)
                if cleaned_text:
                    texts.append(cleaned_text)
        return texts
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text content
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove mentions and hashtags for content analysis (but keep the text)
        text = re.sub(r'[@#]\w+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def _analyze_content_authenticity(self, texts: List[str]) -> Dict:
        """
        Analyze authenticity indicators in content
        """
        if not texts:
            return {"score": 5.0, "personal_score": 0, "storytelling_score": 0, "emotion_score": 0}
        
        personal_matches = 0
        storytelling_matches = 0
        emotion_matches = 0
        total_words = 0
        
        for text in texts:
            words = text.split()
            total_words += len(words)
            
            # Count personal indicators
            for indicator in self.authentic_indicators['personal']:
                if indicator in text:
                    personal_matches += 1
            
            # Count storytelling indicators
            for indicator in self.authentic_indicators['storytelling']:
                if indicator in text:
                    storytelling_matches += 1
            
            # Count genuine emotion indicators
            for indicator in self.authentic_indicators['genuine_emotion']:
                if indicator in text:
                    emotion_matches += 1
        
        # Calculate scores based on frequency
        avg_words_per_post = total_words / len(texts) if texts else 0
        
        personal_score = min(10.0, (personal_matches / len(texts)) * 5)
        storytelling_score = min(10.0, (storytelling_matches / len(texts)) * 4)
        emotion_score = min(10.0, (emotion_matches / len(texts)) * 6)
        
        # Overall authenticity score
        authenticity_score = (personal_score * 0.4 + storytelling_score * 0.3 + emotion_score * 0.3)
        
        # Bonus for longer, more detailed posts
        if avg_words_per_post > 50:
            authenticity_score *= 1.1
        
        return {
            "score": min(10.0, authenticity_score),
            "personal_score": personal_score,
            "storytelling_score": storytelling_score,
            "emotion_score": emotion_score,
            "avg_words_per_post": avg_words_per_post,
            "personal_matches": personal_matches,
            "storytelling_matches": storytelling_matches,
            "emotion_matches": emotion_matches
        }
    
    def _analyze_spam_indicators(self, texts: List[str]) -> Dict:
        """
        Analyze spam and promotional content indicators
        """
        if not texts:
            return {"score": 7.0, "promotional_score": 0, "generic_score": 0, "bait_score": 0}
        
        promotional_matches = 0
        generic_matches = 0
        bait_matches = 0
        
        for text in texts:
            # Count promotional indicators
            for indicator in self.spam_keywords['promotional']:
                if indicator in text:
                    promotional_matches += 1
            
            # Count generic language
            for indicator in self.spam_keywords['generic']:
                if indicator in text:
                    generic_matches += 1
            
            # Count engagement bait
            for indicator in self.spam_keywords['engagement_bait']:
                if indicator in text:
                    bait_matches += 1
        
        # Calculate penalty scores (higher matches = lower authenticity)
        promotional_penalty = min(5.0, (promotional_matches / len(texts)) * 3)
        generic_penalty = min(3.0, (generic_matches / len(texts)) * 2)
        bait_penalty = min(2.0, (bait_matches / len(texts)) * 1.5)
        
        # Overall spam score (10 - penalties)
        spam_score = max(0.0, 10.0 - promotional_penalty - generic_penalty - bait_penalty)
        
        return {
            "score": spam_score,
            "promotional_penalty": promotional_penalty,
            "generic_penalty": generic_penalty,
            "bait_penalty": bait_penalty,
            "promotional_matches": promotional_matches,
            "generic_matches": generic_matches,
            "bait_matches": bait_matches
        }
    
    def _analyze_content_diversity(self, texts: List[str]) -> Dict:
        """
        Analyze diversity and uniqueness of content
        """
        if len(texts) < 2:
            return {"score": 7.0, "uniqueness": 1.0, "vocabulary_diversity": 1.0}
        
        # Calculate text similarity (simple approach)
        similarities = []
        for i in range(len(texts)):
            for j in range(i + 1, len(texts)):
                similarity = self._calculate_text_similarity(texts[i], texts[j])
                similarities.append(similarity)
        
        avg_similarity = sum(similarities) / len(similarities) if similarities else 0
        uniqueness = 1.0 - avg_similarity
        
        # Calculate vocabulary diversity
        all_words = []
        for text in texts:
            all_words.extend(text.split())
        
        if not all_words:
            vocabulary_diversity = 1.0
        else:
            unique_words = len(set(all_words))
            total_words = len(all_words)
            vocabulary_diversity = unique_words / total_words
        
        # Calculate diversity score
        diversity_score = (uniqueness * 0.6 + vocabulary_diversity * 0.4) * 10
        
        return {
            "score": min(10.0, diversity_score),
            "uniqueness": uniqueness,
            "vocabulary_diversity": vocabulary_diversity,
            "avg_similarity": avg_similarity,
            "unique_word_count": len(set(all_words)) if all_words else 0,
            "total_word_count": len(all_words) if all_words else 0
        }
    
    def _analyze_hashtag_usage(self, posts: List[Dict], platform: str) -> Dict:
        """
        Analyze hashtag usage patterns
        """
        if not posts:
            return {"score": 7.0, "avg_hashtag_count": 0, "hashtag_relevance": 1.0}
        
        hashtag_counts = []
        all_hashtags = []
        
        for post in posts:
            caption = post.get('caption', '')
            if caption:
                hashtags = re.findall(r'#\w+', caption.lower())
                hashtag_counts.append(len(hashtags))
                all_hashtags.extend(hashtags)
        
        if not hashtag_counts:
            return {"score": 7.0, "avg_hashtag_count": 0, "hashtag_relevance": 1.0}
        
        avg_hashtag_count = sum(hashtag_counts) / len(hashtag_counts)
        
        # Get platform-specific optimal range
        platform_config = self.platform_patterns.get(platform, self.platform_patterns['instagram'])
        optimal_min, optimal_max = platform_config['optimal_hashtag_count']
        
        # Score based on hashtag count
        if optimal_min <= avg_hashtag_count <= optimal_max:
            count_score = 10.0
        elif avg_hashtag_count < optimal_min:
            count_score = max(5.0, 10.0 - (optimal_min - avg_hashtag_count) * 0.5)
        else:
            count_score = max(3.0, 10.0 - (avg_hashtag_count - optimal_max) * 0.3)
        
        # Analyze hashtag diversity (avoid repetitive hashtags)
        if all_hashtags:
            hashtag_counter = Counter(all_hashtags)
            most_common_count = hashtag_counter.most_common(1)[0][1] if hashtag_counter else 1
            diversity_score = min(10.0, (len(set(all_hashtags)) / len(all_hashtags)) * 10)
            
            # Penalty for overusing the same hashtags
            if most_common_count > len(posts) * 0.8:
                diversity_score *= 0.6
        else:
            diversity_score = 10.0
        
        # Overall hashtag score
        hashtag_score = (count_score * 0.6 + diversity_score * 0.4)
        
        return {
            "score": hashtag_score,
            "avg_hashtag_count": avg_hashtag_count,
            "hashtag_diversity": diversity_score,
            "unique_hashtags": len(set(all_hashtags)),
            "total_hashtags": len(all_hashtags),
            "most_used_hashtag": hashtag_counter.most_common(1)[0] if all_hashtags else None
        }
    
    def _analyze_language_quality(self, texts: List[str]) -> Dict:
        """
        Analyze language quality and readability
        """
        if not texts:
            return {"score": 7.0, "avg_sentence_length": 0, "readability": 5.0}
        
        total_sentences = 0
        total_words = 0
        total_syllables = 0
        
        for text in texts:
            sentences = self._count_sentences(text)
            words = len(text.split())
            syllables = self._count_syllables(text)
            
            total_sentences += sentences
            total_words += words
            total_syllables += syllables
        
        if total_sentences == 0 or total_words == 0:
            return {"score": 5.0, "avg_sentence_length": 0, "readability": 5.0}
        
        # Calculate readability metrics
        avg_sentence_length = total_words / total_sentences
        avg_syllables_per_word = total_syllables / total_words
        
        # Simple readability score (based on Flesch Reading Ease)
        readability = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        readability = max(0, min(100, readability))  # Clamp between 0-100
        
        # Score based on readability (60-70 is good for social media)
        if 50 <= readability <= 80:
            language_score = 9.0
        elif 30 <= readability <= 90:
            language_score = 7.0
        else:
            language_score = 5.0
        
        return {
            "score": language_score,
            "avg_sentence_length": avg_sentence_length,
            "avg_syllables_per_word": avg_syllables_per_word,
            "readability": readability,
            "total_words": total_words,
            "total_sentences": total_sentences
        }
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts using Jaccard similarity
        """
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 and not words2:
            return 1.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _count_sentences(self, text: str) -> int:
        """
        Count sentences in text
        """
        sentence_endings = ['.', '!', '?']
        count = 0
        for char in text:
            if char in sentence_endings:
                count += 1
        return max(1, count)  # At least 1 sentence
    
    def _count_syllables(self, text: str) -> int:
        """
        Estimate syllable count in text
        """
        words = text.split()
        syllable_count = 0
        
        for word in words:
            word = word.lower().strip(string.punctuation)
            if not word:
                continue
            
            # Simple syllable counting heuristic
            vowels = 'aeiouy'
            syllables = 0
            prev_was_vowel = False
            
            for char in word:
                if char in vowels:
                    if not prev_was_vowel:
                        syllables += 1
                    prev_was_vowel = True
                else:
                    prev_was_vowel = False
            
            # Handle silent e
            if word.endswith('e') and syllables > 1:
                syllables -= 1
            
            # Every word has at least 1 syllable
            syllables = max(1, syllables)
            syllable_count += syllables
        
        return syllable_count
    
    def _calculate_content_quality_score(self, authenticity_analysis: Dict, spam_analysis: Dict,
                                       diversity_analysis: Dict, hashtag_analysis: Dict,
                                       language_analysis: Dict) -> float:
        """
        Calculate overall content quality score
        """
        scores = [
            authenticity_analysis["score"] * 0.30,
            spam_analysis["score"] * 0.25,
            diversity_analysis["score"] * 0.20,
            hashtag_analysis["score"] * 0.15,
            language_analysis["score"] * 0.10
        ]
        
        return round(sum(scores), 2)
    
    def _identify_content_flags(self, authenticity_analysis: Dict, spam_analysis: Dict,
                              hashtag_analysis: Dict) -> List[str]:
        """
        Identify content quality red flags
        """
        flags = []
        
        if authenticity_analysis["score"] < 4.0:
            flags.append("Low authenticity indicators in content")
        
        if spam_analysis["promotional_matches"] > len(spam_analysis) * 0.3:
            flags.append("High promotional content ratio")
        
        if spam_analysis["bait_matches"] > 0:
            flags.append("Engagement bait tactics detected")
        
        if hashtag_analysis["avg_hashtag_count"] > 20:
            flags.append("Excessive hashtag usage")
        
        return flags
    
    def _identify_quality_indicators(self, authenticity_analysis: Dict, diversity_analysis: Dict,
                                   language_analysis: Dict) -> List[str]:
        """
        Identify positive content quality indicators
        """
        indicators = []
        
        if authenticity_analysis["personal_score"] > 5.0:
            indicators.append("Personal and relatable content")
        
        if authenticity_analysis["storytelling_score"] > 4.0:
            indicators.append("Good storytelling elements")
        
        if diversity_analysis["uniqueness"] > 0.7:
            indicators.append("Diverse and unique content")
        
        if language_analysis["readability"] > 60:
            indicators.append("Good readability and language quality")
        
        return indicators
    
    def _default_content_analysis(self) -> Dict:
        """
        Return default analysis when insufficient data
        """
        return {
            "quality_score": 5.0,
            "authenticity_analysis": {"score": 5.0, "personal_score": 0, "storytelling_score": 0, "emotion_score": 0},
            "spam_analysis": {"score": 7.0, "promotional_penalty": 0, "generic_penalty": 0, "bait_penalty": 0},
            "diversity_analysis": {"score": 7.0, "uniqueness": 1.0, "vocabulary_diversity": 1.0},
            "hashtag_analysis": {"score": 7.0, "avg_hashtag_count": 0, "hashtag_relevance": 1.0},
            "language_analysis": {"score": 7.0, "avg_sentence_length": 0, "readability": 5.0},
            "content_flags": [],
            "quality_indicators": []
        }

# Global instance
content_analyzer = ContentQualityAnalyzer()
