import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Nifty 100 Analytics Dashboard")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Screen",
    [
        "Home",
        "Company Profile",
        "Screener",
        "Peer Comparison",
        "Trend Analysis",
        "Sector Analysis",
        "Capital Allocation",
        "Annual Reports"
    ]
)

st.header(page)

st.info("Sprint 4 Dashboard Scaffold Successfully Created.")

st.write(
    """
    This is the main dashboard entry point.

    Use the sidebar to navigate between all 8 screens.

    Each screen will be implemented during Sprint 4.
    """
)