"""
🏢 Job Functions — Job-function distribution, heatmap, and sunburst.
"""

import streamlit as st
import pandas as pd

from dashboard.components.charts import (
    job_function_bar,
    heatmap_major_jobfn,
    sunburst_career,
)


def render(df: pd.DataFrame) -> None:
    st.header("🏢 Job Function Analysis")

    st.markdown(
        "What **functional roles** do graduates fill? Explore the distribution "
        "of the 21 classified job-function categories across clusters and industries."
    )

    # ── Aggregate bar ────────────────────────────────────────────────────
    st.plotly_chart(job_function_bar(df), use_container_width=True)

    st.divider()

    # ── Heatmap ──────────────────────────────────────────────────────────
    st.plotly_chart(heatmap_major_jobfn(df), use_container_width=True)

    st.divider()

    # ── Sunburst ─────────────────────────────────────────────────────────
    st.plotly_chart(sunburst_career(df), use_container_width=True)

    # ── Table ────────────────────────────────────────────────────────────
    with st.expander("📋 Job Function × Industry Group counts"):
        ct = pd.crosstab(df["Job Function"], df["Industry Group"], margins=True)
        st.dataframe(ct, use_container_width=True)
