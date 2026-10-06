import streamlit as st

st.set_page_config(page_title="Knowledge Engine POC", layout="wide")

pg = st.navigation(
    [
        st.Page("ui.py", title="Chat", icon="💬", default=True),
        st.Page("status_page.py", title="Status", icon="📊"),
    ],
    position="sidebar",  # use "top" for a menu at the top of the page
)
pg.run()