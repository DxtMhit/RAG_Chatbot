import streamlit as st

# Page config
st.set_page_config(
    page_title="Content Page",
    layout="wide"
)

# Get selected agent
selected_agent = st.session_state.get("selected_agent")

# Safety check
if not selected_agent:
    st.warning("No agent selected")
    if st.button("⬅ Go back to Agents"):
        st.switch_page("pages/page2.py")
    st.stop()

# Page title
st.title(f"Content for {selected_agent}")

st.write("---")

# Main container
with st.container():
    st.markdown(
        """
        <div style="
            border: 2px solid #cccccc;
            padding: 20px;
            border-radius: 12px;
            ">
        """,
        unsafe_allow_html=True
    )

    # File upload section
    st.subheader("Upload Files")
    uploaded_files = st.file_uploader(
        "Upload PDFs / Docs / Text files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    st.write("")

    # Paragraph input
    st.subheader("Add Paragraph")
    paragraph = st.text_area(
        "Enter your paragraph here",
        height=150
    )

    st.write("")

    # Submit button
    if st.button("Submit & Save"):
        st.success(f"Content saved for {selected_agent}")

        # For now just showing data
        if uploaded_files:
            st.write("Files uploaded:", len(uploaded_files))
        if paragraph:
            st.write("Paragraph received")

    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

# Back button
if st.button("⬅ Back to Agents"):
    st.switch_page("pages/page2.py")
