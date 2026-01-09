import streamlit as st

st.set_page_config(page_title="Agents", layout="wide")
st.title("Agents")

# Initialize agents list
if "agents" not in st.session_state:
    st.session_state.agents = []

# -------- ADD AGENT POPUP --------
@st.dialog("Add New Agent")
def add_agent_popup():
    name = st.text_input("Agent Name")
    desc = st.text_area("Agent Description")

    if st.button("Save Agent"):
        if name.strip() == "":
            st.warning("Agent name is required")
        else:
            st.session_state.agents.append({
                "name": name,
                "desc": desc
            })
            st.success("Agent added")
            st.rerun()

# Add Agent button
if st.button("➕ Add Agent"):
    add_agent_popup()

st.write("---")

# -------- DISPLAY AGENTS --------
cols = st.columns(3)

for i, agent in enumerate(st.session_state.agents):
    with cols[i % 3]:

        st.markdown(f"### 👤 {agent['name']}")
        st.caption(agent["desc"])

        if st.button("Open", key=f"open_{i}"):
            st.session_state.selected_agent = agent
            st.switch_page("pages/page3.py")

        if st.button("❌ Remove", key=f"remove_{i}"):
            st.session_state.agents.pop(i)
            st.rerun()

st.write("---")

if st.button("⬅ Back to home"):
    st.switch_page("page1.py")
