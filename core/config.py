"""
Configuration and environment validation
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.1-8b-instant"
LLM_TEMPERATURE = 0.6
FAISS_INDEX_PATH = "storage/faiss_index"
DATABASE_PATH = "storage/chat_history.db"

# Conversation memory settings
DEFAULT_MAX_HISTORY = 5  # Default number of conversation exchanges to remember
MAX_HISTORY_LIMIT = 20   # Maximum allowed conversation history

def validate_env():
    """
    Validate that required environment variables are set.
    Raises an exception if validation fails.
    """
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY not found. Please set it in your .env file.")
    
def get_groq_api_key():
    """Get GROQ API key from environment"""
    return os.getenv("GROQ_API_KEY")