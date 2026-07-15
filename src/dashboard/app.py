import streamlit as st
from pathlib import Path
import runpy

st.set_page_config(
    page_title="Nifty 100 Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Nifty 100 Analytics Dashboard")

pages = {
    "Home": "pages/01_home.py",
    "Company Profile": "pages/02_profile.py",
    "Screener": "pages/03_screener.py",
    "Peer Comparison": "pages/04_peers.py",
    "Trend Analysis": "pages/05_trends.py",
    "Sector Analysis": "pages/06_sectors.py",
    "Capital Allocation": "pages/07_capital.py",
    "Annual Reports": "pages/08_reports.py"
}

selection = st.sidebar.radio(
    "Navigation",
    list(pages.keys())
)

page = Path(pages[selection])

if page.exists():
    runpy.run_path(str(page))
else:
    st.error("Page not found.")