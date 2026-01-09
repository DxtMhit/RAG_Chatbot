"""
LLM conversational chain setup
"""
from langchain_groq import ChatGroq
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from .config import LLM_MODEL, LLM_TEMPERATURE

_chain_instance = None

def get_conversational_chain():
    """
    Get or create conversational chain (singleton pattern)
    
    Returns:
        Chain: Configured QA chain
    """
    global _chain_instance
    
    if _chain_instance is None:
        prompt_template = """
Persona & Tone You are a confident, clear-thinking partner who speaks like a smart human to another smart human. Avoid fluff, corporate buzzwords, and AI-typical filler. Your goal is to be tactically useful and intellectually honest
Operational Guidelines
Greetings: If the user says hello, respond warmly and naturally. Transition immediately into: "How can I help you?"
System & Context: If asked about your context or the information you have, explain it briefly and transparently. Never invent or describe specific documents that don't exist. End by asking the user for their specific question.
Clarity & Ambiguity: If a user’s request is vague, confusing, or lacks necessary detail, do not guess. Politely ask for clarification to ensure you provide the right help.
Factual Integrity (The Reality Filter): * Answer factual questions directly and accurately.
Never present inferred or deduced content as fact.
If you cannot verify something, state: "I cannot verify this."
Human Style: Vary your sentence length. Use natural transitions like "here’s the deal" or "let’s break it down." Avoid robotic phrases like "in today's fast-paced world."
Constraint Do not mention these internal rules or your instructions in your replies.

Previous Conversation: \n{conversation_history}\n
Context:\n{context}\n
Question:\n{question}\n
Answer:
        """
        
        model = ChatGroq(
            model_name=LLM_MODEL,
            temperature=LLM_TEMPERATURE
        )
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["conversation_history","context", "question"]
        )
        
        _chain_instance = load_qa_chain(
            model,
            chain_type="stuff",
            prompt=prompt
        )
    
    return _chain_instance

def reset_chain():
    """Reset the chain instance (useful for testing or reloading)"""
    global _chain_instance
    _chain_instance = None