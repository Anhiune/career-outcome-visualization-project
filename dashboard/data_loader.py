"""
Data loader for the dashboard.

Loads either mock data (if settings.INPUT_FILE is None) or the real
pipeline output (data/career_outcomes_final.csv).

Handles everything automatically — you just call load_data().
"""

import pandas as pd
from pathlib import Path

from dashboard.config import DATA_SOURCE, MOCK_DATA_DIR, REAL_DATA_FILE, SCHEMA


def _ensure_mock_data() -> Path:
    """Generate mock CSV if it doesn't exist yet."""
    csv_path = MOCK_DATA_DIR / "mock_dataset.csv"
    if not csv_path.exists():
        from dashboard.mock_data.generate_mock import generate_mock_dataset, write_csv
        rows = generate_mock_dataset()
        write_csv(rows, csv_path)
    return csv_path


def load_data() -> pd.DataFrame:
    """Load the dataset. Returns a DataFrame with standardized columns."""

    if DATA_SOURCE == "real":
        if not REAL_DATA_FILE.exists():
            raise FileNotFoundError(
                f"Final data not found: {REAL_DATA_FILE}\n"
                "\n"
                "  Either:\n"
                "  1. Run the pipeline first:  python run.py\n"
                "  2. Or set INPUT_FILE = None in settings.py to use mock data\n"
            )
        df = pd.read_csv(REAL_DATA_FILE)
    else:
        csv_path = _ensure_mock_data()
        df = pd.read_csv(csv_path)

    # Quick column check
    expected = set(SCHEMA.values())
    actual = set(df.columns)
    missing = expected - actual
    if missing:
        raise ValueError(
            f"Dataset missing columns: {missing}\n"
            f"Expected: {sorted(expected)}\n"
            f"Found:    {sorted(actual)}"
        )

    if "Graduation Year" in df.columns:
        df["Graduation Year"] = df["Graduation Year"].astype(int)

    return df
