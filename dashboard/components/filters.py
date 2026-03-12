"""
Shared sidebar filter components for the Streamlit dashboard.

Each function writes widgets into st.sidebar and returns the user's selections.
Pages call these to apply consistent filtering across views.
"""

from __future__ import annotations

import streamlit as st
import pandas as pd

from dashboard.config import MAJOR_CLUSTERS, INDUSTRY_GROUPS, JOB_FUNCTIONS


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filters and return a filtered copy of *df*.

    Filters:
      • Graduation year range
      • Major clusters (multiselect)
      • Industry groups (multiselect)
      • Job functions (multiselect)
    """
    st.sidebar.header("🔍 Filters")

    # ── Year range ───────────────────────────────────────────────────────
    years = sorted(df["Graduation Year"].unique())
    if len(years) > 1:
        yr_min, yr_max = st.sidebar.slider(
            "Graduation Year",
            min_value=int(min(years)),
            max_value=int(max(years)),
            value=(int(min(years)), int(max(years))),
        )
        df = df[(df["Graduation Year"] >= yr_min) & (df["Graduation Year"] <= yr_max)]

    # ── Major clusters ───────────────────────────────────────────────────
    available_clusters = sorted(df["Major Cluster"].unique())
    selected_clusters = st.sidebar.multiselect(
        "Major Clusters",
        options=available_clusters,
        default=available_clusters,
    )
    if selected_clusters:
        df = df[df["Major Cluster"].isin(selected_clusters)]

    # ── Industry groups ──────────────────────────────────────────────────
    available_industries = sorted(df["Industry Group"].unique())
    selected_industries = st.sidebar.multiselect(
        "Industry Groups",
        options=available_industries,
        default=available_industries,
    )
    if selected_industries:
        df = df[df["Industry Group"].isin(selected_industries)]

    # ── Job functions ────────────────────────────────────────────────────
    available_fns = sorted(df["Job Function"].unique())
    selected_fns = st.sidebar.multiselect(
        "Job Functions",
        options=available_fns,
        default=available_fns,
    )
    if selected_fns:
        df = df[df["Job Function"].isin(selected_fns)]

    # Show record count
    st.sidebar.metric("Records after filtering", f"{len(df):,}")

    return df
