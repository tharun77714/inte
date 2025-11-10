# Step-by-Step Startup Guide

Follow these steps to start the AI Interview Coach application.

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.9+ installed
- ✅ Node.js 18+ installed
- ✅ All dependencies installed (see below if not)

## Step 1: Verify Backend Dependencies

Open PowerShell and navigate to the project:

```powershell
cd C:\Users\Kotha\OneDrive\Desktop\interview\backend
```

Check if dependencies are installed:

```powershell
python -c "import fastapi, whisper, transformers, nltk, textstat, sentence_transformers; print('All packages installed!')"
```

If you get an error, install missing packages:

```powershell
pip install -r requirements.txt
```

## Step 2: Verify NLTK Data

Check if NLTK data is downloaded:

```powershell
python -c "import nltk; nltk.data.find('tokenizers/punkt'); nltk.data.find('taggers/averaged_perceptron_tagger'); print('NLTK data found!')"
```

If you get an error, download NLTK data:

```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

## Step 3: Verify Frontend Dependencies

Open a NEW PowerShell window and navigate to frontend:

```powershell
cd C:\Users\Kotha\OneDrive\Desktop\interview\frontend
```

Check if node_modules exists:

```powershell
Test-Path node_modules
```

If it returns `False`, install dependencies:

```powershell
npm install
```

## Step 4: Start Backend Server

In your FIRST PowerShell window (backend directory):

```powershell
cd C:\Users\Kotha\OneDrive\Desktop\interview\backend
python -m uvicorn main:app --reload --port 8000
```

**What to expect:**
- You'll see "Uvicorn running on http://127.0.0.1:8000"
- Models will start loading in the background
- Wait for "All models loaded successfully!" message
- Keep this window open!

**First time loading models:**
- Whisper model downloads (~150MB) - takes 1-2 minutes
- GPT-2 downloads (~500MB) - takes 2-3 minutes  
- Sentence Transformer downloads (~90MB) - takes 1 minute
- Total: ~5-10 minutes on first run

## Step 5: Start Frontend Server

In your SECOND PowerShell window (frontend directory):

```powershell
cd C:\Users\Kotha\OneDrive\Desktop\interview\frontend
npm start
```

**What to expect:**
- Browser should automatically open to `http://localhost:3000`
- If not, manually open: `http://localhost:3000`
- First compile takes 1-2 minutes
- Keep this window open!

## Step 6: Verify Everything is Working

### Check Backend:
Open browser and go to: `http://127.0.0.1:8000`

You should see:
```json
{"message":"AI Interview Coach API","status":"running"}
```

### Check Frontend:
Open browser and go to: `http://localhost:3000`

You should see:
- "AI Interview Coach" title
- Domain selection screen
- "Select Your Interview Domain" heading

## Step 7: Start Your First Interview!

1. **Select Domain:** Choose Software, Data Science, Electronics, or General
2. **Choose Experience Level:** Fresher, Intermediate, or Senior
3. **Click on a Domain Card** to start
4. **Read the Question** displayed
5. **Click "Start Recording"** and speak your answer
6. **Click "Stop Recording"** when done
7. **View Feedback** - see your communication and technical scores
8. **Continue** with more questions or end session to see report

## Troubleshooting

### Backend won't start:
- Check Python version: `python --version` (need 3.9+)
- Install dependencies: `pip install -r requirements.txt`
- Check port 8000 is free: `netstat -ano | findstr :8000`

### Frontend won't start:
- Check Node version: `node --version` (need 18+)
- Install dependencies: `npm install`
- Check port 3000 is free: `netstat -ano | findstr :3000`

### Models not loading:
- Check internet connection (needed for first-time download)
- Wait 5-10 minutes for first-time model downloads
- Check disk space (need ~2GB free)

### Audio not recording:
- Grant microphone permissions in browser
- Try Chrome or Firefox (best WebRTC support)
- Check microphone works in other apps

### CORS errors:
- Ensure backend is running on port 8000
- Ensure frontend is running on port 3000
- Check browser console for specific errors

## Quick Start Commands (Copy-Paste)

### Terminal 1 - Backend:
```powershell
cd C:\Users\Kotha\OneDrive\Desktop\interview\backend
python -m uvicorn main:app --reload --port 8000
```

### Terminal 2 - Frontend:
```powershell
cd C:\Users\Kotha\OneDrive\Desktop\interview\frontend
npm start
```

## Stopping the Servers

- **Backend:** Press `Ctrl+C` in the backend PowerShell window
- **Frontend:** Press `Ctrl+C` in the frontend PowerShell window

## Next Steps After Starting

1. ✅ Both servers running
2. ✅ Browser open to `http://localhost:3000`
3. ✅ Select a domain and start practicing!
4. ✅ Review your feedback and improvement reports

Happy interviewing! 🎤✨

