import streamlit as st

# Page setup
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Agents list
agents = ["Agent 1", "Agent 2"]

# Store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- INPUT SECTION ----------
with st.form(key="chat_form", clear_on_submit=True):

    col1, col2, col3 = st.columns([2, 6, 1])

    with col1:
        agent = st.selectbox(
            "Agent",
            agents,
            label_visibility="collapsed"
        )

    with col2:
        user_input = st.text_input(
            "Message",
            placeholder="Type message...",
            label_visibility="collapsed"
        )

    with col3:
        send = st.form_submit_button("Send")

    if send and user_input.strip():
        st.session_state.messages.append({
            "role": "You",
            "text": user_input
        })

        st.session_state.messages.append({
            "role": agent,
            "text": "Reply from agent"
        })

# ---------- CHAT DISPLAY ----------
# st.markdown("""
# <style>
# .chat-box {
#     height: 600px;
#     border: 1px solid #444;
#     border-radius: 10px;
#     padding: 20px;
#     overflow-y: auto;
#     background: #0e1117;
#     margin-top: 20px;
# }
# .message {
#     margin-bottom: 10px;
# }
# </style>
# """, unsafe_allow_html=True)

st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    st.markdown(
        f"<div class='message'><b>{msg['role']}:</b> {msg['text']}</div>",
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)
