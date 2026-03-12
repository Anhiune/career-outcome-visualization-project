"""
🔀 Major → Industry — Chord diagram, heatmap, and stacked bar of career flows.
"""

import streamlit as st
import pandas as pd

from dashboard.components.charts import (
    chord_major_industry,
    heatmap_major_industry,
    stacked_bar_clusters,
)


def render(df: pd.DataFrame) -> None:
    st.header("🔀 Major → Industry Pathways")

    st.markdown(
        "How do graduates from each **Major Cluster** distribute across "
        "**Industry Groups**? Use the sidebar filters to slice the data."
    )

    # ── Chord / Circos diagram ────────────────────────────────────────────
    st.plotly_chart(chord_major_industry(df), use_container_width=True)

    st.divider()

    # ── Heatmap ──────────────────────────────────────────────────────────
    st.plotly_chart(heatmap_major_industry(df), use_container_width=True)

    st.divider()

    # ── Stacked bar ──────────────────────────────────────────────────────
    st.plotly_chart(stacked_bar_clusters(df), use_container_width=True)

    # ── Raw cross-tab table ──────────────────────────────────────────────
    with st.expander("📋 Cross-tabulation data"):
        ct = pd.crosstab(df["Major Cluster"], df["Industry Group"], margins=True)
        st.dataframe(ct, use_container_width=True)
