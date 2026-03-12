"""
Stage 02 — Classify each row.

Adds three new columns to the cleaned data:
  • Major Cluster     — which of 7 academic groups the major belongs to
  • Industry Group    — which of 10 industry groups the company belongs to
  • Job Function      — which of 21 job categories the title belongs to

When real lookup files exist (set in settings.py), classifications come
from those pre-classified Excel files. Otherwise falls back to the
built-in dictionaries and regex rules.

Run alone:   python -m reproducibility.stages.stage_02_classify
Run via:     python run.py
"""

import sys
import re
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from settings import INTERMEDIATE_DIR

# Try to import the real lookup paths
try:
    from settings import CLASSIFIED_COMPANIES_PATH, CLUSTER_BREAKDOWN_PATH
except ImportError:
    CLASSIFIED_COMPANIES_PATH = None
    CLUSTER_BREAKDOWN_PATH = None

CLEAN_OUTPUT      = INTERMEDIATE_DIR / "01_cleaned.csv"
CLASSIFIED_OUTPUT = INTERMEDIATE_DIR / "02_classified.csv"


# ═════════════════════════════════════════════════════════════════════════════
# LOAD REAL LOOKUP TABLES (if available)
# ═════════════════════════════════════════════════════════════════════════════

def _load_cluster_lookup() -> dict:
    """Load Major → (Cluster, Subcluster) from the real analysis Excel."""
    if CLUSTER_BREAKDOWN_PATH and CLUSTER_BREAKDOWN_PATH.exists():
        try:
            cb = pd.read_excel(CLUSTER_BREAKDOWN_PATH, sheet_name="Cluster Breakdown")
            lookup = {}
            for _, row in cb.iterrows():
                major = str(row["Major"]).strip()
                cluster = str(row["Large Cluster"]).strip()
                subcluster = str(row.get("Small Cluster", "")).strip()
                lookup[major] = (cluster, subcluster)
            print(f"[Stage 02] Loaded {len(lookup)} major→cluster mappings from real data")
            return lookup
        except Exception as e:
            print(f"[Stage 02] ⚠️  Could not read cluster file: {e}")
    return None


def _load_company_industry_lookup() -> tuple[dict, dict]:
    """Load Company → Industry Group and (Company,JobTitle) → Job Function from classified Excel."""
    company_to_industry = {}
    row_to_jobfn = {}  # (company, job_title) → job_function

    if CLASSIFIED_COMPANIES_PATH and CLASSIFIED_COMPANIES_PATH.exists():
        try:
            cf = pd.read_excel(CLASSIFIED_COMPANIES_PATH)
            for _, row in cf.iterrows():
                company = str(row.get("Employing Organization", "")).strip()
                industry = str(row.get("Industry Group (1 of 10)", "")).strip()
                job_title = str(row.get("Job Title", "")).strip()
                job_fn = str(row.get("Job Title Classified Group", "")).strip()

                # Strip numeric prefix (e.g. "1. Technology & Software" → "Technology & Software")
                industry_clean = re.sub(r"^\d+\.\s*", "", industry)

                if company and industry_clean and industry_clean != "nan":
                    company_to_industry[company] = industry_clean

                if company and job_title and job_fn and job_fn != "nan":
                    row_to_jobfn[(company, job_title)] = job_fn

            print(f"[Stage 02] Loaded {len(company_to_industry)} company→industry mappings from real data")
            print(f"[Stage 02] Loaded {len(row_to_jobfn)} (company,title)→function mappings from real data")
        except Exception as e:
            print(f"[Stage 02] ⚠️  Could not read classified file: {e}")

    return company_to_industry, row_to_jobfn


# ═════════════════════════════════════════════════════════════════════════════
# MAJOR → CLUSTER MAPPING
# ═════════════════════════════════════════════════════════════════════════════
# Format:  "Major Name": ("CLUSTER NAME", "Subcluster Name")
#
# To add your own majors, just add more lines below.
# Any major not listed here will be labeled "UNCATEGORIZED".

