"""
Chat service - orchestrates the entire chat workflow with conversation history
"""
from .vector_store import search_similar_documents
from .llm_chain import get_conversational_chain
from .database import save_message

def format_conversation_history(conversation_list, max_messages=10):
    """
    Format conversation history for the LLM prompt
    
    Args:
        conversation_list (list): List of conversation messages
        max_messages (int): Maximum number of recent messages to include
    
    Returns:
        str: Formatted conversation history
    """
    if not conversation_list:
        return "No previous conversation."
    
    # Get last N messages (N*2 because each exchange has user + assistant)
    recent_messages = conversation_list[-(max_messages * 2):] if len(conversation_list) > max_messages * 2 else conversation_list
    
    formatted = []
    for msg in recent_messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        formatted.append(f"{role}: {msg['content']}")
    
    return "\n".join(formatted)

def process_user_question(user_question, conversation_history=None, max_history=5):
    """
    Process a user question and return the AI response with conversation context
    
    Args:
        user_question (str): User's question
        conversation_history (list, optional): List of previous conversation messages from session state
        max_history (int): Number of previous exchanges to include (default: 5)
    
    Returns:
        str: AI assistant's response
    
    Raises:
        Exception: If vector store is not initialized or other errors occur
    """
    # Search for similar documents
    docs = search_similar_documents(user_question)
    
    # Format conversation history using the helper function
    history_text = format_conversation_history(
        conversation_history if conversation_history else [], 
        max_messages=max_history
    )

    # Get conversational chain
    chain = get_conversational_chain()
    
    # Generate response with conversation history
    response = chain.invoke(
        {
            "input_documents": docs,
            "conversation_history": history_text,
            "question": user_question
        },
        return_only_outputs=True
    )
    
    answer = response["output_text"]
    
    # Save conversation to database
    save_message("user", user_question)
    save_message("assistant", answer)
    
    return answer

def process_documents(pdf_files=None, text_input=None):
    """
    Process documents (PDFs and/or text) and create vector store
    
    Args:
        pdf_files: List of PDF file objects (optional)
        text_input (str): Additional text input (optional)
    
    Returns:
        dict: Status information with 'success', 'warning', 'error' keys
    """
    from .pdf_loader import extract_text_from_pdfs, validate_extracted_text
    from .text_splitter import split_text_into_chunks
    from .vector_store import create_vector_store
    
    result = {
        "success": False,
        "warning": None,
        "error": None
    }
    
    raw_text = ""
    
    # Process PDFs
    if pdf_files:
        pdf_text, skipped_files = extract_text_from_pdfs(pdf_files)
        validation = validate_extracted_text(pdf_text, skipped_files)
        
        if validation["warning"]:
            result["warning"] = validation["warning"]
        
        if validation["error"] and not text_input:
            result["error"] = validation["error"]
            return result
        
        raw_text += pdf_text
    
    # Add text input
    if text_input:
        raw_text += "\n" + text_input
    
    # Validate we have some text
    if not raw_text.strip():
        result["error"] = "Please provide either PDF files or text input."
        return result
    
    # Create chunks and vector store
    text_chunks = split_text_into_chunks(raw_text)
    create_vector_store(text_chunks)
    
    result["success"] = True
    return result