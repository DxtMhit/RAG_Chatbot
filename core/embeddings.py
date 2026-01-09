"""
Embedding model handling
"""
from langchain_huggingface import HuggingFaceEmbeddings
from .config import EMBEDDING_MODEL

_embeddings_instance = None

def get_embeddings():
    """
    Get or create embeddings model instance (singleton pattern)
    
    Returns:
        HuggingFaceEmbeddings: Embeddings model
    """
    global _embeddings_instance
    
    if _embeddings_instance is None:
        _embeddings_instance = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL
        )
    
    return _embeddings_instance