MAJOR_TO_CLUSTER = {
    # ── BUSINESS & MANAGEMENT ────────────────────────────────────────────
    "Financial Management":       ("BUSINESS & MANAGEMENT", "Finance & Accounting"),
    "Marketing Management":       ("BUSINESS & MANAGEMENT", "Marketing"),
    "Accounting":                  ("BUSINESS & MANAGEMENT", "Finance & Accounting"),
    "Gen Business Mgmt":           ("BUSINESS & MANAGEMENT", "General Management"),
    "Entrepreneurship":            ("BUSINESS & MANAGEMENT", "General Management"),
    "Operations Management":       ("BUSINESS & MANAGEMENT", "Operations"),
    "Human Resources Management":  ("BUSINESS & MANAGEMENT", "Human Resources"),
    "Economics - Business":        ("BUSINESS & MANAGEMENT", "Economics"),
    "Real Estate Studies":         ("BUSINESS & MANAGEMENT", "Real Estate"),
    "International Business":      ("BUSINESS & MANAGEMENT", "International Business"),
    "Bus Admin - Communication":   ("BUSINESS & MANAGEMENT", "General Management"),
    "Family Business":             ("BUSINESS & MANAGEMENT", "General Management"),
    "Risk Management and Insurance": ("BUSINESS & MANAGEMENT", "Finance & Accounting"),
    "Org. Ethics & Compliance":    ("BUSINESS & MANAGEMENT", "General Management"),
    "Law & Compliance":            ("BUSINESS & MANAGEMENT", "Legal"),
    "Legal Studies":               ("BUSINESS & MANAGEMENT", "Legal"),
    "MBA":                         ("BUSINESS & MANAGEMENT", "General Management"),
    "Executive MBA":               ("BUSINESS & MANAGEMENT", "General Management"),
    "Health Care MBA":             ("BUSINESS & MANAGEMENT", "General Management"),
    "Data Analytics":              ("BUSINESS & MANAGEMENT", "Operations & Analytics"),
    "MS Operations & Supply Chain Mgmt": ("BUSINESS & MANAGEMENT", "Operations"),
    "MS Business Analytics":       ("BUSINESS & MANAGEMENT", "Operations & Analytics"),
    "Data Science":                ("BUSINESS & MANAGEMENT", "Operations & Analytics"),
    "Leadership & Management":     ("BUSINESS & MANAGEMENT", "General Management"),
    "Leadership":                  ("BUSINESS & MANAGEMENT", "General Management"),
    "Technology Management":       ("BUSINESS & MANAGEMENT", "General Management"),
    "Software Management":         ("BUSINESS & MANAGEMENT", "General Management"),
    "Health Care Innovation":      ("BUSINESS & MANAGEMENT", "General Management"),
    "Liberal Arts":                ("BUSINESS & MANAGEMENT", "General Management"),
    "U.S. Law":                    ("BUSINESS & MANAGEMENT", "Legal"),

    # ── ENGINEERING & TECHNOLOGY ─────────────────────────────────────────
    "Mechanical Engineering":      ("ENGINEERING & TECHNOLOGY", "Engineering Disciplines"),
    "Computer Science":            ("ENGINEERING & TECHNOLOGY", "Computer Science & IT"),
    "Data Science":                ("ENGINEERING & TECHNOLOGY", "Computer Science & IT"),
    "Electrical Engineering":      ("ENGINEERING & TECHNOLOGY", "Engineering Disciplines"),
    "Civil Engineering":           ("ENGINEERING & TECHNOLOGY", "Engineering Disciplines"),
    "Computer Engineering":        ("ENGINEERING & TECHNOLOGY", "Computer Science & IT"),
    "Software Engineering":        ("ENGINEERING & TECHNOLOGY", "Computer Science & IT"),
    "Data Analytics":              ("ENGINEERING & TECHNOLOGY", "Computer Science & IT"),
    "Manufacturing Engineering":   ("ENGINEERING & TECHNOLOGY", "Engineering Disciplines"),
    "Systems Engineering":         ("ENGINEERING & TECHNOLOGY", "Engineering Disciplines"),
    "Information Technology":      ("ENGINEERING & TECHNOLOGY", "Computer Science & IT"),
    "Quant Methods - Computer Sci": ("ENGINEERING & TECHNOLOGY", "Computer Science & IT"),

    # ── NATURAL & HEALTH SCIENCES ────────────────────────────────────────
    "Biology":                     ("NATURAL & HEALTH SCIENCES", "Biological Sciences"),
    "Actuarial Science":           ("NATURAL & HEALTH SCIENCES", "Mathematics & Statistics"),
    "Neuroscience":                ("NATURAL & HEALTH SCIENCES", "Biological Sciences"),
    "Exercise Science":            ("NATURAL & HEALTH SCIENCES", "Health Sciences"),
    "Biochemistry":                ("NATURAL & HEALTH SCIENCES", "Biological Sciences"),
    "Chemistry":                   ("NATURAL & HEALTH SCIENCES", "Physical Sciences"),
    "Public Health":               ("NATURAL & HEALTH SCIENCES", "Health Sciences"),
    "Environmental Science":       ("NATURAL & HEALTH SCIENCES", "Environmental Sciences"),
    "Environmental Studies":       ("NATURAL & HEALTH SCIENCES", "Environmental Sciences"),
    "Nursing":                     ("NATURAL & HEALTH SCIENCES", "Health Sciences"),
    "Physics":                     ("NATURAL & HEALTH SCIENCES", "Physical Sciences"),
    "Geology":                     ("NATURAL & HEALTH SCIENCES", "Physical Sciences"),
    "Biology of Global Health":    ("NATURAL & HEALTH SCIENCES", "Health Sciences"),
    "Health Promotion & Wellness": ("NATURAL & HEALTH SCIENCES", "Health Sciences"),
    "Statistics":                  ("NATURAL & HEALTH SCIENCES", "Mathematics & Statistics"),
    "Mathematics (Applied Track)": ("NATURAL & HEALTH SCIENCES", "Mathematics & Statistics"),
    "Mathematics (Education Track)": ("NATURAL & HEALTH SCIENCES", "Mathematics & Statistics"),
    "Mathematics (Pure Track)":    ("NATURAL & HEALTH SCIENCES", "Mathematics & Statistics"),
    "Mathematics (Statistics Track)": ("NATURAL & HEALTH SCIENCES", "Mathematics & Statistics"),
    "Geography":                   ("NATURAL & HEALTH SCIENCES", "Environmental Sciences"),
    "Geography - Geo Info Sys (GIS)": ("NATURAL & HEALTH SCIENCES", "Environmental Sciences"),

    # ── SOCIAL SCIENCES & HUMANITIES ─────────────────────────────────────
    "Psychology":                  ("SOCIAL SCIENCES & HUMANITIES", "Psychology"),
    "Political Science":           ("SOCIAL SCIENCES & HUMANITIES", "Political Science"),
    "Philosophy":                  ("SOCIAL SCIENCES & HUMANITIES", "Philosophy"),
    "Economics":                   ("SOCIAL SCIENCES & HUMANITIES", "Economics"),
    "Economics - International":   ("SOCIAL SCIENCES & HUMANITIES", "Economics"),
    "Economics - Mathematical":    ("SOCIAL SCIENCES & HUMANITIES", "Economics"),
    "Economics - Public Policy":   ("SOCIAL SCIENCES & HUMANITIES", "Economics"),
    "Criminal Justice":            ("SOCIAL SCIENCES & HUMANITIES", "Criminal Justice"),
    "History":                     ("SOCIAL SCIENCES & HUMANITIES", "History"),
    "English":                     ("SOCIAL SCIENCES & HUMANITIES", "English & Writing"),
    "English - Creative Writing":  ("SOCIAL SCIENCES & HUMANITIES", "English & Writing"),
    "English - Professional Writing": ("SOCIAL SCIENCES & HUMANITIES", "English & Writing"),
    "Sociology":                   ("SOCIAL SCIENCES & HUMANITIES", "Sociology"),
    "Intl Studies - Economics":    ("SOCIAL SCIENCES & HUMANITIES", "International Studies"),
    "Intl Studies - History":      ("SOCIAL SCIENCES & HUMANITIES", "International Studies"),
    "Intl Studies - Pol Sci":      ("SOCIAL SCIENCES & HUMANITIES", "International Studies"),
    "Justice & Peace Studies":     ("SOCIAL SCIENCES & HUMANITIES", "Social Sciences"),
    "Classical Civilization":      ("SOCIAL SCIENCES & HUMANITIES", "History"),
    "Family Studies":              ("SOCIAL SCIENCES & HUMANITIES", "Social Sciences"),
    "Individualized":              ("SOCIAL SCIENCES & HUMANITIES", "Social Sciences"),
    "Creative Writing & Publishing": ("SOCIAL SCIENCES & HUMANITIES", "English & Writing"),

    # ── COMMUNICATION & MEDIA ────────────────────────────────────────────
    "Communication Studies":       ("COMMUNICATION & MEDIA", "Communication"),
    "Strategic Comm: Ad and PR":   ("COMMUNICATION & MEDIA", "Strategic Communication"),
    "COJO Strategic Communications": ("COMMUNICATION & MEDIA", "Strategic Communication"),
    "Journalism":                  ("COMMUNICATION & MEDIA", "Journalism"),
    "Digital Media Arts":          ("COMMUNICATION & MEDIA", "Digital Media"),
    "COJO Journalism":             ("COMMUNICATION & MEDIA", "Journalism"),
    "COJO Creative Multimedia":    ("COMMUNICATION & MEDIA", "Digital Media"),
    "COJO Interpersonal Comm":     ("COMMUNICATION & MEDIA", "Communication"),
    "COJO Persuasion/Soc Influence": ("COMMUNICATION & MEDIA", "Communication"),
    "Business Communication":      ("COMMUNICATION & MEDIA", "Communication"),
    "Communication and Journalism": ("COMMUNICATION & MEDIA", "Journalism"),
    "Strategic Communication":     ("COMMUNICATION & MEDIA", "Strategic Communication"),

    # ── EDUCATION & SOCIAL SERVICES ──────────────────────────────────────
    "Social Work":                 ("EDUCATION & SOCIAL SERVICES", "Social Work"),
    "Elementary Education (K-6)":  ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Middle/Secondary Education":  ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Educational Studies":         ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Acad Behavioral Strategist":  ("EDUCATION & SOCIAL SERVICES", "Special Education"),
    "Early Childhood Special Educ": ("EDUCATION & SOCIAL SERVICES", "Special Education"),
    "Autism Spectrum Disorders":   ("EDUCATION & SOCIAL SERVICES", "Special Education"),
    "K-12 Music Education":        ("EDUCATION & SOCIAL SERVICES", "Education"),
    "K-12 World Lang. & Cultures": ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Teacher Preparation - K-12":  ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Teacher Preparation-Elem K-6": ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Teacher Preparation-Secondary": ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Music Education":             ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Educ Leadership & Learning":  ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Educational Leadership & Admin": ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Leadership In Student Affairs": ("EDUCATION & SOCIAL SERVICES", "Education"),
    "Counseling Psychology":        ("EDUCATION & SOCIAL SERVICES", "Social Work"),
    "Social Work Advanced Standing": ("EDUCATION & SOCIAL SERVICES", "Social Work"),
    "Organization Develop & Change": ("EDUCATION & SOCIAL SERVICES", "Social Work"),
    "Organization Development":     ("EDUCATION & SOCIAL SERVICES", "Social Work"),
    "Publc Safety & Law Enfr Ldrshp": ("EDUCATION & SOCIAL SERVICES", "Education"),

    # ── ARTS, LANGUAGES & THEOLOGY ───────────────────────────────────────
    "Catholic Studies":            ("ARTS, LANGUAGES & THEOLOGY", "Theology"),
    "Theology":                    ("ARTS, LANGUAGES & THEOLOGY", "Theology"),
    "Pastoral Leadership":         ("ARTS, LANGUAGES & THEOLOGY", "Theology"),
    "Pastoral Ministry":           ("ARTS, LANGUAGES & THEOLOGY", "Theology"),
    "Music":                       ("ARTS, LANGUAGES & THEOLOGY", "Music & Arts"),
    "Music - Business":            ("ARTS, LANGUAGES & THEOLOGY", "Music & Arts"),
    "Music - Performance":         ("ARTS, LANGUAGES & THEOLOGY", "Music & Arts"),
    "Art History":                  ("ARTS, LANGUAGES & THEOLOGY", "Visual Arts"),
    "French":                      ("ARTS, LANGUAGES & THEOLOGY", "Languages"),
    "German":                      ("ARTS, LANGUAGES & THEOLOGY", "Languages"),
    "Spanish":                     ("ARTS, LANGUAGES & THEOLOGY", "Languages"),
    "Spanish Cultural/Literary St.": ("ARTS, LANGUAGES & THEOLOGY", "Languages"),
    "Spanish Linguistics/Lang. St.": ("ARTS, LANGUAGES & THEOLOGY", "Languages"),

    # ── NATURAL & HEALTH SCIENCES (additional) ───────────────────────
    "Regulatory Science":           ("NATURAL & HEALTH SCIENCES", "Health Sciences"),
    "Mathematics":                  ("NATURAL & HEALTH SCIENCES", "Mathematics & Statistics"),
    "Software Engineering":         ("ENGINEERING & TECHNOLOGY", "Computer Science & IT"),
    "Manufacturing Engineering":    ("ENGINEERING & TECHNOLOGY", "Engineering Disciplines"),
    "Systems Engineering":          ("ENGINEERING & TECHNOLOGY", "Engineering Disciplines"),
    "Information Technology":       ("ENGINEERING & TECHNOLOGY", "Computer Science & IT"),
}


