"""
Validate pipeline outputs — checks that all expected files exist and
contain well-formed data.

Usage:
    python -m reproducibility.validate
    python run.py   (also runs this automatically after the pipeline)
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from settings import DATA_DIR, INTERMEDIATE_DIR, FINAL_OUTPUT, REPORTS_DIR, FINAL_COLUMNS


def validate() -> bool:
    """Run all checks. Returns True if everything passes."""
    passed = 0
    failed = 0

    def check(name: str, ok: bool, detail: str = ""):
        nonlocal passed, failed
        if ok:
            print(f"  ✅ {name}")
            passed += 1
        else:
            print(f"  ❌ {name}  — {detail}")
            failed += 1

    print("\n── Validation ──\n")

    # 1. Intermediate files
    for fname in ["01_cleaned.csv", "02_classified.csv", "03_analysis.json"]:
        p = INTERMEDIATE_DIR / fname
        check(f"Intermediate: {fname}", p.exists(), f"Missing: {p}")

    # 2. Final output
    check("Final CSV exists", FINAL_OUTPUT.exists(), f"Missing: {FINAL_OUTPUT}")

    if FINAL_OUTPUT.exists():
        import pandas as pd
        df = pd.read_csv(FINAL_OUTPUT)
        check(f"Final CSV has rows ({len(df):,})", len(df) > 0, "File is empty")

        missing_cols = set(FINAL_COLUMNS) - set(df.columns)
        check("Final CSV has all expected columns",
              len(missing_cols) == 0,
              f"Missing: {missing_cols}")

        null_pct = df.isnull().mean().mean() * 100
        check(f"Null values ≤ 20% (actual: {null_pct:.1f}%)",
              null_pct <= 20,
              f"Too many nulls: {null_pct:.1f}%")

    # 3. Pipeline report
    report_path = REPORTS_DIR / "pipeline_report.json"
    check("Pipeline report exists", report_path.exists(), f"Missing: {report_path}")
    if report_path.exists():
        with open(report_path) as f:
            report = json.load(f)
        check("Report has row count", "rows" in report, "Missing 'rows' key")

    # 4. Analysis JSON
    analysis_path = INTERMEDIATE_DIR / "03_analysis.json"
    if analysis_path.exists():
        with open(analysis_path) as f:
            analysis = json.load(f)
        check("Analysis has summary", "summary" in analysis, "Missing 'summary' key")

    # Summary
    total = passed + failed
    print(f"\n  {passed}/{total} checks passed", end="")
    if failed:
        print(f"  ({failed} failed)")
    else:
        print("  — all good! 🎉")

    return failed == 0


if __name__ == "__main__":
    ok = validate()
    sys.exit(0 if ok else 1)
