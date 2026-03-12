"""
Stage 03 — Analyze the classified data.

Produces a JSON file with summary statistics, cross-tabulations,
top pathways, diversity scores, and yearly trends.

Run alone:   python -m reproducibility.stages.stage_03_analyze
Run via:     python run.py
"""

import json
import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from settings import INTERMEDIATE_DIR, PARAMS

CLASSIFIED_OUTPUT = INTERMEDIATE_DIR / "02_classified.csv"
ANALYSIS_OUTPUT   = INTERMEDIATE_DIR / "03_analysis.json"


def analyze(input_path: Path | None = None) -> dict:
    """Run the analysis and return results as a dict."""

    src = input_path or CLASSIFIED_OUTPUT
    if not src.exists():
        print(f"[Stage 03] ERROR: Input not found: {src}")
        print("           Run Stage 02 first (python run.py)")
        sys.exit(1)

    print(f"[Stage 03] Loading classified data: {src.name}")
    df = pd.read_csv(src)

    results: dict = {}

    # ── Summary ──────────────────────────────────────────────────────────
    results["summary"] = {
        "total_students":    int(len(df)),
        "unique_majors":     int(df["Major"].nunique()),
        "unique_companies":  int(df["Company"].nunique()) if "Company" in df.columns else 0,
        "unique_job_titles": int(df["Job Title"].nunique()) if "Job Title" in df.columns else 0,
        "year_range": [
            int(df["Graduation Year"].min()),
            int(df["Graduation Year"].max()),
        ] if "Graduation Year" in df.columns else [],
    }

    # ── Distributions ────────────────────────────────────────────────────
    results["major_counts"] = df["Major"].value_counts().head(PARAMS["top_n_majors"]).to_dict()
    results["cluster_distribution"] = df["Major Cluster"].value_counts().to_dict()
    results["industry_distribution"] = df["Industry Group"].value_counts().to_dict()
    results["job_function_distribution"] = df["Job Function"].value_counts().to_dict()

    # ── Cross-tabs ───────────────────────────────────────────────────────
    ct1 = pd.crosstab(df["Major Cluster"], df["Industry Group"])
    results["major_industry_matrix"] = {
        str(mc): {str(ig): int(ct1.loc[mc, ig]) for ig in ct1.columns}
        for mc in ct1.index
    }

    ct2 = pd.crosstab(df["Major Cluster"], df["Job Function"])
    results["major_jobfn_matrix"] = {
        str(mc): {str(jf): int(ct2.loc[mc, jf]) for jf in ct2.columns}
        for mc in ct2.index
    }

    # ── Top pathways ─────────────────────────────────────────────────────
    pathways = (
        df.groupby(["Major Cluster", "Industry Group"]).size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
        .head(PARAMS["top_n_pathways"])
    )
    results["top_pathways"] = pathways.to_dict(orient="records")

    # ── Top companies ────────────────────────────────────────────────────
    if "Company" in df.columns:
        results["top_companies"] = df["Company"].value_counts().head(PARAMS["top_n_companies"]).to_dict()

    # ── Yearly trends ────────────────────────────────────────────────────
    if "Graduation Year" in df.columns:
        yearly = df.groupby(["Graduation Year", "Major Cluster"]).size().reset_index(name="Count")
        results["yearly_trends"] = yearly.to_dict(orient="records")

    # ── Diversity scores (Simpson's index) ───────────────────────────────
    diversity = {}
    for mc in df["Major Cluster"].unique():
        props = df[df["Major Cluster"] == mc]["Industry Group"].value_counts(normalize=True)
        diversity[str(mc)] = round(float(1 - (props ** 2).sum()), 4)
    results["diversity_scores"] = diversity

    # ── Save ─────────────────────────────────────────────────────────────
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(ANALYSIS_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"[Stage 03] ✅ Saved analysis → {ANALYSIS_OUTPUT.name}")

    return results


if __name__ == "__main__":
    analyze()