# ═════════════════════════════════════════════════════════════════════════════
# COMPANY → INDUSTRY GROUP MAPPING
# ═════════════════════════════════════════════════════════════════════════════
# Add your companies here. Any company not listed → "Uncategorized".

COMPANY_TO_INDUSTRY = {
    # Technology & Software
    "3M":                      "Technology & Software",
    "AWS":                     "Technology & Software",
    "Microsoft":               "Technology & Software",
    "Google":                  "Technology & Software",
    "Intel":                   "Technology & Software",
    "IBM":                     "Technology & Software",
    "Apple":                   "Technology & Software",
    "Amazon":                  "Technology & Software",
    "Meta":                    "Technology & Software",
    "Target (Tech)":           "Technology & Software",
    "Optum":                   "Technology & Software",

    # Healthcare & Medical
    "Mayo Clinic":             "Healthcare & Medical",
    "Abbott Laboratories":     "Healthcare & Medical",
    "Abbott Northwestern Hospital": "Healthcare & Medical",
    "Medtronic":               "Healthcare & Medical",
    "Allina Health":           "Healthcare & Medical",
    "Fairview":                "Healthcare & Medical",
    "Children's Minnesota":    "Healthcare & Medical",
    "UnitedHealth Group":      "Healthcare & Medical",

    # Financial Services & Insurance
    "US Bank":                 "Financial Services & Insurance",
    "Wells Fargo":             "Financial Services & Insurance",
    "Ameriprise Financial":    "Financial Services & Insurance",
    "Allianz":                 "Financial Services & Insurance",
    "Securian Financial":      "Financial Services & Insurance",
    "RBC Wealth Management":   "Financial Services & Insurance",

    # Manufacturing & Industrial
    "Honeywell":               "Manufacturing & Industrial",
    "Polaris":                 "Manufacturing & Industrial",
    "General Mills":           "Manufacturing & Industrial",
    "Cargill":                 "Manufacturing & Industrial",
    "Toro Company":            "Manufacturing & Industrial",
    "Donaldson Company":       "Manufacturing & Industrial",

    # Education & Academia
    "University of St. Thomas": "Education & Academia",
    "Minneapolis Public Schools": "Education & Academia",
    "St. Paul Public Schools": "Education & Academia",
    "Osseo Area Schools":      "Education & Academia",
    "Wayzata Public Schools":  "Education & Academia",

    # Government & Public Service
    "State of Minnesota":      "Government & Public Service",
    "City of Minneapolis":     "Government & Public Service",
    "Hennepin County":         "Government & Public Service",
    "US Army":                 "Government & Public Service",
    "Peace Corps":             "Government & Public Service",
    "AmeriCorps":              "Government & Public Service",

    # Professional Services & Consulting
    "Accenture":               "Professional Services & Consulting",
    "Deloitte":                "Professional Services & Consulting",
    "EY":                      "Professional Services & Consulting",
    "McKinsey":                "Professional Services & Consulting",
    "Boston Consulting Group": "Professional Services & Consulting",
    "KPMG":                    "Professional Services & Consulting",
    "PwC":                     "Professional Services & Consulting",
    "Grant Thornton":          "Professional Services & Consulting",

    # Retail & Consumer Products
    "Target":                  "Retail & Consumer Products",
    "Best Buy":                "Retail & Consumer Products",
    "Land O'Lakes":            "Retail & Consumer Products",
    "Fastenal":                "Retail & Consumer Products",
    "Sleep Number":            "Retail & Consumer Products",

    # Energy & Utilities
    "Xcel Energy":             "Energy & Utilities",
    "CenterPoint Energy":      "Energy & Utilities",
    "Great River Energy":      "Energy & Utilities",
    "NextEra Energy":          "Energy & Utilities",

    # Construction / Engineering / Real Estate
    "Ryan Companies":          "Construction / Engineering / Real Estate",
    "Kraus-Anderson":          "Construction / Engineering / Real Estate",
    "Mortenson":               "Construction / Engineering / Real Estate",
    "McGough Construction":    "Construction / Engineering / Real Estate",
    "CBRE Group":              "Construction / Engineering / Real Estate",
}


