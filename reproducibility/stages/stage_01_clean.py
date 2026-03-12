"""
Stage 01 — Clean the raw data.

Reads your Excel/CSV, keeps the columns you specified in settings.py,
renames them to our standard names, and writes a cleaned CSV.

Run alone:   python -m reproducibility.stages.stage_01_clean
Run via:     python run.py
"""

import sys
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from settings import (
    RAW_DATA_FILE,
    YOUR_COLUMN_NAMES,
    EXCLUDE_DEGREE_LEVELS,
    MERGE_DUPLICATE_MAJORS,
    PARAMS,
    INTERMEDIATE_DIR,
)

CLEAN_OUTPUT = INTERMEDIATE_DIR / "01_cleaned.csv"

# Map from YOUR column names → our standard names
RENAME_MAP = {}
if YOUR_COLUMN_NAMES.get("major"):
    RENAME_MAP[YOUR_COLUMN_NAMES["major"]] = "Major"
if YOUR_COLUMN_NAMES.get("job_title"):
    RENAME_MAP[YOUR_COLUMN_NAMES["job_title"]] = "Job Title"
if YOUR_COLUMN_NAMES.get("company"):
    RENAME_MAP[YOUR_COLUMN_NAMES["company"]] = "Company"
if YOUR_COLUMN_NAMES.get("school"):
    RENAME_MAP[YOUR_COLUMN_NAMES["school"]] = "Academic Division"
if YOUR_COLUMN_NAMES.get("degree"):
    RENAME_MAP[YOUR_COLUMN_NAMES["degree"]] = "Degree Level"
if YOUR_COLUMN_NAMES.get("state"):
    RENAME_MAP[YOUR_COLUMN_NAMES["state"]] = "State"


def clean(input_path: Path | None = None) -> pd.DataFrame:
    """Load raw data, clean it, save as CSV."""

    src = input_path or RAW_DATA_FILE

    # Try CSV fallback if .xlsx not found
    if src and not src.exists() and src.suffix == ".xlsx":
        csv_alt = src.with_suffix(".csv")
        if csv_alt.exists():
            src = csv_alt

    if not src or not src.exists():
        print(f"[Stage 01] ERROR: Raw data file not found: {src}")
        print()
        print("  FIX: Open settings.py and set INPUT_FILE to your data file path.")
        print("  Example:  INPUT_FILE = 'my_data.xlsx'")
        print()
        print("  Or run with mock data:  python run.py --mock")
        sys.exit(1)

    # ── Load ─────────────────────────────────────────────────────────────
    print(f"[Stage 01] Loading: {src.name}")
    if src.suffix.lower() in (".xlsx", ".xls"):
        df = pd.read_excel(src)
    else:
        df = pd.read_csv(src)

    print(f"[Stage 01] Found {len(df):,} rows, {len(df.columns)} columns")
    print(f"[Stage 01] Columns: {list(df.columns)}")

    # ── Detect whether columns are already in standard form ────────────
    standard_names = set(RENAME_MAP.values())   # {"Major", "Job Title", …}
    raw_names      = set(RENAME_MAP.keys())     # {"Program Name/Major", …}
    grad_date_col  = YOUR_COLUMN_NAMES.get("grad_date")

    already_standard = "Major" in df.columns and raw_names != standard_names and not raw_names.issubset(set(df.columns))

    if already_standard:
        # Data already has standardized names (e.g., mock data) — skip rename
        print("[Stage 01] Columns already in standard form — skipping rename")
        keep_cols = [c for c in df.columns if c in standard_names or c not in raw_names]
        df = df[keep_cols].copy()
    else:
        # ── Check required columns exist ─────────────────────────────────
        required = YOUR_COLUMN_NAMES.get("major")
        if required and required not in df.columns:
            print(f"\n  ERROR: Column '{required}' not found in your data!")
            print(f"  Your file has these columns: {list(df.columns)}")
            print(f"\n  FIX: Open settings.py and update YOUR_COLUMN_NAMES")
            sys.exit(1)

        # ── Keep only mapped columns that exist ──────────────────────────
        # Also keep the grad_date column even though it's not renamed yet
        keep_cols = [c for c in RENAME_MAP.keys() if c in df.columns]
        if grad_date_col and grad_date_col in df.columns and grad_date_col not in keep_cols:
            keep_cols.append(grad_date_col)
        df = df[keep_cols].copy()

        # ── Rename to standard names ─────────────────────────────────────
        df = df.rename(columns=RENAME_MAP)
    initial = len(df)

    # ── Filter degree levels ─────────────────────────────────────────────
    if "Degree Level" in df.columns and EXCLUDE_DEGREE_LEVELS:
        df = df[~df["Degree Level"].isin(EXCLUDE_DEGREE_LEVELS)]
        removed = initial - len(df)
        if removed:
            print(f"[Stage 01] Filtered out {removed:,} non-undergrad records")

    # ── Merge duplicate major names ──────────────────────────────────────
    if MERGE_DUPLICATE_MAJORS and "Major" in df.columns:
        df["Major"] = df["Major"].replace(MERGE_DUPLICATE_MAJORS)
        print(f"[Stage 01] Merged {len(MERGE_DUPLICATE_MAJORS)} duplicate major names")

    # ── Drop very small majors ───────────────────────────────────────────
    min_count = PARAMS.get("min_major_count", 1)
    if min_count > 1 and "Major" in df.columns:
        counts = df["Major"].value_counts()
        keep = counts[counts >= min_count].index
        before = len(df)
        df = df[df["Major"].isin(keep)]
        print(f"[Stage 01] Dropped {before - len(df)} rows (majors with <{min_count} students)")

    # ── Extract graduation year from date ────────────────────────────────

    def _extract_year(series: pd.Series) -> pd.Series:
        """Extract year from a column that might be int, datetime, or string."""
        if pd.api.types.is_integer_dtype(series):
            # Already integer years (e.g. 2021, 2022, ...)
            return series
        if pd.api.types.is_float_dtype(series):
            return series.astype(int)
        # Try parsing as datetime
        dt = pd.to_datetime(series, errors="coerce")
        if dt.notna().any():
            return dt.dt.year
        return series  # give up, return as-is

    if grad_date_col and grad_date_col in RENAME_MAP:
        # We didn't rename it, handle separately
        pass
    # Check if original date column still exists (wasn't renamed)
    if grad_date_col and grad_date_col in df.columns:
        df["Graduation Year"] = _extract_year(df[grad_date_col])
        df = df.drop(columns=[grad_date_col], errors="ignore")
    elif "Graduation Date" in df.columns:
        df["Graduation Year"] = _extract_year(df["Graduation Date"])
        df = df.drop(columns=["Graduation Date"], errors="ignore")
    elif "Graduation Year" not in df.columns:
        df["Graduation Year"] = 2024  # default if no date info

    print(f'[Stage 01] Graduation years: {sorted(df["Graduation Year"].unique())}')

    # ── Save ─────────────────────────────────────────────────────────────
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_OUTPUT, index=False)
    print(f"[Stage 01] ✅ Saved {len(df):,} cleaned rows → {CLEAN_OUTPUT.name}")

    return df


if __name__ == "__main__":
    clean()
