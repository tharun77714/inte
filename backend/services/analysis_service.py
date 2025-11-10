"""
Analysis service for communication skills evaluation
"""

import logging
import re
import nltk
from typing import Dict, List, Tuple
import textstat

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    pass

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for analyzing communication skills"""
    
    def __init__(self):
        """Initialize analysis service"""
        self.filler_words = [
            "um", "uh", "er", "ah", "like", "you know", "so", "well",
            "actually", "basically", "literally", "right", "okay", "ok",
            "hmm", "huh", "yeah", "yep", "nope"
        ]
    
    async def analyze_communication(self, transcript: str) -> Dict:
        """
        Analyze communication skills from transcript
        
        Args:
            transcript: Transcribed text
        
        Returns:
            Dictionary with communication analysis
        """
        try:
            # Detect filler words
            filler_words_found, filler_count = self._detect_filler_words(transcript)
            
            # Calculate clarity score
            clarity_score = self._calculate_clarity_score(transcript)
            
            # Calculate grammar score
            grammar_score = self._calculate_grammar_score(transcript)
            
            # Calculate tone score
            tone_score = self._calculate_tone_score(transcript)
            
            # Overall communication score
            comm_score = (clarity_score * 0.4 + grammar_score * 0.3 + tone_score * 0.3)
            
            # Penalize for excessive filler words
            if filler_count > 5:
                comm_score *= 0.9
            if filler_count > 10:
                comm_score *= 0.8
            
            comm_score = max(0.0, min(1.0, comm_score))
            
            # Generate suggestions
            suggestions = self._generate_communication_suggestions(
                filler_count, clarity_score, grammar_score, tone_score
            )
            
            return {
                "score": round(comm_score, 2),
                "filler_words_count": filler_count,
                "filler_words": list(set(filler_words_found)),
                "clarity_score": round(clarity_score, 2),
                "grammar_score": round(grammar_score, 2),
                "tone_score": round(tone_score, 2),
                "suggestions": suggestions
            }
        except Exception as e:
            logger.error(f"Error analyzing communication: {e}")
            return {
                "score": 0.5,
                "filler_words_count": 0,
                "filler_words": [],
                "clarity_score": 0.5,
                "grammar_score": 0.5,
                "tone_score": 0.5,
                "suggestions": ["Analysis error occurred"]
            }
    
    def _detect_filler_words(self, text: str) -> Tuple[List[str], int]:
        """Detect filler words in text"""
        text_lower = text.lower()
        found_fillers = []
        
        for filler in self.filler_words:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(filler) + r'\b'
            matches = re.findall(pattern, text_lower)
            found_fillers.extend(matches)
        
        return found_fillers, len(found_fillers)
    
    def _calculate_clarity_score(self, text: str) -> float:
        """
        Calculate clarity score based on:
        - Sentence length (optimal 15-20 words)
        - Word complexity
        - Repetition
        """
        if not text or len(text.strip()) == 0:
            return 0.0
        
        sentences = nltk.sent_tokenize(text)
        if not sentences:
            return 0.5
        
        # Average sentence length
        avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
        
        # Optimal sentence length is 15-20 words
        if 15 <= avg_sentence_length <= 20:
            length_score = 1.0
        elif 10 <= avg_sentence_length <= 25:
            length_score = 0.8
        elif 5 <= avg_sentence_length <= 30:
            length_score = 0.6
        else:
            length_score = 0.4
        
        # Check for repetition (repeated phrases)
        words = text.lower().split()
        unique_ratio = len(set(words)) / len(words) if words else 0
        diversity_score = min(1.0, unique_ratio * 1.2)  # Penalize high repetition
        
        # Flesch reading ease (higher = easier to understand)
        try:
            flesch_score = textstat.flesch_reading_ease(text)
            # Normalize to 0-1 (60-100 is good readability)
            readability_score = max(0.0, min(1.0, (flesch_score - 30) / 70))
        except:
            readability_score = 0.7
        
        # Combined clarity score
        clarity = (length_score * 0.3 + diversity_score * 0.3 + readability_score * 0.4)
        return max(0.0, min(1.0, clarity))
    
    def _calculate_grammar_score(self, text: str) -> float:
        """
        Calculate grammar score based on:
        - Sentence structure
        - Common grammar patterns
        """
        if not text or len(text.strip()) == 0:
            return 0.0
        
        sentences = nltk.sent_tokenize(text)
        if not sentences:
            return 0.5
        
        # Basic checks
        score = 0.7  # Base score
        
        # Check for proper sentence endings
        proper_endings = sum(1 for s in sentences if s.strip().endswith(('.', '!', '?')))
        ending_ratio = proper_endings / len(sentences) if sentences else 0
        score += ending_ratio * 0.2
        
        # Check for capitalization
        proper_caps = sum(1 for s in sentences if s and s[0].isupper())
        cap_ratio = proper_caps / len(sentences) if sentences else 0
        score += cap_ratio * 0.1
        
        return max(0.0, min(1.0, score))
    
    def _calculate_tone_score(self, text: str) -> float:
        """
        Calculate tone score based on:
        - Positive/negative words
        - Confidence indicators
        - Professional language
        """
        if not text or len(text.strip()) == 0:
            return 0.5
        
        text_lower = text.lower()
        score = 0.7  # Base score
        
        # Positive indicators
        positive_words = [
            "confident", "excited", "passionate", "motivated", "successful",
            "achieved", "improved", "learned", "expertise", "experience"
        ]
        positive_count = sum(1 for word in positive_words if word in text_lower)
        score += min(0.2, positive_count * 0.05)
        
        # Negative indicators (hesitation, uncertainty)
        negative_words = [
            "maybe", "perhaps", "i think", "i guess", "not sure",
            "don't know", "uncertain", "doubt"
        ]
        negative_count = sum(1 for word in negative_words if word in text_lower)
        score -= min(0.2, negative_count * 0.05)
        
        # Professional language check
        professional_words = [
            "implemented", "developed", "designed", "optimized", "analyzed",
            "collaborated", "managed", "delivered"
        ]
        professional_count = sum(1 for word in professional_words if word in text_lower)
        score += min(0.1, professional_count * 0.02)
        
        return max(0.0, min(1.0, score))
    
    def _generate_communication_suggestions(
        self,
        filler_count: int,
        clarity_score: float,
        grammar_score: float,
        tone_score: float
    ) -> List[str]:
        """Generate personalized communication suggestions"""
        suggestions = []
        
        if filler_count > 5:
            suggestions.append(
                f"Reduce filler words (found {filler_count}). Practice pausing instead of using 'um' or 'uh'."
            )
        
        if clarity_score < 0.6:
            suggestions.append(
                "Improve clarity by using shorter, more direct sentences. Avoid run-on sentences."
            )
        
        if grammar_score < 0.6:
            suggestions.append(
                "Work on grammar and sentence structure. Practice speaking in complete sentences."
            )
        
        if tone_score < 0.6:
            suggestions.append(
                "Use more confident language. Avoid phrases like 'I think' or 'maybe'. Be more assertive."
            )
        
        if not suggestions:
            suggestions.append(
                "Great communication! Continue practicing to maintain consistency."
            )
        
        return suggestions

