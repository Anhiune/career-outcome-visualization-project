"""
=========================================================================
  SETTINGS.PY — The ONE file you edit to configure everything.
=========================================================================

This is the single source of truth for the entire project.
Both the dashboard and the reproducibility pipeline read from here.

HOW TO USE WITH YOUR OWN DATA:
  1. Put your Excel/CSV file in the project folder (or anywhere).
  2. Set INPUT_FILE below to point at it.
  3. Set YOUR_COLUMN_NAMES to tell us which of your columns maps to what.
  4. Run:  python run.py
  5. Open: http://localhost:8501

That's it. Everything else is automatic.
=========================================================================
"""

from pathlib import Path

# ─────────────────────────────────────────────────────────────────────────────
# 1. WHERE IS YOUR DATA?
# ─────────────────────────────────────────────────────────────────────────────
#    Point this at your Excel (.xlsx) or CSV (.csv) file.
#    Use an absolute path, or a path relative to this file.
#
#    Examples:
#      INPUT_FILE = "my_data.xlsx"
#      INPUT_FILE = "C:/Users/me/Desktop/career_data.csv"
#      INPUT_FILE = None   ← uses built-in mock data (for testing)

INPUT_FILE = "major_industry_circos_draft1/Ire Anh Data 1.22.26 (1).xlsx"

# Supplementary lookup files (pre-classified data from your folder)
CLASSIFIED_COMPANIES_FILE = "major_industry_circos_draft1/data/Career_Company_Industry_CLASSIFIED_v2.xlsx"
CLUSTER_BREAKDOWN_FILE    = "major_industry_circos_draft1/Major_Career_Analysis_v4.xlsx"

# ─────────────────────────────────────────────────────────────────────────────
# 2. WHAT ARE YOUR COLUMN NAMES?
# ─────────────────────────────────────────────────────────────────────────────
#    Tell us which column in YOUR file corresponds to each field.
#    Only "major" and "job_title" are required. Leave others as None
#    if your data doesn't have them — we'll handle it gracefully.
#
#    The LEFT side is what we call it internally.
#    The RIGHT side is the column header in YOUR file.

