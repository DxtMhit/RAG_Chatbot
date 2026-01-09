import streamlit as st

st.set_page_config(
    page_title="Agents",
    layout="wide"
)

st.title("Agents")

# Initialize agents list
if "agents" not in st.session_state:
    st.session_state.agents = ["Agent 1", "Agent 2"]

# Add Agent button
if st.button("➕ Add Agent", key="add_agent"):
    st.session_state.agents.append(
        f"Agent {len(st.session_state.agents) + 1}"
    )

st.write("---")

# Display agents
cols = st.columns(4)

for i, agent in enumerate(st.session_state.agents):
    with cols[i % 4]:

        # Open agent
        if st.button(
            f"👤 {agent}",
            key=f"open_{i}",
            use_container_width=True
        ):
            st.session_state.selected_agent = agent
            st.switch_page("pages/page3.py")

        # Remove agent
        if st.button(
            "❌ Remove",
            key=f"remove_{i}"
        ):
            st.session_state.agents.pop(i)
            st.rerun()

st.write("---")

# ✅ Back button (ONLY ONCE)
if st.button("⬅ Back to home", key="back_home"):
    st.switch_page("page1.py")