# ═════════════════════════════════════════════════════════════════════════════
# JOB TITLE → JOB FUNCTION (regex rules)
# ═════════════════════════════════════════════════════════════════════════════
# Each rule is (regex_pattern, category_name).
# Rules are checked in order — first match wins.

JOB_TITLE_RULES: list[tuple[str, str]] = [
    (r"teacher|tutor|instructor|professor|education",                                  "Education & Teaching"),
    (r"nurse|rn\b|therapist|clinical|physician|pharma|medical|health",                 "Healthcare & Clinical"),
    (r"software|developer|devops|sre|full.?stack|front.?end|back.?end|programmer",     "Software & IT"),
    (r"data.?(analyst|scientist|engineer)|analytics|business.?intelligence|bi\b",      "Data & Analytics"),
    (r"account(ant|ing)|auditor|tax|financial.?analyst|underwriter|cpa\b|bookkeep",    "Finance & Accounting"),
    (r"engineer|engineering",                                                           "Engineering"),
    (r"sales|business.?development|account.?exec|bdm\b",                               "Sales & Business Development"),
    (r"marketing|brand|content|social.?media|pr\b|public.?relation|advertising",       "Marketing & Communications"),
    (r"human.?resource|recruiter|talent|hr\b|benefits|payroll",                        "Human Resources"),
    (r"consult|advisory|strateg",                                                       "Consulting & Advisory"),
    (r"operations|supply.?chain|logistics|procurement|warehouse",                      "Operations & Supply Chain"),
    (r"research|lab|scientist|r&d",                                                     "Research & Science"),
    (r"paralegal|legal|attorney|law\b|compliance|contract",                            "Legal"),
    (r"government|public.?admin|city.?plan|legislat|policy",                           "Government & Public Service"),
    (r"social.?work|case.?manager|nonprofit|community|volunteer|grant",                "Nonprofit & Social Services"),
    (r"design|ux|ui\b|graphic|creative|multimedia|visual",                             "Design & Creative"),
    (r"manager|director|vp\b|president|chief|head.?of|lead\b",                        "Management & Leadership"),
    (r"admin|assistant|coordinator|receptionist|office.?manager|clerk",                 "Administrative & Support"),
    (r"construct|site.?super|estimat|field.?engineer|inspector",                       "Construction & Trades"),
    (r"real.?estate|property|apprais|leasing|broker",                                  "Real Estate"),
]


