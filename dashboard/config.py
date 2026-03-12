"""
Dashboard config — re-exports everything from the top-level settings.py.

All dashboard modules import from here. You only ever edit settings.py.
"""

import sys
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from settings import (  # noqa: F401
    PROJECT_ROOT,
    DATA_DIR,
    MOCK_DATA_DIR,
    FINAL_OUTPUT as REAL_DATA_FILE,
    USE_MOCK,
    SCHEMA,
    FINAL_COLUMNS,
    MAJOR_CLUSTERS,
    MAJOR_CLUSTER_COLORS,
    INDUSTRY_GROUPS,
    INDUSTRY_COLORS,
    JOB_FUNCTIONS,
    APP_TITLE,
    APP_ICON,
    PARAMS,
)

DATA_SOURCE = "mock" if USE_MOCK else "real"
DASHBOARD_DIR = Path(__file__).resolve().parent
SIDEBAR_TITLE = "Filters"
