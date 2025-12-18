from sentence_transformers import SentenceTransformer

# Lightweight, fast, production-safe
_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> list[list[float]]:
    """
    Convert multiple texts into embeddings
    """
    return _model.encode(texts, convert_to_numpy=True).tolist()

def embed_query(text: str) -> list[float]:
    """
    Convert a single query into an embedding
    """
    return _model.encode(text, convert_to_numpy=True).tolist()
