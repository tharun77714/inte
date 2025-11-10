"""
Audio processing service using Whisper for speech-to-text
"""

import whisper
import logging
import os
import numpy as np
from typing import Optional, Tuple, List
import asyncio
from io import BytesIO
import base64

logger = logging.getLogger(__name__)


class AudioService:
    """Service for audio transcription using OpenAI Whisper"""
    
    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper model
        
        Args:
            model_size: Model size (tiny, base, small, medium, large)
                       'base' is recommended for balance of speed/accuracy
        """
        self.model_size = model_size
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load Whisper model (lazy loading)"""
        try:
            logger.info(f"Loading Whisper model: {self.model_size}")
            self.model = whisper.load_model(self.model_size)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading Whisper model: {e}")
            raise
    
    async def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            language: Optional language code (e.g., 'en')
        
        Returns:
            Transcribed text
        """
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._transcribe_sync,
                audio_path,
                language
            )
            return result["text"].strip()
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise
    
    def _transcribe_sync(self, audio_path: str, language: Optional[str] = None) -> dict:
        """Synchronous transcription (runs in thread pool)"""
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        result = self.model.transcribe(
            audio_path,
            language=language,
            task="transcribe",
            fp16=False  # Use FP32 for compatibility
        )
        return result
    
    async def transcribe_audio_chunk(self, audio_data: str) -> str:
        """
        Transcribe audio chunk from base64 encoded data
        
        Args:
            audio_data: Base64 encoded audio data
        
        Returns:
            Transcribed text
        """
        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_data)
            
            # Save to temporary file
            temp_path = f"temp_chunk_{hash(audio_data)}.wav"
            with open(temp_path, "wb") as f:
                f.write(audio_bytes)
            
            # Transcribe
            transcript = await self.transcribe_audio(temp_path)
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return transcript
        except Exception as e:
            logger.error(f"Error transcribing audio chunk: {e}")
            return ""
    
    def detect_filler_words(self, text: str) -> Tuple[List[str], int]:
        """
        Detect filler words in transcribed text
        
        Args:
            text: Transcribed text
        
        Returns:
            Tuple of (list of filler words found, count)
        """
        filler_words = [
            "um", "uh", "er", "ah", "like", "you know", "so", "well",
            "actually", "basically", "literally", "right", "okay", "ok"
        ]
        
        text_lower = text.lower()
        found_fillers = []
        
        for filler in filler_words:
            if filler in text_lower:
                # Count occurrences
                count = text_lower.count(filler)
                found_fillers.extend([filler] * count)
        
        return found_fillers, len(found_fillers)

