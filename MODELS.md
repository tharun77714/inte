# Pretrained Models Documentation

This document describes all pretrained models used in the AI Interview Coach system.

## Models Overview

The system uses **4 main pretrained models** for different tasks:

### 1. **Whisper (OpenAI)** - Speech-to-Text
- **Purpose:** Convert audio recordings to text
- **Model:** `whisper-base` (default)
- **Size:** ~150MB
- **Location:** Auto-downloaded on first use
- **Usage:** `backend/services/audio_service.py`
- **Alternatives:** `tiny` (39MB, faster), `small` (500MB, better), `medium` (1.5GB), `large` (3GB)

**Configuration:**
```python
# In backend/services/audio_service.py
self.model_size = "base"  # Change to desired size
```

### 2. **GPT-2 (Hugging Face)** - Text Generation
- **Purpose:** Generate interview questions dynamically
- **Model:** `gpt2` (small, 124M parameters)
- **Size:** ~500MB
- **Location:** Auto-downloaded from Hugging Face on first use
- **Usage:** `backend/services/llm_service.py`
- **Device:** CPU or CUDA (auto-detected)

**What it does:**
- Generates contextual interview questions based on domain and experience level
- Creates follow-up questions based on previous answers
- Falls back to templates if model not loaded

### 3. **Sentence Transformer (all-MiniLM-L6-v2)** - Semantic Analysis
- **Purpose:** Evaluate answer quality using semantic similarity
- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Size:** ~90MB
- **Location:** Auto-downloaded from Hugging Face on first use
- **Usage:** `backend/services/llm_service.py` for technical evaluation

**What it does:**
- Calculates semantic similarity between question and answer
- Compares answers against expected domain concepts
- Provides more accurate technical correctness scoring

### 4. **NLTK Models** - Text Processing
- **Purpose:** Tokenization, POS tagging for communication analysis
- **Models:** `punkt`, `averaged_perceptron_tagger`
- **Size:** ~50MB total
- **Location:** Auto-downloaded via NLTK on first use
- **Usage:** `backend/services/analysis_service.py`

**What it does:**
- Sentence tokenization for clarity analysis
- Part-of-speech tagging for grammar assessment
- Text structure analysis

## Model Loading Strategy

### Background Loading
All models load in **background threads** to avoid blocking server startup:
- Models start loading when service is initialized
- System falls back to templates if models aren't ready
- Models are cached after first download

### First Run Behavior
1. **Whisper:** Downloads model on first transcription request
2. **GPT-2:** Downloads on first question generation (if enabled)
3. **Sentence Transformer:** Downloads on first evaluation
4. **NLTK:** Downloads on first analysis

### Memory Requirements

**Minimum (CPU):**
- RAM: 4GB
- Disk: 1GB for all models

**Recommended:**
- RAM: 8GB+
- Disk: 2GB+ (for larger models)

**With GPU (CUDA):**
- VRAM: 2GB+ (for faster inference)
- Same RAM/disk as above

## Model Sizes Summary

| Model | Size | Download Time* | Load Time |
|-------|------|----------------|-----------|
| Whisper (base) | ~150MB | 1-2 min | 5-10 sec |
| GPT-2 | ~500MB | 3-5 min | 10-20 sec |
| Sentence Transformer | ~90MB | 1-2 min | 3-5 sec |
| NLTK Data | ~50MB | 30 sec | Instant |
| **Total** | **~790MB** | **5-10 min** | **20-35 sec** |

*Download time depends on internet speed

## Configuration

### Change Whisper Model Size
Edit `backend/services/audio_service.py`:
```python
def __init__(self, model_size: str = "base"):  # Change "base" to "tiny", "small", etc.
```

### Disable LLM Models (Use Templates Only)
Edit `backend/services/llm_service.py`:
```python
# Comment out model loading in _load_models_sync()
# System will automatically use templates
```

### Use GPU (CUDA)
Models automatically detect and use GPU if available. To force CPU:
```python
# In llm_service.py
self.device = "cpu"  # Force CPU
```

## Troubleshooting

### Models Not Downloading
- Check internet connection
- Verify Hugging Face access (no firewall blocking)
- Check disk space (need ~2GB free)

### Out of Memory Errors
- Use smaller Whisper model (`tiny` instead of `base`)
- Reduce batch sizes in model inference
- Close other applications

### Slow Model Loading
- First load is slow (downloading + loading)
- Subsequent loads are faster (models cached)
- Consider using smaller models for faster startup

### Model Download Fails
- Check Hugging Face status
- Try manual download: `python -c "from transformers import pipeline; pipeline('text-generation', model='gpt2')"`
- Use template fallback (works without models)

## Model Sources

- **Whisper:** [OpenAI GitHub](https://github.com/openai/whisper)
- **GPT-2:** [Hugging Face](https://huggingface.co/gpt2)
- **Sentence Transformer:** [Hugging Face](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- **NLTK:** [NLTK Data](https://www.nltk.org/data.html)

All models are **free and open-source** - no API keys required!

