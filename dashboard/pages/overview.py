"""
📊 Overview — Key metrics and high-level distributions.
"""

import streamlit as st
import pandas as pd

from dashboard.components.charts import (
    treemap_overview,
    trend_line,
    top_majors_bar,
)


def render(df: pd.DataFrame) -> None:
    st.header("📊 Overview")

    # ── KPI row ──────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Graduates", f"{len(df):,}")
    c2.metric("Unique Majors", df["Major"].nunique())
    c3.metric("Companies", df["Company"].nunique())
    c4.metric("Grad-Year Span", f"{df['Graduation Year'].min()}–{df['Graduation Year'].max()}")

    st.divider()

    # ── Cluster distribution ─────────────────────────────────────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Graduates by Major Cluster")
        cluster_counts = df["Major Cluster"].value_counts()
        st.bar_chart(cluster_counts)

    with col_right:
        st.subheader("Graduates by Industry Group")
        industry_counts = df["Industry Group"].value_counts()
        st.bar_chart(industry_counts)

    st.divider()

    # ── Treemap ──────────────────────────────────────────────────────────
    st.plotly_chart(treemap_overview(df), use_container_width=True)

    # ── Top majors ───────────────────────────────────────────────────────
    st.plotly_chart(top_majors_bar(df, n=20), use_container_width=True)

    # ── Trends ───────────────────────────────────────────────────────────
    if df["Graduation Year"].nunique() > 1:
        st.plotly_chart(trend_line(df), use_container_width=True)
