"""
Mock data generator for the Major-Industry Career Dashboard.

Produces a realistic synthetic dataset that mirrors the expected schema of the
final analysis output.  Run this module directly to regenerate mock_dataset.csv:

    python -m dashboard.mock_data.generate_mock

The generated file is used by data_loader.py when config.DATA_SOURCE == "mock".
"""

import random
import csv
from pathlib import Path

# ── Constants (aligned with config.py) ───────────────────────────────────────

MAJORS_BY_CLUSTER = {
    "BUSINESS & MANAGEMENT": [
        ("Financial Management", 373),
        ("Marketing Management", 323),
        ("Accounting", 145),
        ("Gen Business Mgmt", 124),
        ("Entrepreneurship", 106),
        ("Operations Management", 55),
        ("Human Resources Management", 51),
        ("Economics - Business", 44),
        ("Real Estate Studies", 37),
        ("International Business", 21),
    ],
    "ENGINEERING & TECHNOLOGY": [
        ("Mechanical Engineering", 228),
        ("Computer Science", 114),
        ("Data Science", 80),
        ("Electrical Engineering", 72),
        ("Civil Engineering", 51),
        ("Computer Engineering", 36),
        ("Software Engineering", 39),
        ("Data Analytics", 29),
        ("Manufacturing Engineering", 10),
        ("Systems Engineering", 6),
    ],
    "NATURAL & HEALTH SCIENCES": [
        ("Biology", 142),
        ("Actuarial Science", 86),
        ("Neuroscience", 68),
        ("Exercise Science", 64),
        ("Biochemistry", 41),
        ("Chemistry", 24),
        ("Environmental Science", 21),
        ("Public Health", 26),
        ("Nursing", 9),
        ("Physics", 6),
    ],
    "SOCIAL SCIENCES & HUMANITIES": [
        ("Psychology", 99),
        ("Political Science", 50),
        ("Philosophy", 39),
        ("Economics", 25),
        ("Criminal Justice", 24),
        ("History", 18),
        ("Sociology", 11),
        ("English", 18),
    ],
    "COMMUNICATION & MEDIA": [
        ("Communication Studies", 23),
        ("Strategic Comm: Ad and PR", 22),
        ("COJO Strategic Communications", 20),
        ("Journalism", 17),
        ("Digital Media Arts", 25),
        ("COJO Journalism", 12),
    ],
    "EDUCATION & SOCIAL SERVICES": [
        ("Social Work", 95),
        ("Elementary Education (K-6)", 32),
        ("Middle/Secondary Education", 14),
        ("Educational Studies", 14),
        ("Acad Behavioral Strategist", 53),
    ],
    "ARTS, LANGUAGES & THEOLOGY": [
        ("Catholic Studies", 46),
        ("Music - Business", 11),
        ("Theology", 5),
        ("Art History", 5),
        ("Spanish Cultural/Literary St.", 5),
        ("Music", 3),
    ],
}

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

# Probability weights: which industry groups each major cluster tends toward
CLUSTER_INDUSTRY_WEIGHTS = {
    "BUSINESS & MANAGEMENT":        [0.10, 0.05, 0.25, 0.05, 0.03, 0.03, 0.15, 0.20, 0.02, 0.12],
    "ENGINEERING & TECHNOLOGY":     [0.30, 0.05, 0.05, 0.25, 0.02, 0.03, 0.10, 0.03, 0.10, 0.07],
    "NATURAL & HEALTH SCIENCES":    [0.05, 0.35, 0.10, 0.08, 0.08, 0.05, 0.10, 0.05, 0.05, 0.09],
    "SOCIAL SCIENCES & HUMANITIES": [0.05, 0.10, 0.08, 0.03, 0.15, 0.15, 0.15, 0.10, 0.02, 0.17],
    "COMMUNICATION & MEDIA":        [0.15, 0.03, 0.05, 0.03, 0.05, 0.05, 0.15, 0.35, 0.02, 0.12],
    "EDUCATION & SOCIAL SERVICES":  [0.03, 0.15, 0.02, 0.02, 0.45, 0.15, 0.05, 0.05, 0.01, 0.07],
    "ARTS, LANGUAGES & THEOLOGY":   [0.05, 0.05, 0.03, 0.03, 0.25, 0.10, 0.10, 0.15, 0.02, 0.22],
}

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

