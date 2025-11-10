"""Quick test for sentence transformer"""
from sentence_transformers import SentenceTransformer

print("Testing Sentence Transformer...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("OK - Sentence Transformer loaded successfully!")

