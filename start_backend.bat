@echo off
echo Starting AI Interview Coach Backend...
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause

