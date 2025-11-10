"""
AI Interview Coach - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import json
import logging

from services.audio_service import AudioService
from services.llm_service import LLMService
from services.analysis_service import AnalysisService
from services.report_service import ReportService
from models.schemas import InterviewSession, FeedbackRequest, ReportRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Interview Coach API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
audio_service = AudioService()
llm_service = LLMService()
analysis_service = AnalysisService()
report_service = ReportService()

# Active WebSocket connections
active_connections: List[WebSocket] = []


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Interview Coach API", "status": "running"}


@app.get("/api/domains")
async def get_domains():
    """Get available interview domains"""
    domains = [
        {"id": "software", "name": "Software Engineering", "description": "Coding, algorithms, system design"},
        {"id": "data_science", "name": "Data Science", "description": "ML, statistics, data analysis"},
        {"id": "electronics", "name": "Electronics", "description": "Circuit design, embedded systems"},
        {"id": "general", "name": "General", "description": "Behavioral and general questions"},
    ]
    return {"domains": domains}


@app.post("/api/interview/start")
async def start_interview(domain: str, experience_level: str = "fresher"):
    """Start a new interview session"""
    try:
        # Generate initial question based on domain
        question = await llm_service.generate_question(domain, experience_level)
        
        session = InterviewSession(
            domain=domain,
            experience_level=experience_level,
            current_question=question,
            questions_asked=1
        )
        
        return {
            "session_id": session.session_id,
            "question": question,
            "domain": domain
        }
    except Exception as e:
        logger.error(f"Error starting interview: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/interview/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """Transcribe audio to text using Whisper"""
    try:
        # Save uploaded audio temporarily
        audio_path = f"temp_{audio_file.filename}"
        with open(audio_path, "wb") as f:
            content = await audio_file.read()
            f.write(content)
        
        # Transcribe
        transcript = await audio_service.transcribe_audio(audio_path)
        
        # Clean up
        import os
        os.remove(audio_path)
        
        return {"transcript": transcript}
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/interview/evaluate")
async def evaluate_response(request: FeedbackRequest):
    """Evaluate candidate response and provide feedback"""
    try:
        # Analyze communication skills
        comm_analysis = await analysis_service.analyze_communication(
            request.transcript
        )
        
        # Evaluate technical correctness
        tech_analysis = await llm_service.evaluate_response(
            question=request.question,
            answer=request.transcript,
            domain=request.domain
        )
        
        # Combine feedback
        feedback = {
            "communication": comm_analysis,
            "technical": tech_analysis,
            "overall_score": (comm_analysis["score"] + tech_analysis["score"]) / 2
        }
        
        return feedback
    except Exception as e:
        logger.error(f"Error evaluating response: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/interview/next-question")
async def get_next_question(domain: str, experience_level: str, previous_answers: List[str]):
    """Generate next interview question based on previous answers"""
    try:
        question = await llm_service.generate_followup_question(
            domain=domain,
            experience_level=experience_level,
            previous_answers=previous_answers
        )
        return {"question": question}
    except Exception as e:
        logger.error(f"Error generating next question: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.post("/api/report/generate")
async def generate_report(request: ReportRequest):
    """Generate personalized improvement report"""
    try:
        report = await report_service.generate_report(
            session_data=request.session_data,
            domain=request.domain
        )
        return report
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


@app.websocket("/ws/interview")
async def websocket_interview(websocket: WebSocket):
    """WebSocket endpoint for real-time interview sessions"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "audio_chunk":
                # Process audio chunk in real-time
                transcript = await audio_service.transcribe_audio_chunk(
                    data["audio_data"]
                )
                await websocket.send_json({
                    "type": "transcript",
                    "text": transcript
                })
            
            elif data["type"] == "evaluate":
                # Real-time evaluation
                feedback = await analysis_service.analyze_communication(
                    data["transcript"]
                )
                await websocket.send_json({
                    "type": "feedback",
                    "data": feedback
                })
    
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        logger.info("WebSocket disconnected")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

