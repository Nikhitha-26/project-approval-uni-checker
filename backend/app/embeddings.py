from sentence_transformers import SentenceTransformer
from typing import List

# Load model once at module level
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str) -> List[float]:
    """
    Generate a 384-dim embedding for the given text using Sentence-BERT.
    """
    embedding = model.encode(text, show_progress_bar=False, normalize_embeddings=True)
    return embedding.tolist()
