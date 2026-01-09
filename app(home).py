import streamlit as st

# Page config
st.set_page_config(
    page_title="Agent Chat App",
    layout="wide"
)

# Title
st.title("My App")
st.write("")  # space

# Main container
with st.container():
    st.markdown(
        """
        <div style="
            border: 2px solid #cccccc;
            padding: 30px;
            border-radius: 15px;
            ">
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    
    # AGENT CARD (CLICKABLE)
    with col1:
        if st.button("👤 Agent", use_container_width=True):
            st.switch_page("pages/agents.py")
    
    # CHAT CARD (CLICKABLE)
    with col2:
        if st.button("💬 Chat", use_container_width=True):
            st.switch_page("pages/chat.py")
    
    st.markdown("</div>", unsafe_allow_html=True)