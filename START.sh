#!/bin/bash

echo "========================================"
echo "AI Interview Coach - Quick Start"
echo "========================================"
echo ""
echo "Starting Backend Server..."
cd backend
python3 -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

sleep 3

echo ""
echo "Starting Frontend Server..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "Both servers are starting!"
echo ""
echo "Backend: http://127.0.0.1:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "========================================"
echo ""

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait

