"""
Pipeline config — re-exports everything from the top-level settings.py.

All pipeline stages import from here. You only ever edit settings.py.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from settings import (  # noqa: F401
    PROJECT_ROOT,
    DATA_DIR,
    RAW_DATA_FILE,
    INTERMEDIATE_DIR,
    FINAL_OUTPUT,
    FINAL_COLUMNS,
    REPORTS_DIR,
    SCHEMA,
    PARAMS,
    YOUR_COLUMN_NAMES,
    EXCLUDE_DEGREE_LEVELS,
    MERGE_DUPLICATE_MAJORS,
    USE_MOCK,
    MOCK_DATA_DIR,
    MAJOR_CLUSTERS,
    INDUSTRY_GROUPS,
    JOB_FUNCTIONS,
)

# Intermediate file paths
CLEAN_OUTPUT      = INTERMEDIATE_DIR / "01_cleaned.csv"
CLASSIFIED_OUTPUT = INTERMEDIATE_DIR / "02_classified.csv"
ANALYSIS_OUTPUT   = INTERMEDIATE_DIR / "03_analysis.json"

# Build expected raw column list from user's column mapping
RAW_COLUMNS = [v for v in YOUR_COLUMN_NAMES.values() if v is not None]