YOUR_COLUMN_NAMES = {
    "major":          "Program Name/Major",        # REQUIRED — student's major
    "job_title":      "Job Title",                 # REQUIRED — their job after graduation
    "company":        "Employing Organization",    # Company/employer name
    "school":         "Academic Division/School",  # College within the university
    "degree":         "Degree Level",              # e.g., "Bachelor's"
    "grad_date":      "Graduation Date",           # Date or year of graduation
    "state":          "Position Location - State", # US state of employment

    # These are ADDED by the pipeline (you don't need them in your raw data):
    # "major_cluster"    → auto-assigned (7 academic clusters)
    # "industry_group"   → auto-assigned (10 industry groups)
    # "job_function"     → auto-assigned (21 job function categories)
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. WHAT DEGREE LEVELS TO KEEP?
# ─────────────────────────────────────────────────────────────────────────────
#    If your data has a "Degree Level" column, we'll filter OUT these levels.
#    Set to [] (empty list) to keep everything.

EXCLUDE_DEGREE_LEVELS = [
    "Master's", "Doctorate", "Certificate",
    "Graduate level degree",   # actual label in the UST dataset
    "Associate's degree",      # keep focus on bachelor's only
]

# ─────────────────────────────────────────────────────────────────────────────
# 4. DUPLICATE MAJOR NAMES TO MERGE
# ─────────────────────────────────────────────────────────────────────────────
#    If the same major appears under different names, map old → new here.
#    Set to {} (empty dict) if you don't have duplicates.

MERGE_DUPLICATE_MAJORS = {
    "Business Communication":        "Bus Admin - Communication",
    "Communication and Journalism":  "Communication Studies",
    "Strategic Communication":       "Strategic Comm: Ad and PR",
    # (BS) suffix variants
    "Computer Science (BS)":          "Computer Science",
    "Biology (BS)":                   "Biology",
    "Geology (BS)":                   "Geology",
    "Physics (BS)":                   "Physics",
    "Comp Science BS (Master Track)": "Computer Science",
    "Environmental Sci (Chemistry)":  "Environmental Science",
    "Environmental Sci (Geoscience)": "Environmental Science",
    "Economm ics - Public Policy":    "Economics - Public Policy",
}

# ─────────────────────────────────────────────────────────────────────────────
# 5. DASHBOARD APPEARANCE (optional)
# ─────────────────────────────────────────────────────────────────────────────

APP_TITLE = "UST Career Pathways Dashboard"
APP_ICON  = "🎓"


# ═════════════════════════════════════════════════════════════════════════════
#  EVERYTHING BELOW IS AUTOMATIC — you don't need to change it.
# ═════════════════════════════════════════════════════════════════════════════

# ── Paths (auto-computed) ────────────────────────────────────────────────────
PROJECT_ROOT     = Path(__file__).resolve().parent
DATA_DIR         = PROJECT_ROOT / "data"
INTERMEDIATE_DIR = DATA_DIR / "intermediate"
FINAL_OUTPUT     = DATA_DIR / "career_outcomes_final.csv"
MOCK_DATA_DIR    = PROJECT_ROOT / "dashboard" / "mock_data"
REPORTS_DIR      = PROJECT_ROOT / "reproducibility" / "reports"

# Resolve input file path
if INPUT_FILE is not None:
    _p = Path(INPUT_FILE)
    RAW_DATA_FILE = _p if _p.is_absolute() else PROJECT_ROOT / _p
else:
    RAW_DATA_FILE = None  # will use mock data

# Resolve supplementary lookup files
def _resolve(val):
    if not val:
        return None
    p = Path(val)
    return p if p.is_absolute() else PROJECT_ROOT / p

CLASSIFIED_COMPANIES_PATH = _resolve(CLASSIFIED_COMPANIES_FILE if 'CLASSIFIED_COMPANIES_FILE' in dir() else None)
CLUSTER_BREAKDOWN_PATH    = _resolve(CLUSTER_BREAKDOWN_FILE if 'CLUSTER_BREAKDOWN_FILE' in dir() else None)

# Whether we're using mock data
USE_MOCK = (RAW_DATA_FILE is None) or (not Path(RAW_DATA_FILE).exists() if RAW_DATA_FILE else True)

# ── Internal schema (the standardized column names used everywhere) ──────────
SCHEMA = {
    "major":            "Major",
    "major_cluster":    "Major Cluster",
    "major_subcluster": "Major Subcluster",
    "school":           "Academic Division",
    "degree":           "Degree Level",
    "grad_year":        "Graduation Year",
    "job_title":        "Job Title",
    "job_function":     "Job Function",
    "company":          "Company",
    "industry_group":   "Industry Group",
    "state":            "State",
}

FINAL_COLUMNS = list(SCHEMA.values())

# ── Major Clusters (7 groups) ────────────────────────────────────────────────
MAJOR_CLUSTERS = [
    "BUSINESS & MANAGEMENT",
    "ENGINEERING & TECHNOLOGY",
    "NATURAL & HEALTH SCIENCES",
    "SOCIAL SCIENCES & HUMANITIES",
    "COMMUNICATION & MEDIA",
    "EDUCATION & SOCIAL SERVICES",
    "ARTS, LANGUAGES & THEOLOGY",
]

MAJOR_CLUSTER_COLORS = {
    "BUSINESS & MANAGEMENT":        "#1f77b4",
    "ENGINEERING & TECHNOLOGY":     "#ff7f0e",
    "NATURAL & HEALTH SCIENCES":    "#2ca02c",
    "SOCIAL SCIENCES & HUMANITIES": "#d62728",
    "COMMUNICATION & MEDIA":        "#9467bd",
    "EDUCATION & SOCIAL SERVICES":  "#8c564b",
    "ARTS, LANGUAGES & THEOLOGY":   "#e377c2",
}

# ── Industry Groups (10 groups) ──────────────────────────────────────────────
INDUSTRY_GROUPS = [
    "Technology & Software",
    "Healthcare & Medical",
    "Financial Services & Insurance",
    "Manufacturing & Industrial",
    "Education & Academia",
    "Government & Public Service",
    "Professional Services & Consulting",
    "Retail & Consumer Products",
    "Energy & Utilities",
    "Construction / Engineering / Real Estate",
]

INDUSTRY_COLORS = {
    "Technology & Software":                    "#4e79a7",
    "Healthcare & Medical":                     "#f28e2b",
    "Financial Services & Insurance":           "#e15759",
    "Manufacturing & Industrial":               "#76b7b2",
    "Education & Academia":                     "#59a14f",
    "Government & Public Service":              "#edc948",
    "Professional Services & Consulting":       "#b07aa1",
    "Retail & Consumer Products":               "#ff9da7",
    "Energy & Utilities":                       "#9c755f",
    "Construction / Engineering / Real Estate": "#bab0ac",
}

# ── Job Function Categories (21 groups) ──────────────────────────────────────
JOB_FUNCTIONS = [
    "Education & Teaching",
    "Healthcare & Clinical",
    "Software & IT",
    "Data & Analytics",
    "Finance & Accounting",
    "Engineering",
    "Sales & Business Development",
    "Marketing & Communications",
    "Human Resources",
    "Consulting & Advisory",
    "Operations & Supply Chain",
    "Research & Science",
    "Legal",
    "Government & Public Service",
    "Nonprofit & Social Services",
    "Design & Creative",
    "Management & Leadership",
    "Administrative & Support",
    "Construction & Trades",
    "Real Estate",
    "Other",
]

# ── Pipeline parameters ─────────────────────────────────────────────────────
PARAMS = {
    "min_major_count": 1,
    "top_n_majors": 20,
    "top_n_companies": 20,
    "top_n_pathways": 20,
}
