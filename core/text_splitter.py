"""
Text chunking functionality
"""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import CHUNK_SIZE, CHUNK_OVERLAP

def split_text_into_chunks(text):
    """
    Split text into smaller chunks for embedding
    
    Args:
        text (str): Raw text to split
    
    Returns:
        list: List of text chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    
    chunks = text_splitter.split_text(text)
    return chunks