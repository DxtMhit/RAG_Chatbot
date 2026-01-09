"""
FAISS vector store operations
"""
import os
from langchain_community.vectorstores import FAISS
from .embeddings import get_embeddings
from .config import FAISS_INDEX_PATH

def create_vector_store(text_chunks):
    """
    Create and save FAISS vector store from text chunks
    
    Args:
        text_chunks (list): List of text chunks to embed
    """
    # Ensure storage directory exists
    os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
    
    embeddings = get_embeddings()
    
    vector_store = FAISS.from_texts(
        text_chunks,
        embedding=embeddings
    )
    
    vector_store.save_local(FAISS_INDEX_PATH)

def load_vector_store():
    """
    Load existing FAISS vector store
    
    Returns:
        FAISS: Loaded vector store
    
    Raises:
        Exception: If vector store cannot be loaded
    """
    embeddings = get_embeddings()
    
    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(
            "FAISS index not found. Please upload and process PDFs first."
        )
    
    vector_store = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    
    return vector_store

def search_similar_documents(query, k=4):
    """
    Search for similar documents in the vector store
    
    Args:
        query (str): Query text
        k (int): Number of similar documents to return
    
    Returns:
        list: List of similar documents
    """
    vector_store = load_vector_store()
    docs = vector_store.similarity_search(query, k=k)
    return docs