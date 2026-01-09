import streamlit as st
import pandas as pd
from DB.check_DB import get_all_messages
import time

REFRESH_SECONDS = 10
st.title("Chat History")
messages = get_all_messages()

if not messages:
    st.info("No messages found in database.")
else:
    df = pd.DataFrame(
        messages,
        columns=["Role", "Message", "Timestamp"]
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

time.sleep(REFRESH_SECONDS)
st.rerun()
