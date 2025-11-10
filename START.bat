@echo off
echo ========================================
echo AI Interview Coach - Quick Start
echo ========================================
echo.
echo This will start both backend and frontend servers.
echo Make sure you have:
echo   - Python 3.9+ installed
echo   - Node.js 18+ installed
echo   - All dependencies installed (run setup first)
echo.
pause

echo.
echo Starting Backend Server...
echo.
start "Backend Server" cmd /k "cd /d %~dp0backend && python -m uvicorn main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo.
echo Starting Frontend Server...
echo.
start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo ========================================
echo Both servers are starting!
echo.
echo Backend: http://127.0.0.1:8000
echo Frontend: http://localhost:3000
echo.
echo The browser should open automatically.
echo Close the server windows to stop the servers.
echo ========================================
echo.
pause

