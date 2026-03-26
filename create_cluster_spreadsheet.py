import csv
import os

DATA_DIR = "csv_data"
MAIN_DATA = os.path.join(DATA_DIR, "Ire_Anh_Data_1.22.26_(1).csv")
MAJOR_CLUSTERS = os.path.join(DATA_DIR, "Major_Career_Analysis_v4__Cluster_Breakdown.csv")
CAREER_CLUSTERS = os.path.join(DATA_DIR, "Major_Career_Analysis_v4__Career_Analysis.csv")
OUTPUT_FILE = os.path.join("csv_exports", "Major_Job_Cluster_Lookup.csv")

def load_major_cluster_map():
    """Build major name -> (small_cluster, large_cluster) mapping."""
    mapping = {}
    with open(MAJOR_CLUSTERS, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            major = row["Major"].strip()
            mapping[major.lower()] = {
                "small": row["Small Cluster"].strip(),
                "large": row["Large Cluster"].strip(),
            }
    return mapping

def load_career_cluster_map():
    """Build job title -> (small_cluster, large_cluster) mapping from the detailed breakdown."""
    mapping = {}
    with open(CAREER_CLUSTERS, encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    header_idx = None
    for i, row in enumerate(rows):
        if len(row) >= 3 and row[0] == "Large Cluster" and row[1] == "Small Cluster" and row[2] == "Job Title":
            header_idx = i
            break

    if header_idx is None:
        print("WARNING: Could not find detailed breakdown header in career analysis.")
        return mapping

    for row in rows[header_idx + 1:]:
        if len(row) < 4 or not row[0].strip():
            continue
        large = row[0].strip()
        small = row[1].strip()
        job_title = row[2].strip()
        if job_title and job_title.lower() != "unknown":
            mapping[job_title.lower()] = {"small": small, "large": large}
    return mapping

MAJOR_NAME_ALIASES = {
    "computer science (bs)": "computer science",
    "comp science bs (master track)": "comp science bs (master track)",
    "economics - public policy": "economics",
    "economics - business": "economics",
    "economics - international": "economics",
    "economics - mathematical": "economics",
    "biology (bs)": "biology",
    "geology (bs)": "geology",
    "physics (bs)": "physics",
    "data science": "data analytics",
    "information technology": "computer science",
    "software engineering": "computer science",
    "software management": "computer science",
    "systems engineering": "mechanical engineering",
    "manufacturing engineering": "mechanical engineering",
    "mba": "gen business mgmt",
    "executive mba": "gen business mgmt",
    "health care mba": "gen business mgmt",
    "leadership": "leadership & management",
    "spanish": "spanish cultural/literary st.",
    "creative writing & publishing": "english - creative writing",
    "music education": "k-12 music education",
    "liberal arts": "philosophy",
    "teacher preparation - k-12": "middle/secondary education",
    "teacher preparation-elem k-6": "elementary education (k-6)",
    "teacher preparation-secondary": "middle/secondary education",
    "educational studies": "middle/secondary education",
    "educational leadership & admin": "leadership & management",
    "educ leadership & learning": "leadership & management",
    "counseling psychology": "psychology",
    "pastoral leadership": "theology",
    "pastoral ministry": "theology",
    "autism spectrum disorders": "social work",
    "acad behavioral strategist": "social work",
    "early childhood special educ": "social work",
    "organization develop & change": "human resources management",
    "organization development": "human resources management",
    "org. ethics & compliance": "law & compliance",
    "health care innovation": "public health",
    "regulatory science": "chemistry",
    "technology management": "operations management",
    "u.s. law": "law & compliance",
    "publc safety & law enfr ldrshp": "law & compliance",
    "mathematics (applied track)": "mathematics",
    "mathematics (education track)": "mathematics",
    "mathematics (pure track)": "mathematics",
    "mathematics (statistics track)": "statistics",
    "leadership in student affairs": "leadership & management",
}

DIRECT_CLUSTER_OVERRIDES = {
    "liberal arts": {"small": "Humanities & Liberal Arts", "large": "SOCIAL SCIENCES & HUMANITIES"},
    "systems engineering": {"small": "Engineering Disciplines", "large": "ENGINEERING & TECHNOLOGY"},
    "manufacturing engineering": {"small": "Engineering Disciplines", "large": "ENGINEERING & TECHNOLOGY"},
    "data science": {"small": "Computer Science & IT", "large": "ENGINEERING & TECHNOLOGY"},
    "information technology": {"small": "Computer Science & IT", "large": "ENGINEERING & TECHNOLOGY"},
    "software engineering": {"small": "Computer Science & IT", "large": "ENGINEERING & TECHNOLOGY"},
    "software management": {"small": "Computer Science & IT", "large": "ENGINEERING & TECHNOLOGY"},
    "counseling psychology": {"small": "Social Sciences", "large": "SOCIAL SCIENCES & HUMANITIES"},
    "autism spectrum disorders": {"small": "Special Education & Counseling", "large": "EDUCATION & SOCIAL SERVICES"},
    "acad behavioral strategist": {"small": "Special Education & Counseling", "large": "EDUCATION & SOCIAL SERVICES"},
    "early childhood special educ": {"small": "Special Education & Counseling", "large": "EDUCATION & SOCIAL SERVICES"},
    "educational studies": {"small": "Teacher Education", "large": "EDUCATION & SOCIAL SERVICES"},
    "educational leadership & admin": {"small": "Educational Leadership", "large": "EDUCATION & SOCIAL SERVICES"},
    "educ leadership & learning": {"small": "Educational Leadership", "large": "EDUCATION & SOCIAL SERVICES"},
    "leadership in student affairs": {"small": "Educational Leadership", "large": "EDUCATION & SOCIAL SERVICES"},
    "organization develop & change": {"small": "Specialized Business", "large": "BUSINESS & MANAGEMENT"},
    "organization development": {"small": "Specialized Business", "large": "BUSINESS & MANAGEMENT"},
    "org. ethics & compliance": {"small": "Specialized Business", "large": "BUSINESS & MANAGEMENT"},
    "u.s. law": {"small": "Specialized Business", "large": "BUSINESS & MANAGEMENT"},
    "publc safety & law enfr ldrshp": {"small": "Specialized Business", "large": "BUSINESS & MANAGEMENT"},
    "mba": {"small": "General Business", "large": "BUSINESS & MANAGEMENT"},
    "executive mba": {"small": "General Business", "large": "BUSINESS & MANAGEMENT"},
    "health care mba": {"small": "General Business", "large": "BUSINESS & MANAGEMENT"},
    "health care innovation": {"small": "Health & Wellness", "large": "NATURAL & HEALTH SCIENCES"},
    "regulatory science": {"small": "Physical Sciences", "large": "NATURAL & HEALTH SCIENCES"},
    "technology management": {"small": "Operations & Analytics", "large": "BUSINESS & MANAGEMENT"},
    "creative writing & publishing": {"small": "Creative Writing", "large": "COMMUNICATION & MEDIA"},
    "music education": {"small": "Teacher Education", "large": "EDUCATION & SOCIAL SERVICES"},
    "spanish": {"small": "Languages", "large": "ARTS, LANGUAGES & THEOLOGY"},
    "pastoral leadership": {"small": "Arts & Theology", "large": "ARTS, LANGUAGES & THEOLOGY"},
    "pastoral ministry": {"small": "Arts & Theology", "large": "ARTS, LANGUAGES & THEOLOGY"},
}

def lookup_major(major_name, major_map):
    key = major_name.strip().lower()
    if key in major_map:
        return major_map[key]
    if key in DIRECT_CLUSTER_OVERRIDES:
        return DIRECT_CLUSTER_OVERRIDES[key]
    if key in MAJOR_NAME_ALIASES:
        alias = MAJOR_NAME_ALIASES[key]
        if alias in major_map:
            return major_map[alias]
    return {"small": "", "large": ""}

def lookup_job(job_title, career_map):
    if not job_title or not job_title.strip():
        return {"small": "", "large": ""}
    key = job_title.strip().lower()
    if key in career_map:
        return career_map[key]
    return {"small": "Unclassified Jobs", "large": "Unclassified"}

def main():
    major_map = load_major_cluster_map()
    career_map = load_career_cluster_map()

    print(f"Loaded {len(major_map)} major -> cluster mappings")
    print(f"Loaded {len(career_map)} job title -> cluster mappings")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    unmatched_majors = set()
    total = 0
    major_matched = 0
    job_matched = 0

    with open(MAIN_DATA, encoding="utf-8") as fin, \
         open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as fout:

        reader = csv.DictReader(fin)
        writer = csv.writer(fout)
        writer.writerow([
            "Major",
            "Small Major Cluster",
            "Large Major Cluster",
            "Job Title",
            "Small Job Title Cluster",
            "Large Job Title Cluster",
        ])

        for row in reader:
            total += 1
            major = row.get("Program Name/Major", "").strip()
            job_title = row.get("Job Title", "").strip()

            mc = lookup_major(major, major_map)
            jc = lookup_job(job_title, career_map)

            if mc["small"]:
                major_matched += 1
            else:
                unmatched_majors.add(major)

            if jc["small"] and jc["small"] != "Unclassified Jobs":
                job_matched += 1

            writer.writerow([
                major,
                mc["small"],
                mc["large"],
                job_title,
                jc["small"],
                jc["large"],
            ])

    print(f"\nProcessed {total} rows")
    print(f"Major cluster matched: {major_matched}/{total} ({100*major_matched/total:.1f}%)")
    print(f"Job title cluster matched: {job_matched}/{total} ({100*job_matched/total:.1f}%)")

    if unmatched_majors:
        print(f"\nUnmatched majors ({len(unmatched_majors)}):")
        for m in sorted(unmatched_majors):
            print(f"  - {m}")

    print(f"\nOutput saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
