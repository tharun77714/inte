# AI Interview Coach - Self-Hosted

An AI-powered interview coaching system that simulates real interviews, provides instant feedback, and helps candidates improve technical and soft skills.

## Features

- 🎤 **Audio-First Interview Simulation** - Practice interviews with voice interaction
- 🤖 **AI-Powered Evaluation** - Instant feedback on communication, technical skills, and soft skills
- 📊 **Personalized Reports** - Detailed improvement reports after each session
- 🌐 **Multi-Domain Support** - Software, Data Science, Electronics, and more
- 🆓 **Free & Open-Source** - Uses free/open-source models and APIs
- 🏠 **Self-Hosted** - Run entirely on your own infrastructure

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Whisper** - Open-source speech-to-text (OpenAI)
- **Hugging Face Transformers** - Free LLM models (Llama, Mistral, etc.)
- **SQLite** - Lightweight database
- **WebSocket** - Real-time communication

### Frontend
- **React** - UI framework
- **Web Audio API** - Audio recording
- **Tailwind CSS** - Styling

## Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- FFmpeg (for audio processing)

### Installation

1. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

2. **Frontend Setup**
```bash
cd frontend
npm install
npm start
```

3. **Download Whisper Model** (first run will auto-download)
   - Model: `base` (recommended for balance of speed/accuracy)
   - Or use `small`, `medium` for better accuracy

## Usage

1. Start the backend server (default: http://localhost:8000)
2. Start the frontend (default: http://localhost:3000)
3. Select your domain (Software, Data Science, Electronics, etc.)
4. Start an interview session
5. Speak your answers - AI will transcribe and evaluate
6. Receive instant feedback and detailed reports

## Project Structure

```
interview/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models/              # Data models
│   ├── services/            # Business logic
│   │   ├── audio_service.py # Audio processing
│   │   ├── llm_service.py   # LLM integration
│   │   ├── analysis_service.py # Feedback analysis
│   │   └── report_service.py # Report generation
│   ├── utils/               # Utilities
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   └── App.js           # Main app
│   └── package.json
└── README.md
```

## Pretrained Models Used (All Free & Open-Source)

### 1. **Whisper (OpenAI)** - Speech-to-Text
- Model: `whisper-base` (~150MB)
- Converts audio recordings to text
- Auto-downloads on first use

### 2. **GPT-2 (Hugging Face)** - Question Generation
- Model: `gpt2` (~500MB)
- Generates dynamic interview questions
- Auto-downloads on first use

### 3. **Sentence Transformer** - Semantic Evaluation
- Model: `all-MiniLM-L6-v2` (~90MB)
- Evaluates answer quality using semantic similarity
- Auto-downloads on first use

### 4. **NLTK Models** - Text Processing
- Models: `punkt`, `averaged_perceptron_tagger` (~50MB)
- Tokenization and grammar analysis
- Auto-downloads on first use

**Total Model Size:** ~790MB (downloaded automatically)  
**All processing runs locally** - no external API costs or keys needed!

See [MODELS.md](MODELS.md) for detailed model documentation.

## License

MIT

