# Quick Start Guide

## 🚀 Fast Setup (5 minutes)

> **For detailed step-by-step instructions, see [START_GUIDE.md](START_GUIDE.md)**

### Step 1: Install Prerequisites

**Python & Node.js:**
- Install Python 3.9+ from [python.org](https://www.python.org/downloads/)
- Install Node.js 18+ from [nodejs.org](https://nodejs.org/)

**FFmpeg (for audio processing):**
- **Windows:** `choco install ffmpeg` or download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

### Step 2: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data (first time only)
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### Step 3: Frontend Setup

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install
```

### Step 4: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Step 5: Open in Browser

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 🎯 First Interview Session

1. **Select Domain:** Choose Software, Data Science, Electronics, or General
2. **Choose Level:** Fresher, Intermediate, or Senior
3. **Start Recording:** Click "Start Recording" and speak your answer
4. **Get Feedback:** View instant feedback on communication and technical skills
5. **Continue:** Answer more questions (up to 5 per session)
6. **View Report:** Get personalized improvement report at the end

## 📝 Notes

- **First Run:** Whisper model (~150MB) will download automatically on first use
- **Microphone:** Grant browser permission for microphone access
- **Browser:** Chrome or Firefox recommended for best audio support
- **No API Keys Needed:** Everything runs locally using free/open-source models

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (need 3.9+)
- Ensure dependencies installed: `pip install -r requirements.txt`

**Frontend won't start:**
- Check Node version: `node --version` (need 18+)
- Clear cache: `rm -rf node_modules package-lock.json && npm install`

**Audio not recording:**
- Check browser permissions (Settings > Privacy > Microphone)
- Try different browser (Chrome/Firefox)
- Check microphone is working in other apps

**Whisper model download fails:**
- Check internet connection
- Models are cached after first download
- Try smaller model: Edit `backend/services/audio_service.py`, change `model_size="tiny"`

## 🎓 Next Steps

- Practice regularly to improve scores
- Review improvement plans in reports
- Try different domains to broaden skills
- Focus on reducing filler words for better communication scores

Happy interviewing! 🎤✨