def classify_job_title(title: str) -> str:
    """Classify a single job title string → one of 21 categories."""
    if not isinstance(title, str):
        return "Other"
    t = title.lower().strip()
    for pattern, category in JOB_TITLE_RULES:
        if re.search(pattern, t):
            return category
    return "Other"


def classify(input_path: Path | None = None) -> pd.DataFrame:
    """Run the classification stage."""

    src = input_path or CLEAN_OUTPUT
    if not src.exists():
        print(f"[Stage 02] ERROR: Input not found: {src}")
        print("           Run Stage 01 first (python run.py)")
        sys.exit(1)

    print(f"[Stage 02] Loading cleaned data: {src.name}")
    df = pd.read_csv(src)

    # ── Try loading real lookup tables first ──────────────────────────────
    real_cluster_lookup = _load_cluster_lookup()
    real_company_lookup, real_jobtitle_lookup = _load_company_industry_lookup()

    # ── Classify majors ──────────────────────────────────────────────────
    # Build a combined lookup: real data first, then hardcoded fallback
    combined_cluster = {}
    # Add hardcoded (always available as safety net)
    combined_cluster.update(MAJOR_TO_CLUSTER)
    # Overlay real lookup — but skip "Unclassified" entries so hardcoded can fill them
    if real_cluster_lookup:
        for k, v in real_cluster_lookup.items():
            cluster_name = v[0] if isinstance(v, tuple) else v
            if cluster_name != "Unclassified":
                combined_cluster[k] = v

    def _lookup_cluster(major):
        val = combined_cluster.get(major)
        if val:
            return val if isinstance(val, tuple) else (val, "")
        return ("UNCATEGORIZED", "")

    df["Major Cluster"]    = df["Major"].map(lambda m: _lookup_cluster(m)[0])
    df["Major Subcluster"] = df["Major"].map(lambda m: _lookup_cluster(m)[1])

    uncat = df["Major Cluster"].isin(["UNCATEGORIZED", "Unclassified"]).sum()
    if uncat:
        unmapped = df[df["Major Cluster"].isin(["UNCATEGORIZED", "Unclassified"])]["Major"].unique()
        print(f"[Stage 02] ⚠️  {uncat} rows have unmapped majors: {list(unmapped[:10])}")

    # ── Classify companies → Industry Group ──────────────────────────────
    if "Company" in df.columns:
        if real_company_lookup:
            # Use real pre-classified lookup
            df["Industry Group"] = df["Company"].map(real_company_lookup).fillna("Other")
        else:
            df["Industry Group"] = df["Company"].map(COMPANY_TO_INDUSTRY).fillna("Other")

        other_ind = (df["Industry Group"] == "Other").sum()
        if other_ind:
            print(f"[Stage 02] ⚠️  {other_ind} rows have unmapped companies → 'Other'")
    else:
        df["Industry Group"] = "Other"

    # ── Classify job titles → Job Function ───────────────────────────────
    if "Job Title" in df.columns and "Company" in df.columns and real_jobtitle_lookup:
        # Use real per-row lookup: (company, job_title) → job_function
        def lookup_job_fn(row):
            key = (str(row.get("Company", "")).strip(), str(row.get("Job Title", "")).strip())
            result = real_jobtitle_lookup.get(key)
            if result:
                return result
            # Fallback to regex
            return classify_job_title(row.get("Job Title", ""))

        df["Job Function"] = df.apply(lookup_job_fn, axis=1)
        matched = df["Job Function"].ne("Other").sum()
        print(f"[Stage 02] Job functions: {matched} matched, {len(df) - matched} as 'Other'")
    elif "Job Title" in df.columns:
        df["Job Function"] = df["Job Title"].apply(classify_job_title)
        other_count = (df["Job Function"] == "Other").sum()
        print(f"[Stage 02] Job functions: {other_count} classified as 'Other'")
    else:
        df["Job Function"] = "Other"

    # ── Save ─────────────────────────────────────────────────────────────
    INTERMEDIATE_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLASSIFIED_OUTPUT, index=False)
    print(f"[Stage 02] ✅ Saved {len(df):,} classified rows → {CLASSIFIED_OUTPUT.name}")

    return df


if __name__ == "__main__":
    classify()