SAMPLE_COMPANIES = {
    "Technology & Software":                    ["3M", "AWS", "Accenture", "Microsoft", "Google", "Target (Tech)", "Optum", "UnitedHealth Group", "Intel", "IBM"],
    "Healthcare & Medical":                     ["Mayo Clinic", "Abbott Laboratories", "Medtronic", "Allina Health", "Fairview", "Abbott Northwestern Hospital", "Children's Minnesota", "UnitedHealth Group", "Optum"],
    "Financial Services & Insurance":           ["US Bank", "Wells Fargo", "Ameriprise Financial", "Allianz", "Securian Financial", "Deloitte", "EY", "KPMG", "PwC", "RBC Wealth Management"],
    "Manufacturing & Industrial":               ["3M", "Honeywell", "Polaris", "Medtronic", "General Mills", "Cargill", "Toro Company", "Donaldson Company"],
    "Education & Academia":                     ["University of St. Thomas", "Minneapolis Public Schools", "St. Paul Public Schools", "Osseo Area Schools", "Wayzata Public Schools"],
    "Government & Public Service":              ["State of Minnesota", "City of Minneapolis", "Hennepin County", "US Army", "Peace Corps", "AmeriCorps"],
    "Professional Services & Consulting":       ["Accenture", "Deloitte", "EY", "McKinsey", "Boston Consulting Group", "KPMG", "PwC", "Grant Thornton"],
    "Retail & Consumer Products":               ["Target", "Best Buy", "General Mills", "Land O'Lakes", "Cargill", "Fastenal", "Sleep Number"],
    "Energy & Utilities":                       ["Xcel Energy", "CenterPoint Energy", "Great River Energy", "NextEra Energy"],
    "Construction / Engineering / Real Estate":  ["Ryan Companies", "Kraus-Anderson", "Mortenson", "McGough Construction", "CBRE Group"],
}

SAMPLE_TITLES = {
    "Education & Teaching":            ["Teacher", "Tutor", "Instructor", "Teaching Assistant", "Education Coordinator"],
    "Healthcare & Clinical":           ["Registered Nurse", "Physical Therapist", "Clinical Research Coordinator", "Health Coach", "Medical Assistant"],
    "Software & IT":                   ["Software Engineer", "Web Developer", "IT Analyst", "Systems Administrator", "DevOps Engineer"],
    "Data & Analytics":                ["Data Analyst", "Business Intelligence Analyst", "Data Scientist", "Analytics Consultant", "Quantitative Analyst"],
    "Finance & Accounting":            ["Accountant", "Financial Analyst", "Auditor", "Tax Associate", "Underwriter"],
    "Engineering":                     ["Mechanical Engineer", "Electrical Engineer", "Civil Engineer", "Project Engineer", "Design Engineer"],
    "Sales & Business Development":    ["Account Executive", "Sales Representative", "Business Development Associate", "Account Manager", "Inside Sales Rep"],
    "Marketing & Communications":      ["Marketing Coordinator", "Content Strategist", "Social Media Manager", "Brand Manager", "PR Specialist"],
    "Human Resources":                 ["HR Coordinator", "Recruiter", "Benefits Analyst", "Talent Acquisition Specialist", "HR Generalist"],
    "Consulting & Advisory":           ["Consultant", "Management Consultant", "Strategy Analyst", "Advisory Associate", "Business Analyst"],
    "Operations & Supply Chain":       ["Operations Analyst", "Supply Chain Coordinator", "Logistics Manager", "Procurement Specialist", "Operations Manager"],
    "Research & Science":              ["Research Assistant", "Lab Technician", "Research Scientist", "Clinical Research Associate", "Scientist"],
    "Legal":                           ["Paralegal", "Legal Assistant", "Compliance Analyst", "Contract Specialist", "Legal Coordinator"],
    "Government & Public Service":     ["Policy Analyst", "Government Affairs Specialist", "Public Administrator", "City Planner", "Legislative Aide"],
    "Nonprofit & Social Services":     ["Case Manager", "Social Worker", "Program Coordinator", "Community Outreach Specialist", "Grant Writer"],
    "Design & Creative":               ["Graphic Designer", "UX Designer", "Creative Director", "Visual Designer", "Multimedia Specialist"],
    "Management & Leadership":         ["Project Manager", "Program Manager", "Team Lead", "Operations Director", "Assistant Manager"],
    "Administrative & Support":        ["Administrative Assistant", "Office Manager", "Executive Assistant", "Office Coordinator", "Receptionist"],
    "Construction & Trades":           ["Construction Manager", "Site Supervisor", "Estimator", "Field Engineer", "Inspector"],
    "Real Estate":                     ["Real Estate Analyst", "Property Manager", "Leasing Agent", "Real Estate Associate", "Appraiser"],
    "Other":                           ["Associate", "Specialist", "Coordinator", "Analyst", "Assistant"],
}

