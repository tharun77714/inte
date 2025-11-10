"""
Pydantic models for request/response schemas
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


class InterviewSession(BaseModel):
    session_id: str = str(uuid.uuid4())
    domain: str
    experience_level: str = "fresher"
    current_question: str
    questions_asked: int = 0
    answers: List[str] = []
    feedback_history: List[Dict[str, Any]] = []
    created_at: datetime = datetime.now()


class FeedbackRequest(BaseModel):
    question: str
    transcript: str
    domain: str
    session_id: Optional[str] = None


class ReportRequest(BaseModel):
    session_id: str
    session_data: Dict[str, Any]
    domain: str


class CommunicationAnalysis(BaseModel):
    score: float
    filler_words_count: int
    filler_words: List[str]
    clarity_score: float
    grammar_score: float
    tone_score: float
    suggestions: List[str]


class TechnicalAnalysis(BaseModel):
    score: float
    correctness: float
    completeness: float
    relevance: float
    feedback: str
    suggestions: List[str]


class FeedbackResponse(BaseModel):
    communication: CommunicationAnalysis
    technical: TechnicalAnalysis
    overall_score: float
    timestamp: datetime = datetime.now()

