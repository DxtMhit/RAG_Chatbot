"""
Multi-PDF Chat Application - Streamlit UI with Conversation Memory
"""
import streamlit as st
from core import validate_env, process_user_question, process_documents

def initialize_session_state():
    """Initialize session state variables"""
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "max_history" not in st.session_state:
        st.session_state.max_history = 5  # Default: remember last 5 exchanges

def display_conversation():
    """Display the conversation history"""
    for message in st.session_state.conversation:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.write(f"🧑 **You:** {content}")
        else:
            st.write(f"🤖 **Assistant:** {content}")

def handle_user_question(user_question):
    """Handle user question submission with conversation history"""
    if not user_question:
        st.warning("Please enter a question.")
        return
    
    try:
        with st.spinner("Thinking..."):
            # Pass conversation history to the chat service
            answer = process_user_question(
                user_question, 
                conversation_history=st.session_state.conversation,
                max_history=st.session_state.max_history
            )
        
        # Update session state
        st.session_state.conversation.append({
            "role": "user",
            "content": user_question
        })
        
        st.session_state.conversation.append({
            "role": "assistant",
            "content": answer
        })
        
        # Show success message without displaying conversation here
        st.success("Response generated!")
        return answer
        
    except FileNotFoundError:
        st.error("⚠️ Please upload and process PDFs first before asking questions.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def handle_document_processing(pdf_docs, para):
    """Handle document upload and processing"""
    if not pdf_docs and not para:
        st.warning("Please provide either PDF files or text input.")
        return
    
    with st.spinner("Processing documents..."):
        result = process_documents(pdf_files=pdf_docs, text_input=para)
    
    if result["warning"]:
        st.warning(result["warning"])
    
    if result["error"]:
        st.error(result["error"])
        return
    
    if result["success"]:
        st.success("✅ Documents processed successfully! You can now ask questions.")

def main():
    """Main application entry point"""
    # Page configuration
    st.set_page_config(
        page_title="Multi PDF Chatbot",
        page_icon="📚",
        layout="wide"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Validate environment
    try:
        validate_env()
    except ValueError as e:
        st.error(str(e))
        st.stop()
    
    # Header
    st.header("Multi-PDF's 📚 - Chat Agent 🤖")
    st.markdown("Upload your PDFs and ask questions about their content!")
    
    # Main chat interface
    st.subheader("💬 Chat Interface")
    
    user_question = st.text_input(
        "Ask your question",
        placeholder="What would you like to know?",
        key="user_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 4])
    answer = ""
    with col1:
        if st.button("🚀 Submit", use_container_width=True):
            answer = handle_user_question(user_question)
    
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.conversation = []
            st.rerun()

    st.write(answer)
    # Display conversation history
    if st.session_state.conversation:
        st.divider()
        st.subheader("📜 Conversation History")
        
        # Show memory info
        total_exchanges = len(st.session_state.conversation) // 2
        st.caption(f"💭 Model remembers last {st.session_state.max_history} exchanges | Total: {total_exchanges} exchanges")
        
        display_conversation()
    
    # Sidebar for document upload and settings
    with st.sidebar:
        st.title("📁 Document Management")
        st.write("---")
        
        # PDF Upload Section
        st.subheader("📄 Upload PDFs")
        pdf_docs = st.file_uploader(
            "Choose PDF files",
            accept_multiple_files=True,
            type=['pdf'],
            help="Upload one or more PDF files to chat with"
        )
        
        # Text Input Section
        st.subheader("✍️ Additional Text")
        para = st.text_area(
            "Enter any additional text",
            placeholder="Add extra context or information...",
            height=150
        )
        
        # Process Button
        if st.button("⚡ Submit & Process", use_container_width=True):
            handle_document_processing(pdf_docs, para)
        
        st.write("---")
        
        # Memory Settings
        st.subheader("🧠 Memory Settings")
        st.session_state.max_history = st.slider(
            "Conversation history length",
            min_value=1,
            max_value=20,
            value=st.session_state.max_history,
            help="Number of previous exchanges the model will remember"
        )
        
        st.caption(f"Model will remember last {st.session_state.max_history} exchanges (user + assistant messages)")
        
        st.write("---")
        
        # Additional Info
        with st.expander("ℹ️ How to use"):
            st.markdown("""
            1. **Upload PDFs** or **enter text** in the sidebar
            2. Click **Submit & Process** to index your documents
            3. Ask questions in the main chat interface
            4. The model remembers your conversation history
            5. Adjust memory length with the slider
            6. Click **Clear Chat** to start fresh
            """)
        
        with st.expander("🧠 About Conversation Memory"):
            st.markdown("""
            The chatbot now remembers your previous messages!
            
            **How it works:**
            - Previous conversations are sent with each question
            - You can reference earlier topics naturally
            - The model maintains context across messages
            - Adjust the memory slider to control how much history is kept
            
            **Example:**
            - You: "What is the revenue for Q3?"
            - Bot: "The Q3 revenue was $5M"
            - You: "What about Q4?" ← Bot knows you're asking about revenue
            - Bot: "The Q4 revenue was $6M"
            """)
        
        with st.expander("⚙️ About"):
            st.markdown("""
            This application uses:
            - **LangChain** for document processing
            - **FAISS** for vector storage
            - **HuggingFace** embeddings
            - **Groq** LLM for responses
            - **Conversation Memory** for context
            """)

if __name__ == "__main__":
    main()
