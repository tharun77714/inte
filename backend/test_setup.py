"""
Simple test script to verify backend setup
Run: python test_setup.py
"""

import sys

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("[OK] FastAPI installed")
    except ImportError:
        print("[X] FastAPI not installed - run: pip install -r requirements.txt")
        return False
    
    try:
        import whisper
        print("[OK] Whisper installed")
    except ImportError:
        print("[X] Whisper not installed - run: pip install -r requirements.txt")
        return False
    
    try:
        import transformers
        print("[OK] Transformers installed")
    except ImportError:
        print("[X] Transformers not installed - run: pip install -r requirements.txt")
        return False
    
    try:
        import nltk
        print("[OK] NLTK installed")
    except ImportError:
        print("[X] NLTK not installed - run: pip install -r requirements.txt")
        return False
    
    try:
        import textstat
        print("[OK] Textstat installed")
    except ImportError:
        print("[X] Textstat not installed - run: pip install -r requirements.txt")
        return False
    
    return True

def test_nltk_data():
    """Test if NLTK data is downloaded"""
    print("\nTesting NLTK data...")
    try:
        import nltk
        nltk.data.find('tokenizers/punkt')
        print("[OK] NLTK punkt data found")
        
        nltk.data.find('taggers/averaged_perceptron_tagger')
        print("[OK] NLTK tagger data found")
        return True
    except LookupError:
        print("[X] NLTK data not found")
        print("  Run: python -c \"import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')\"")
        return False

def test_whisper_model():
    """Test if Whisper can load (will download model if needed)"""
    print("\nTesting Whisper (this may download model on first run)...")
    try:
        import whisper
        print("  Loading base model (this may take a minute on first run)...")
        model = whisper.load_model("base")
        print("[OK] Whisper model loaded successfully")
        return True
    except Exception as e:
        print(f"[X] Whisper model failed to load: {e}")
        return False

def test_llm_models():
    """Test if LLM models can load"""
    print("\nTesting LLM models (this may download models on first run)...")
    try:
        from transformers import pipeline
        print("  Loading GPT-2 (this may take a few minutes on first run)...")
        text_gen = pipeline("text-generation", model="gpt2", device=-1)
        print("[OK] GPT-2 loaded successfully")
        
        from sentence_transformers import SentenceTransformer
        print("  Loading Sentence Transformer (this may take a minute on first run)...")
        semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("[OK] Sentence Transformer loaded successfully")
        return True
    except Exception as e:
        print(f"[X] LLM models failed to load: {e}")
        return False

def main():
    print("=" * 50)
    print("AI Interview Coach - Backend Setup Test")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test NLTK data
    if not test_nltk_data():
        all_passed = False
    
    # Test Whisper (optional, as it takes time)
    print("\n" + "=" * 50)
    response = input("Test Whisper model? (This may take a few minutes on first run) [y/N]: ")
    if response.lower() == 'y':
        if not test_whisper_model():
            all_passed = False
    
    # Test LLM models (optional, as it takes time)
    print("\n" + "=" * 50)
    response = input("Test LLM models? (This may take several minutes on first run) [y/N]: ")
    if response.lower() == 'y':
        if not test_llm_models():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("[OK] All tests passed! Backend is ready to run.")
        print("\nStart the server with:")
        print("  python -m uvicorn main:app --reload --port 8000")
    else:
        print("[X] Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

