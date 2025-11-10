# Setup Instructions

## Prerequisites

1. **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
2. **Node.js 18+** - [Download Node.js](https://nodejs.org/)
3. **FFmpeg** (for audio processing)
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `choco install ffmpeg`
   - Mac: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` or `sudo yum install ffmpeg`

## Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Download NLTK data (first time only):**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

5. **Start the backend server:**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

**Note:** First run will download Whisper model (~150MB for 'base' model). This happens automatically.

## Frontend Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the development server:**
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Usage

1. Open `http://localhost:3000` in your browser
2. Select your interview domain (Software, Data Science, Electronics, etc.)
3. Choose your experience level
4. Start recording your answers to interview questions
5. Receive instant feedback on communication and technical skills
6. View detailed improvement reports after each session

## Troubleshooting

### Audio Recording Issues
- Ensure microphone permissions are granted in your browser
- Try using Chrome or Firefox (best WebRTC support)
- Check that your microphone is working in other applications

### Whisper Model Download Issues
- Ensure you have internet connection for first-time model download
- Models are cached after first download
- If download fails, manually download from [Whisper GitHub](https://github.com/openai/whisper)

### Port Already in Use
- Backend: Change port in `uvicorn` command: `--port 8001`
- Frontend: Set `PORT=3001` in environment or edit `package.json`

### Memory Issues
- Use smaller Whisper model: Edit `backend/services/audio_service.py` and change `model_size="tiny"` or `model_size="small"`
- Close other applications to free up RAM

## Model Sizes (Whisper)

- `tiny` - ~39MB, fastest, lower accuracy
- `base` - ~150MB, balanced (recommended)
- `small` - ~500MB, better accuracy
- `medium` - ~1.5GB, high accuracy
- `large` - ~3GB, best accuracy

Change in `backend/services/audio_service.py`:
```python
self.model_size = "base"  # Change to desired size
```

