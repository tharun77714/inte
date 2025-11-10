"""
LLM service for interview question generation and response evaluation
Uses free/open-source models from Hugging Face
"""

import logging
from typing import List, Optional, Dict
import asyncio
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, AutoModel
from sentence_transformers import SentenceTransformer
import torch
import numpy as np

logger = logging.getLogger(__name__)


class LLMService:
    """Service for LLM operations using free models"""
    
    def __init__(self):
        """Initialize LLM models"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
        # Initialize models
        self.text_generator = None
        self.semantic_model = None
        self._models_loaded = False
        self._loading = False
        
        # Start loading models in background (non-blocking)
        import threading
        self._load_thread = threading.Thread(target=self._load_models_sync, daemon=True)
        self._load_thread.start()
    
    def _load_models_sync(self):
        """Load pretrained models synchronously (runs in background thread)"""
        try:
            if self._loading:
                return
            self._loading = True
            
            logger.info("Loading pretrained models in background...")
            
            # Load text generation model for question generation
            # Using GPT-2 small for fast, local inference
            logger.info("Loading GPT-2 for text generation...")
            self.text_generator = pipeline(
                "text-generation",
                model="gpt2",
                device=0 if self.device == "cuda" else -1,
                max_length=100,
                do_sample=True,
                temperature=0.7
            )
            logger.info("✓ GPT-2 loaded")
            
            # Load sentence transformer for semantic similarity (evaluation)
            # Using all-MiniLM-L6-v2 (fast, lightweight, good quality)
            logger.info("Loading Sentence Transformer for semantic analysis...")
            self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✓ Sentence Transformer loaded")
            
            self._models_loaded = True
            logger.info("All models loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            logger.warning("Falling back to template-based approach")
            self._models_loaded = False
        finally:
            self._loading = False
    
    async def generate_question(self, domain: str, experience_level: str) -> str:
        """
        Generate interview question based on domain and experience level
        
        Args:
            domain: Interview domain (software, data_science, etc.)
            experience_level: fresher, intermediate, senior
        
        Returns:
            Generated interview question
        """
        try:
            # Wait for models to load
            if not self._models_loaded:
                # Wait a bit and check again
                await asyncio.sleep(1)
                if not self._models_loaded:
                    # Fallback to templates if models not loaded
                    questions = self._get_question_templates(domain, experience_level)
                    import random
                    return random.choice(questions)
            
            # Use LLM to generate question
            prompt = f"Generate an interview question for a {experience_level} level {domain} engineer. Question:"
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._generate_text,
                prompt
            )
            
            # Clean up generated text
            question = result.strip()
            # Remove the prompt if it's included
            if "Question:" in question:
                question = question.split("Question:")[-1].strip()
            
            # Validate and return
            if len(question) > 10 and len(question) < 200:
                return question
            else:
                # Fallback if generated text is invalid
                questions = self._get_question_templates(domain, experience_level)
                import random
                return random.choice(questions)
        
        except Exception as e:
            logger.error(f"Error generating question: {e}")
            # Fallback to template question
            questions = self._get_question_templates(domain, experience_level)
            import random
            return random.choice(questions)
    
    def _generate_text(self, prompt: str) -> str:
        """Synchronous text generation (runs in thread pool)"""
        try:
            result = self.text_generator(
                prompt,
                max_new_tokens=50,
                num_return_sequences=1,
                pad_token_id=self.text_generator.tokenizer.eos_token_id
            )
            return result[0]['generated_text']
        except Exception as e:
            logger.error(f"Text generation error: {e}")
            return prompt
    
    async def generate_followup_question(
        self,
        domain: str,
        experience_level: str,
        previous_answers: List[str]
    ) -> str:
        """Generate follow-up question based on previous answers"""
        try:
            # Analyze previous answers to generate contextual follow-up
            # For now, use template-based approach
            questions = self._get_followup_templates(domain, experience_level)
            import random
            return random.choice(questions)
        except Exception as e:
            logger.error(f"Error generating followup question: {e}")
            return self._get_fallback_question(domain)
    
    async def evaluate_response(
        self,
        question: str,
        answer: str,
        domain: str
    ) -> dict:
        """
        Evaluate candidate's response for technical correctness
        
        Args:
            question: Interview question
            answer: Candidate's answer
            domain: Interview domain
        
        Returns:
            Evaluation dictionary with score and feedback
        """
        try:
            # Use semantic similarity + rule-based evaluation
            semantic_score = await self._calculate_semantic_score(question, answer, domain)
            keyword_score = self._calculate_keyword_score(answer, domain)
            length_score = self._calculate_length_score(answer)
            
            # Combined score (weighted)
            score = (
                semantic_score * 0.5 +  # 50% semantic similarity
                keyword_score * 0.3 +   # 30% keyword matching
                length_score * 0.2      # 20% answer length
            )
            
            score = max(0.0, min(1.0, score))
            
            feedback = self._generate_technical_feedback(question, answer, domain, score)
            
            return {
                "score": round(score, 2),
                "correctness": round(semantic_score, 2),
                "completeness": round(length_score, 2),
                "relevance": round(keyword_score, 2),
                "feedback": feedback,
                "suggestions": self._get_improvement_suggestions(domain, score)
            }
        except Exception as e:
            logger.error(f"Error evaluating response: {e}")
            return {
                "score": 0.5,
                "correctness": 0.5,
                "completeness": 0.5,
                "relevance": 0.5,
                "feedback": "Evaluation error occurred",
                "suggestions": []
            }
    
    async def _calculate_semantic_score(self, question: str, answer: str, domain: str) -> float:
        """Calculate semantic similarity score using sentence transformers"""
        try:
            if not self._models_loaded or self.semantic_model is None:
                # Fallback if model not loaded
                return 0.5
            
            # Get expected answer concepts for the question
            expected_concepts = self._get_expected_concepts(question, domain)
            
            # Encode question, answer, and expected concepts
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None,
                self._encode_texts,
                [question, answer] + expected_concepts
            )
            
            question_emb = embeddings[0]
            answer_emb = embeddings[1]
            concept_embs = embeddings[2:]
            
            # Calculate similarity between answer and question
            question_similarity = np.dot(answer_emb, question_emb) / (
                np.linalg.norm(answer_emb) * np.linalg.norm(question_emb)
            )
            
            # Calculate similarity with expected concepts
            concept_similarities = [
                np.dot(answer_emb, concept_emb) / (
                    np.linalg.norm(answer_emb) * np.linalg.norm(concept_emb)
                )
                for concept_emb in concept_embs
            ]
            avg_concept_similarity = np.mean(concept_similarities) if concept_similarities else 0.5
            
            # Combined semantic score
            semantic_score = (question_similarity * 0.4 + avg_concept_similarity * 0.6)
            
            # Normalize to 0-1 range (cosine similarity is -1 to 1)
            semantic_score = (semantic_score + 1) / 2
            
            return float(semantic_score)
        except Exception as e:
            logger.error(f"Error calculating semantic score: {e}")
            return 0.5
    
    def _encode_texts(self, texts: List[str]) -> np.ndarray:
        """Encode texts using sentence transformer"""
        return self.semantic_model.encode(texts, convert_to_numpy=True)
    
    def _get_expected_concepts(self, question: str, domain: str) -> List[str]:
        """Get expected concepts/key points for a question"""
        # Domain-specific expected concepts
        concept_map = {
            "software": [
                "programming concepts",
                "software development",
                "coding best practices",
                "technical implementation"
            ],
            "data_science": [
                "machine learning",
                "data analysis",
                "statistical methods",
                "data processing"
            ],
            "electronics": [
                "circuit design",
                "electronic components",
                "signal processing",
                "electrical principles"
            ],
            "general": [
                "professional experience",
                "problem solving",
                "team collaboration",
                "technical skills"
            ]
        }
        return concept_map.get(domain, concept_map["general"])
    
    def _calculate_keyword_score(self, answer: str, domain: str) -> float:
        """Calculate score based on domain-specific keywords"""
        domain_keywords = self._get_domain_keywords(domain)
        answer_lower = answer.lower()
        
        keyword_matches = sum(1 for keyword in domain_keywords if keyword in answer_lower)
        
        # Score based on keyword density
        if keyword_matches == 0:
            return 0.3
        elif keyword_matches < 3:
            return 0.5
        elif keyword_matches < 5:
            return 0.7
        else:
            return 0.9
    
    def _calculate_length_score(self, answer: str) -> float:
        """Calculate score based on answer length and completeness"""
        word_count = len(answer.split())
        
        # Optimal answer length is 30-100 words
        if word_count < 10:
            return 0.3  # Too short
        elif word_count < 20:
            return 0.6  # Short but acceptable
        elif word_count <= 100:
            return 0.9  # Good length
        elif word_count <= 150:
            return 0.8  # Slightly long
        else:
            return 0.7  # Too long
    
    def _generate_technical_feedback(self, question: str, answer: str, domain: str, score: float) -> str:
        """Generate technical feedback"""
        if score >= 0.7:
            return f"Good answer! You demonstrated understanding of {domain} concepts. Consider adding more specific examples."
        elif score >= 0.5:
            return f"Your answer shows basic understanding. Try to be more specific and provide concrete examples from {domain}."
        else:
            return f"Your answer needs more depth. Review {domain} fundamentals and practice explaining concepts clearly."
    
    def _get_question_templates(self, domain: str, experience_level: str) -> List[str]:
        """Get question templates for domain and level"""
        templates = {
            "software": {
                "fresher": [
                    "What is object-oriented programming? Explain with an example.",
                    "Describe the difference between a list and a tuple in Python.",
                    "What is the time complexity of binary search?",
                    "Explain what a REST API is.",
                    "What is version control and why is it important?"
                ],
                "intermediate": [
                    "Explain the difference between SQL and NoSQL databases.",
                    "What is the difference between synchronous and asynchronous programming?",
                    "Describe how you would design a caching system.",
                    "What are design patterns? Give examples of common ones.",
                    "Explain microservices architecture and its benefits."
                ]
            },
            "data_science": {
                "fresher": [
                    "What is the difference between supervised and unsupervised learning?",
                    "Explain what overfitting means in machine learning.",
                    "What is cross-validation and why is it important?",
                    "Describe the difference between classification and regression.",
                    "What is feature engineering?"
                ],
                "intermediate": [
                    "Explain the bias-variance tradeoff in machine learning.",
                    "How would you handle missing data in a dataset?",
                    "Describe different evaluation metrics for classification problems.",
                    "What is regularization and why is it used?",
                    "Explain the difference between bagging and boosting."
                ]
            },
            "electronics": {
                "fresher": [
                    "Explain Ohm's law and its applications.",
                    "What is the difference between AC and DC current?",
                    "Describe what a transistor does in a circuit.",
                    "What is a microcontroller and how does it differ from a microprocessor?",
                    "Explain the concept of voltage, current, and resistance."
                ],
                "intermediate": [
                    "How would you design a power supply circuit?",
                    "Explain the difference between analog and digital signals.",
                    "Describe how a MOSFET works.",
                    "What is signal processing and why is it important?",
                    "Explain the concept of impedance in AC circuits."
                ]
            },
            "general": {
                "fresher": [
                    "Tell me about yourself.",
                    "Why do you want to work in this field?",
                    "What are your strengths and weaknesses?",
                    "Where do you see yourself in 5 years?",
                    "Why should we hire you?"
                ]
            }
        }
        
        return templates.get(domain, templates["general"]).get(experience_level, templates["general"]["fresher"])
    
    def _get_followup_templates(self, domain: str, experience_level: str) -> List[str]:
        """Get follow-up question templates"""
        return [
            "Can you elaborate on that?",
            "Can you give a specific example?",
            "How would you handle edge cases in that scenario?",
            "What challenges have you faced with this?",
            "How would you improve that approach?"
        ]
    
    def _get_fallback_question(self, domain: str) -> str:
        """Get fallback question if generation fails"""
        return f"Tell me about your experience with {domain}."
    
    def _get_domain_keywords(self, domain: str) -> List[str]:
        """Get relevant keywords for domain"""
        keywords = {
            "software": ["algorithm", "data structure", "api", "database", "framework", "code", "programming"],
            "data_science": ["machine learning", "model", "dataset", "feature", "prediction", "training", "accuracy"],
            "electronics": ["circuit", "voltage", "current", "resistor", "transistor", "signal", "digital", "analog"],
            "general": ["experience", "project", "team", "problem", "solution", "skill"]
        }
        return keywords.get(domain, keywords["general"])
    
    def _get_improvement_suggestions(self, domain: str, score: float) -> List[str]:
        """Get improvement suggestions based on score"""
        if score >= 0.7:
            return [
                "Great job! Continue practicing to maintain consistency.",
                "Try to add more real-world examples to your answers."
            ]
        elif score >= 0.5:
            return [
                "Review fundamental concepts in your domain.",
                "Practice explaining technical concepts in simple terms.",
                "Prepare specific examples from your experience."
            ]
        else:
            return [
                "Focus on understanding core concepts in your domain.",
                "Practice answering questions out loud.",
                "Study common interview questions for your field.",
                "Work on structuring your answers clearly."
            ]

