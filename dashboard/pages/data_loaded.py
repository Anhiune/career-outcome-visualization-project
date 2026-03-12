"""
📂 Data Loaded — Browse all CSV data files used in this project.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

from dashboard.config import PROJECT_ROOT


# Folder containing all CSVs
CSV_DIR = PROJECT_ROOT / "csv_data"

# The main files the pipeline actually uses (source → purpose)
_KEY_FILES = {
    "Ire_Anh_Data_1.22.26_(1).csv": "Raw student records (pipeline input)",
    # Major_Career_Analysis_v4 — all sheets
    "Major_Career_Analysis_v4__Cluster_Breakdown.csv": "v4: Major → (Large Cluster, Small Cluster)",
    "Major_Career_Analysis_v4__All_Majors.csv": "v4: All 91 majors with counts",
    "Major_Career_Analysis_v4__Small_Clusters.csv": "v4: 24 small clusters → large clusters",
    "Major_Career_Analysis_v4__Large_Clusters.csv": "v4: 7 large cluster summaries",
    "Major_Career_Analysis_v4__Job_Titles_by_Years.csv": "v4: 50 job titles → career clusters by year",
    "Major_Career_Analysis_v4__Breakdown_by_Years.csv": "v4: Major enrollment by year (2021–2024)",
    "Major_Career_Analysis_v4__Career_Analysis.csv": "v4: Career destination breakdown",
    "Major_Career_Analysis_v4__Career_Cluster_by_Years.csv": "v4: Career cluster trends by year",
    "Major_Career_Analysis_v4__Overview.csv": "v4: Summary statistics",
    # Career_Company_Industry_CLASSIFIED_v2 — all sheets
    "Career_Company_Industry_CLASSIFIED_v2__Full_Data_with_Industries.csv": "v2: Company → Industry + Job Function (2,828 rows)",
    "Career_Company_Industry_CLASSIFIED_v2__Industry_Groups_Summary.csv": "v2: 10 industry group summaries",
    "Career_Company_Industry_CLASSIFIED_v2__Unusual-Unrelated_Job_Titles.csv": "v2: 213 flagged unusual job titles",
    "Career_Company_Industry_CLASSIFIED_v2__Companies_Needing_Research.csv": "v2: Companies needing further research",
}

# Also show the pipeline output
_PIPELINE_OUTPUT = PROJECT_ROOT / "data" / "career_outcomes_final.csv"


@st.cache_data(show_spinner=False)
def _list_csv_files():
    """Return sorted list of CSV files in csv_data/."""
    if not CSV_DIR.exists():
        return []
    return sorted(CSV_DIR.glob("*.csv"), key=lambda p: p.name.lower())


@st.cache_data(show_spinner=False)
def _load_csv(path_str: str) -> pd.DataFrame:
    """Load a CSV with caching (keyed on path string)."""
    return pd.read_csv(path_str, nrows=500)


@st.cache_data(show_spinner=False)
def _file_stats(path_str: str):
    """Return (total_rows, cols) without loading entire file."""
    df = pd.read_csv(path_str)
    return len(df), len(df.columns), list(df.columns)


def render(df: pd.DataFrame) -> None:
    st.header("📂 Data Loaded")
    st.markdown(
        "Browse all CSV data files used in this project. "
        "Select a file to preview its contents."
    )

    # ── Pipeline output ──────────────────────────────────────────────────
    st.subheader("Pipeline Output")
    if _PIPELINE_OUTPUT.exists():
        rows, cols, col_names = _file_stats(str(_PIPELINE_OUTPUT))
        st.success(f"**{_PIPELINE_OUTPUT.name}** — {rows:,} rows × {cols} columns")
        with st.expander("Preview pipeline output", expanded=False):
            preview = _load_csv(str(_PIPELINE_OUTPUT))
            st.dataframe(preview, use_container_width=True, height=300)
    else:
        st.warning("Pipeline output not found. Run `python run.py` first.")

    st.divider()

    # ── CSV data files ───────────────────────────────────────────────────
    st.subheader("Source CSV Files")

    csv_files = _list_csv_files()

    if not csv_files:
        st.warning("No CSV files found in `csv_data/` folder.")
        return

    # Summary metrics
    c1, c2 = st.columns(2)
    c1.metric("Total CSV Files", len(csv_files))

    key_found = [f for f in csv_files if f.name in _KEY_FILES]
    c2.metric("Key Pipeline Files", len(key_found))

    st.divider()

    # ── Key files section ────────────────────────────────────────────────
    st.markdown("#### 🔑 Key Files (used by the pipeline)")
    for fp in csv_files:
        if fp.name in _KEY_FILES:
            purpose = _KEY_FILES[fp.name]
            rows, cols, col_names = _file_stats(str(fp))
            with st.expander(f"**{fp.name}**  —  {purpose}  ({rows:,} rows × {cols} cols)"):
                st.caption(f"Columns: {', '.join(col_names)}")
                preview = _load_csv(str(fp))
                st.dataframe(preview, use_container_width=True, height=300)
                if rows > 500:
                    st.info(f"Showing first 500 of {rows:,} rows.")

    st.divider()

    # ── All files browser ────────────────────────────────────────────────
    st.markdown("#### 📁 All CSV Files")

    # Group by base name (before __ separator)
    groups: dict[str, list[Path]] = {}
    for fp in csv_files:
        base = fp.name.split("__")[0] if "__" in fp.name else fp.stem
        groups.setdefault(base, []).append(fp)

    selected_group = st.selectbox(
        "Filter by workbook",
        ["All files"] + sorted(groups.keys()),
        index=0,
    )

    if selected_group == "All files":
        shown_files = csv_files
    else:
        shown_files = groups[selected_group]

    # File selector
    file_names = [f.name for f in shown_files]
    selected_name = st.selectbox("Select a file to preview", file_names)

    if selected_name:
        selected_path = CSV_DIR / selected_name
        rows, cols, col_names = _file_stats(str(selected_path))

        st.markdown(f"**{selected_name}** — {rows:,} rows × {cols} columns")
        if selected_name in _KEY_FILES:
            st.caption(f"🔑 {_KEY_FILES[selected_name]}")
        st.caption(f"Columns: {', '.join(col_names)}")

        preview = _load_csv(str(selected_path))
        st.dataframe(preview, use_container_width=True, height=400)
        if rows > 500:
            st.info(f"Showing first 500 of {rows:,} rows.")
