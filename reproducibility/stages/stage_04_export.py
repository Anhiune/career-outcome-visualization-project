"""
Stage 04 — Export the final dashboard-ready CSV.

Copies the classified data into 'data/career_outcomes_final.csv' with
exactly the columns the dashboard expects. Also writes a pipeline report.

Run alone:   python -m reproducibility.stages.stage_04_export
Run via:     python run.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from settings import INTERMEDIATE_DIR, FINAL_OUTPUT, FINAL_COLUMNS, DATA_DIR, REPORTS_DIR

CLASSIFIED_OUTPUT = INTERMEDIATE_DIR / "02_classified.csv"


def export(input_path: Path | None = None) -> Path:
    """Produce the final CSV for the dashboard."""

    src = input_path or CLASSIFIED_OUTPUT
    if not src.exists():
        print(f"[Stage 04] ERROR: Input not found: {src}")
        print("           Run Stage 02 first (python run.py)")
        sys.exit(1)

    print(f"[Stage 04] Loading classified data: {src.name}")
    df = pd.read_csv(src)

    # Ensure all expected columns exist (add blanks for any missing)
    for col in FINAL_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    df = df[FINAL_COLUMNS]

    # Save final CSV
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(FINAL_OUTPUT, index=False)
    print(f"[Stage 04] ✅ Saved {len(df):,} rows → {FINAL_OUTPUT.name}")

    # Save pipeline report
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report = {
        "timestamp":       datetime.now().isoformat(),
        "rows":            len(df),
        "columns":         list(df.columns),
        "unique_majors":   int(df["Major"].nunique()),
        "unique_companies": int(df["Company"].nunique()) if "Company" in df.columns else 0,
        "major_clusters":  sorted(df["Major Cluster"].dropna().unique().tolist()),
        "industry_groups": sorted(df["Industry Group"].dropna().unique().tolist()),
        "job_functions":   sorted(df["Job Function"].dropna().unique().tolist()),
    }
    report_path = REPORTS_DIR / "pipeline_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"[Stage 04] ✅ Saved report → {report_path.name}")

    return FINAL_OUTPUT


if __name__ == "__main__":
    export()
