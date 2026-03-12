"""
🗺️ Career Pathways Explorer — 3-level Sankey and drill-down tables.
"""

import streamlit as st
import pandas as pd

from dashboard.components.charts import sankey_three_level


def render(df: pd.DataFrame) -> None:
    st.header("🗺️ Career Pathways Explorer")

    st.markdown(
        "Trace the full pathway from **Major Cluster → Industry Group → Job Function** "
        "using the three-level Sankey diagram below."
    )

    # ── 3-level Sankey ───────────────────────────────────────────────────
    st.plotly_chart(sankey_three_level(df), use_container_width=True)

    st.divider()

    # ── Drill-down: select a specific major ──────────────────────────────
    st.subheader("🔎 Drill Down by Major")

    majors_sorted = sorted(df["Major"].unique())
    selected_major = st.selectbox("Select a major:", majors_sorted)

    subset = df[df["Major"] == selected_major]
    st.write(f"**{selected_major}** — {len(subset)} graduates")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top Industries**")
        st.dataframe(
            subset["Industry Group"].value_counts().reset_index().rename(
                columns={"index": "Industry", "count": "Count"}
            ),
            hide_index=True,
        )
    with col2:
        st.markdown("**Top Job Functions**")
        st.dataframe(
            subset["Job Function"].value_counts().reset_index().rename(
                columns={"index": "Function", "count": "Count"}
            ),
            hide_index=True,
        )

    # Top companies for this major
    st.markdown("**Top Employers**")
    st.dataframe(
        subset["Company"].value_counts().head(10).reset_index().rename(
            columns={"index": "Company", "count": "Count"}
        ),
        hide_index=True,
    )

    st.divider()

    # ── Pathway search ───────────────────────────────────────────────────
    st.subheader("🔗 Pathway Search")
    st.markdown("Filter by a specific **Major Cluster → Industry Group** combination.")

    col_mc, col_ig = st.columns(2)
    with col_mc:
        mc = st.selectbox("Major Cluster:", sorted(df["Major Cluster"].unique()), key="ps_mc")
    with col_ig:
        ig = st.selectbox("Industry Group:", sorted(df["Industry Group"].unique()), key="ps_ig")

    pathway = df[(df["Major Cluster"] == mc) & (df["Industry Group"] == ig)]
    st.write(f"**{len(pathway)}** graduates from *{mc}* → *{ig}*")

    if len(pathway) > 0:
        st.markdown("**Breakdown by Job Function:**")
        st.dataframe(
            pathway["Job Function"].value_counts().reset_index().rename(
                columns={"index": "Function", "count": "Count"}
            ),
            hide_index=True,
        )
        st.markdown("**Sample Records:**")
        st.dataframe(
            pathway[["Major", "Job Title", "Company", "Job Function", "Graduation Year"]]
            .sample(min(10, len(pathway)), random_state=42),
            hide_index=True,
        )