SCHOOLS = [
    "Opus College of Business",
    "School of Engineering",
    "College of Arts and Sciences",
    "Morrison Family College of Health",
    "School of Education",
    "School of Social Work",
]

SCHOOL_BY_CLUSTER = {
    "BUSINESS & MANAGEMENT":        "Opus College of Business",
    "ENGINEERING & TECHNOLOGY":     "School of Engineering",
    "NATURAL & HEALTH SCIENCES":    "College of Arts and Sciences",
    "SOCIAL SCIENCES & HUMANITIES": "College of Arts and Sciences",
    "COMMUNICATION & MEDIA":        "College of Arts and Sciences",
    "EDUCATION & SOCIAL SERVICES":  "School of Education",
    "ARTS, LANGUAGES & THEOLOGY":   "College of Arts and Sciences",
}

STATES = [
    "MN", "MN", "MN", "MN", "MN",  # heavy MN weighting
    "WI", "CA", "TX", "IL", "NY",
    "CO", "WA", "FL", "GA", "MA",
    "ND", "SD", "IA", "NE", "OH",
]

GRAD_YEARS = list(range(2019, 2026))


def _pick_job_function(cluster: str, industry: str) -> str:
    """Pick a job function biased by cluster and industry."""
    # Simple heuristic weighting
    weights = [1.0] * len(JOB_FUNCTIONS)
    mapping = {
        "EDUCATION & SOCIAL SERVICES": {"Education & Teaching": 8, "Nonprofit & Social Services": 5, "Healthcare & Clinical": 3},
        "ENGINEERING & TECHNOLOGY":    {"Software & IT": 6, "Engineering": 6, "Data & Analytics": 4},
        "BUSINESS & MANAGEMENT":       {"Finance & Accounting": 5, "Sales & Business Development": 4, "Marketing & Communications": 3, "Management & Leadership": 3},
        "NATURAL & HEALTH SCIENCES":   {"Healthcare & Clinical": 6, "Research & Science": 5, "Data & Analytics": 3},
        "SOCIAL SCIENCES & HUMANITIES":{"Nonprofit & Social Services": 4, "Government & Public Service": 3, "Legal": 3, "Education & Teaching": 3},
        "COMMUNICATION & MEDIA":       {"Marketing & Communications": 7, "Design & Creative": 4, "Sales & Business Development": 3},
        "ARTS, LANGUAGES & THEOLOGY":  {"Education & Teaching": 4, "Design & Creative": 3, "Nonprofit & Social Services": 3},
    }
    if cluster in mapping:
        for fn, w in mapping[cluster].items():
            idx = JOB_FUNCTIONS.index(fn)
            weights[idx] = w
    return random.choices(JOB_FUNCTIONS, weights=weights, k=1)[0]


def generate_mock_dataset(n: int | None = None, seed: int = 42) -> list[dict]:
    """Generate a mock dataset of student career outcomes.

    If *n* is None, uses realistic counts from the real data (~3 474 rows).
    """
    random.seed(seed)
    rows: list[dict] = []

    for cluster, majors in MAJORS_BY_CLUSTER.items():
        for major, count in majors:
            actual_count = count if n is None else max(1, int(count * n / 3474))
            for _ in range(actual_count):
                industry = random.choices(INDUSTRY_GROUPS, weights=CLUSTER_INDUSTRY_WEIGHTS[cluster], k=1)[0]
                job_fn = _pick_job_function(cluster, industry)
                company = random.choice(SAMPLE_COMPANIES[industry])
                title = random.choice(SAMPLE_TITLES[job_fn])
                rows.append({
                    "Major": major,
                    "Major Cluster": cluster,
                    "Major Subcluster": "",  # placeholder — will be filled with real subclusters
                    "Academic Division": SCHOOL_BY_CLUSTER[cluster],
                    "Degree Level": "Bachelor's",
                    "Graduation Year": random.choice(GRAD_YEARS),
                    "Job Title": title,
                    "Job Function": job_fn,
                    "Company": company,
                    "Industry Group": industry,
                    "State": random.choice(STATES),
                })
    random.shuffle(rows)
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    """Write rows to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows → {path}")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "mock_dataset.csv"
    data = generate_mock_dataset()
    write_csv(data, out)
