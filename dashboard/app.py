"""
UST Career Pathways Dashboard — main Streamlit entry point.

Run with:  streamlit run dashboard/app.py
Or just:   python run.py   (which does it for you)
"""

import streamlit as st
import pandas as pd

from dashboard.config import APP_TITLE, APP_ICON, DATA_SOURCE
from dashboard.data_loader import load_data
from dashboard.components.filters import apply_filters
from dashboard.pages import overview, major_industry, job_functions, career_pathways, data_loaded

# ─── Page config ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Data loading (cached) ──────────────────────────────────────────────────

@st.cache_data(show_spinner="Loading data …")
def _load():
    return load_data()

df_raw = _load()

# ─── Mock-data banner ───────────────────────────────────────────────────────

if DATA_SOURCE == "mock":
    st.info(
        "📋 **Using mock data.** To use your own file, open `settings.py`, "
        "set `INPUT_FILE` to your data path, then re-run.",
        icon="ℹ️",
    )

# ─── Sidebar + Navigation ───────────────────────────────────────────────────

PAGES = {
    "📊 Overview":           overview,
    "🔀 Major → Industry":  major_industry,
    "🏢 Job Functions":      job_functions,
    "🗺️ Career Pathways":   career_pathways,
    "📂 Data Loaded":        data_loaded,
}

st.sidebar.title(f"{APP_ICON} {APP_TITLE}")
page_name = st.sidebar.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")

# Apply filters
df = apply_filters(df_raw)

# Show active record count
st.sidebar.markdown(f"**{len(df):,}** / {len(df_raw):,} records shown")

# ─── Render selected page ───────────────────────────────────────────────────

PAGES[page_name].render(df)
