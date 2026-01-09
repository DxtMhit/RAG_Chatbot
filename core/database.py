"""
Database connection and message storage
"""
import sqlite3
import os
from .config import DATABASE_PATH

def get_db_connection():
    """Create and return a database connection"""
    # Ensure storage directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DATABASE_PATH)
    _initialize_database(conn)
    return conn

def _initialize_database(conn):
    """Create messages table if it doesn't exist"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

def save_message(role, content):
    """
    Save a message to the database
    
    Args:
        role (str): 'user' or 'assistant'
        content (str): message content
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO messages (role, content) VALUES (?, ?)",
        (role, content)
    )
    
    conn.commit()
    conn.close()

def get_conversation_history(limit=None):
    """
    Retrieve conversation history from database
    
    Args:
        limit (int, optional): Number of recent messages to retrieve
    
    Returns:
        list: List of message dictionaries
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT role, content, timestamp FROM messages ORDER BY timestamp DESC"
    if limit:
        query += f" LIMIT {limit}"
    
    cursor.execute(query)
    messages = [
        {"role": row[0], "content": row[1], "timestamp": row[2]}
        for row in cursor.fetchall()
    ]
    
    conn.close()
    return messages[::-1]  # Reverse to get chronological order

def clear_history():
    """Clear all messages from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()