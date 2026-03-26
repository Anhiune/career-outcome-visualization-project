import csv
from collections import Counter, defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
SOURCE_CSV = PROJECT_ROOT / "data" / "career_outcomes_final.csv"
SIDE_TOTAL_UNITS = 1000


VISIBLE_SUBCLUSTER = "Arts & Theology"

SUBCLUSTER_ORDER = [
    "Arts & Theology",
    "English & Writing",
    "Languages",
]

SUBCLUSTER_COLORS = {
    "Arts & Theology": "major_arts",
    "English & Writing": "major_writing",
    "Languages": "major_languages",
}

CAREER_ORDER = [
    "Unclassified",
    "Business & Finance",
    "Healthcare & Science",
    "Technology & Engineering",
    "Education & Service",
    "Arts, Media & Legal",
]

CAREER_COLORS = {
    "Business & Finance": "career_business",
    "Technology & Engineering": "career_technology",
    "Healthcare & Science": "career_health",
    "Education & Service": "career_education",
    "Arts, Media & Legal": "career_arts",
    "Unclassified": "career_unclassified",
}

MAJOR_DISPLAY_ORDER = [
    "Catholic Studies",
    "Music - Business",
    "Music",
    "Theology",
    "Art History",
    "Music - Performance",
    "English",
    "English - Professional Writing",
    "Spanish Cultural/Literary St.",
    "French",
    "Spanish Linguistics/Lang. St.",
    "German",
]


def sanitize_id(value: str) -> str:
    cleaned = []
    for ch in value:
        if ch.isalnum():
            cleaned.append(ch)
        else:
            cleaned.append("_")
    token = "".join(cleaned).strip("_")
    while "__" in token:
        token = token.replace("__", "_")
    return token or "unknown"


def compact_label(value: str) -> str:
    replacements = {
        "Catholic Studies": "Catholic-Studies",
        "Music - Business": "Music-Business",
        "Music - Performance": "Music-Perf",
        "Art History": "Art-History",
        "English - Professional Writing": "Eng-Prof-Writing",
        "Spanish Cultural/Literary St.": "Spanish-Cultural",
        "Spanish Linguistics/Lang. St.": "Spanish-Linguistics",
        "Business & Finance": "Business-Finance",
        "Technology & Engineering": "Tech-Eng",
        "Healthcare & Science": "Health-Science",
        "Education & Service": "Edu-Service",
        "Arts, Media & Legal": "Arts-Legal",
    }
    return replacements.get(value, value.replace(" ", "-"))


def scale_counts(count_map, total_units):
    total = sum(count_map.values())
    if total <= 0:
        return {key: 1 for key in count_map}

    raw = {key: (value / total) * total_units for key, value in count_map.items()}
    scaled = {key: max(1, int(raw[key])) for key in count_map}
    remainder = total_units - sum(scaled.values())

    if remainder > 0:
        order = sorted(count_map, key=lambda key: (raw[key] - scaled[key]), reverse=True)
        idx = 0
        while remainder > 0:
            key = order[idx % len(order)]
            scaled[key] += 1
            remainder -= 1
            idx += 1
    elif remainder < 0:
        order = sorted(count_map, key=lambda key: (scaled[key] - raw[key]), reverse=True)
        idx = 0
        while remainder < 0 and order:
            key = order[idx % len(order)]
            if scaled[key] > 1:
                scaled[key] -= 1
                remainder += 1
            idx += 1

    return scaled


def map_job_to_small_cluster(title: str) -> str:
    title = str(title).lower().strip()

    if any(k in title for k in ["accountant", "audit", "tax", "bookkeep"]):
        return "Accounting & Audit"
    if any(k in title for k in ["financ", "wealth", "bank", "invest", "risk", "actuar", "underwrit", "loan", "credit", "equity", "portfolio"]):
        return "Finance & Investment"
    if any(k in title for k in ["project manager", "program manager", "operations", "logistics", "supply chain", "coordinator", "planner", "production", "inventory"]):
        return "Management & Operations"
    if any(k in title for k in ["sales", "account executive", "market", "brand", "pr ", "public relations", "social media", "advertising", "digital", "seo", "communication", "buyer", "merchandis"]):
        return "Sales & Marketing"

    if any(k in title for k in ["software", "developer", "programmer", "data", "cloud", "cyber", "security", "web", "full stack", "front end", "back end"]):
        return "Software & Data"
    if any(k in title for k in ["engineer", "mechanical", "civil", "electrical", "manufacturing", "systems"]):
        if "software" not in title:
            return "Engineering"
    if any(k in title for k in ["it ", "network", "technician", "support", "help desk", "admin", "tech "]):
        return "IT & Infrastructure"

    if any(k in title for k in ["nurse", "rn", "doctor", "physician", "medical", "patient", "health", "therapist", "pharm", "dent", "care", "hospital", "clinic", "veterinary"]):
        return "Clinical Care"
    if any(k in title for k in ["research", "scientist", "bio", "chem", "lab", "assistant", "fellow"]):
        if "sales" not in title:
            return "Research & Science"

    if any(k in title for k in ["teach", "tutor", "professor", "instructor", "educat", "school", "faculty", "academic", "coach"]):
        return "Education"
    if any(k in title for k in ["social work", "counsel", "case manager", "advocate", "community", "youth", "family", "psych", "nonprofit"]):
        return "Social Service"

    if any(k in title for k in ["design", "writ", "editor", "artist", "media", "video", "photog", "journ", "architect", "interior", "fashion"]):
        return "Creative & Media"
    if any(k in title for k in ["legal", "law", "attorney", "paralegal", "compliance"]):
        return "Legal & Policy"

    if any(k in title for k in ["manager", "director", "executive", "chief", "president", "lead", "supervis", "head of", "owner", "founder"]):
        return "Leadership (General)"

    return "Unclassified Jobs"


CAREER_SMALL_TO_LARGE = {
    "Accounting & Audit": "Business & Finance",
    "Finance & Investment": "Business & Finance",
    "Management & Operations": "Business & Finance",
    "Sales & Marketing": "Business & Finance",
    "Leadership (General)": "Business & Finance",
    "Software & Data": "Technology & Engineering",
    "Engineering": "Technology & Engineering",
    "IT & Infrastructure": "Technology & Engineering",
    "Clinical Care": "Healthcare & Science",
    "Research & Science": "Healthcare & Science",
    "Education": "Education & Service",
    "Social Service": "Education & Service",
    "Creative & Media": "Arts, Media & Legal",
    "Legal & Policy": "Arts, Media & Legal",
    "Unclassified Jobs": "Unclassified",
}


def classify_career_large_cluster(job_title: str) -> str:
    small_cluster = map_job_to_small_cluster(job_title)
    return CAREER_SMALL_TO_LARGE.get(small_cluster, "Unclassified")


def load_rows():
    rows = []
    major_catalog = {}
    all_major_counts = Counter()
    with SOURCE_CSV.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            if row["Major Cluster"] != "ARTS, LANGUAGES & THEOLOGY":
                continue

            major = row["Major"].strip()
            subcluster = row["Major Subcluster"].strip()
            major_catalog[major] = subcluster
            all_major_counts[major] += 1
            job_title = (row["Job Title"] or "Unknown").strip() or "Unknown"
            if subcluster == VISIBLE_SUBCLUSTER:
                career_large = classify_career_large_cluster(job_title)
                rows.append(
                    {
                        "major": major,
                        "subcluster": subcluster,
                        "job_title": job_title,
                        "career_large": career_large,
                    }
                )
    return rows, major_catalog, all_major_counts


def write_colors():
    colors = """<colors>
major_arts = 189,110,48
major_writing = 213,147,79
major_languages = 237,199,138

major_arts_a4 = 189,110,48,0.45
major_writing_a4 = 213,147,79,0.45
major_languages_a4 = 237,199,138,0.45

career_business = 162,164,168
career_technology = 152,154,158
career_health = 142,144,148
career_education = 132,134,138
career_arts = 122,124,128
career_unclassified = 176,178,181
</colors>
"""
    (BASE_DIR / "colors.conf").write_text(colors, encoding="ascii")


def write_config(majors_in_order, careers_in_order):
    pairwise_lines = []
    for left, right in zip(careers_in_order, careers_in_order[1:]):
        pairwise_lines.append(
            f"    <pairwise {left['id']} {right['id']}>\n"
            f"      spacing = 2r\n"
            f"    </pairwise>"
        )
    for left, right in zip(majors_in_order, majors_in_order[1:]):
        spacing = "2r" if left["subcluster"] == right["subcluster"] else "4r"
        pairwise_lines.append(
            f"    <pairwise {left['id']} {right['id']}>\n"
            f"      spacing = {spacing}\n"
            f"    </pairwise>"
        )
    pairwise_lines.append(
        f"    <pairwise {careers_in_order[-1]['id']} {majors_in_order[0]['id']}>\n"
        "      spacing = 22r\n"
        "    </pairwise>"
    )
    pairwise_lines.append(
        f"    <pairwise {majors_in_order[-1]['id']} {careers_in_order[0]['id']}>\n"
        "      spacing = 22r\n"
        "    </pairwise>"
    )

    config = f"""karyotype = karyotype.txt
chromosomes_units = 1
chromosomes_display_default = yes

<image>
dir = .
file = arts_theology_native.png
png = yes
svg = yes
radius = 1800p
background = white
angle_offset = 114
auto_alpha_colors = yes
auto_alpha_steps = 5
</image>

<ideogram>
  <spacing>
    default = 0.010r
{chr(10).join(pairwise_lines)}
  </spacing>
radius = 0.87r
  thickness = 48p
  fill = yes
  stroke_color = white
  stroke_thickness = 5p
  show_label = no
  label_font = default
  label_radius = 1.10r
  label_size = 24
  label_parallel = yes
</ideogram>

show_ticks = no
show_tick_labels = no

<links>
<link>
file = links.txt
radius = 0.83r
bezier_radius = 0.18r
thickness = 2
ribbon = yes
flat = yes
stroke_thickness = 0
stroke_color = dgrey
</link>
</links>

<plots>
<plot>
type = text
color = black
file = labels.txt
r0 = 1.04r
r1 = 1.30r
label_size = 18p
label_font = default
show_links = no
padding = 0r
rpadding = 0r
label_snuggle = yes
snuggle_tolerance = 0.6r
max_snuggle_distance = 2r
</plot>
</plots>

<<include colors.conf>>
<<include __CIRCOS_ROOT__/etc/colors_fonts_patterns.conf>>
<<include __CIRCOS_ROOT__/etc/housekeeping.conf>>
"""
    (BASE_DIR / "circos.conf").write_text(config, encoding="ascii")


def build():
    rows, major_catalog, all_major_counts = load_rows()
    if not rows:
        raise SystemExit("No Arts & Theology rows found in source CSV.")

    visible_major_counts = Counter(row["major"] for row in rows)

    career_counts = Counter(row["career_large"] for row in rows)
    scaled_major_counts = scale_counts(all_major_counts, SIDE_TOTAL_UNITS)
    scaled_career_counts = scale_counts(career_counts, SIDE_TOTAL_UNITS)

    majors_in_order = []
    for subcluster in SUBCLUSTER_ORDER:
        names = [name for name, cluster in major_catalog.items() if cluster == subcluster]
        order_lookup = {name: idx for idx, name in enumerate(MAJOR_DISPLAY_ORDER)}
        for major in sorted(
            names,
            key=lambda name: (
                order_lookup.get(name, 999),
                -visible_major_counts.get(name, 0),
                name,
            ),
        ):
            majors_in_order.append(
                {
                    "name": major,
                    "id": f"major_{sanitize_id(major)}",
                    "label": compact_label(major),
                    "size": scaled_major_counts[major],
                    "visible_count": visible_major_counts.get(major, 0),
                    "subcluster": subcluster,
                    "color": SUBCLUSTER_COLORS[subcluster],
                    "visible": subcluster == VISIBLE_SUBCLUSTER,
                }
            )

    careers_in_order = []
    for career in CAREER_ORDER:
        count = career_counts.get(career, 0)
        if count <= 0:
            continue
        careers_in_order.append(
            {
                "name": career,
                "id": f"career_{sanitize_id(career)}",
                "label": compact_label(career),
                "size": scaled_career_counts[career],
                "visible_count": count,
                "color": CAREER_COLORS[career],
            }
        )

    karyotype_lines = []
    for item in majors_in_order:
        karyotype_lines.append(
            f"chr - {item['id']} {item['label']} 0 {item['size']} {item['color']}"
        )
    for item in careers_in_order:
        karyotype_lines.append(
            f"chr - {item['id']} {item['label']} 0 {item['size']} {item['color']}"
        )
    (BASE_DIR / "karyotype.txt").write_text("\n".join(karyotype_lines) + "\n", encoding="ascii")

    major_offsets = {}
    for item in majors_in_order:
        visible = item["visible_count"]
        major_offsets[item["name"]] = max(0, (item["size"] - visible) // 2)

    career_offsets = {}
    for item in careers_in_order:
        visible = item["visible_count"]
        career_offsets[item["name"]] = max(0, (item["size"] - visible) // 2)

    major_id_lookup = {item["name"]: item["id"] for item in majors_in_order}
    major_color_lookup = {
        item["name"]: f"{item['color']}_a4" for item in majors_in_order
    }
    career_id_lookup = {item["name"]: item["id"] for item in careers_in_order}

    sorted_rows = sorted(
        rows,
        key=lambda row: (
            majors_in_order.index(next(item for item in majors_in_order if item["name"] == row["major"])),
            CAREER_ORDER.index(row["career_large"]),
            row["job_title"].lower(),
        ),
    )

    link_lines = []
    for row in sorted_rows:
        major = row["major"]
        career = row["career_large"]

        major_start = major_offsets[major]
        major_end = major_start + 1
        major_offsets[major] = major_end

        career_start = career_offsets[career]
        career_end = career_start + 1
        career_offsets[career] = career_end

        link_lines.append(
            f"{major_id_lookup[major]} {major_start} {major_end} "
            f"{career_id_lookup[career]} {career_start} {career_end} "
            f"color={major_color_lookup[major]}"
        )

    (BASE_DIR / "links.txt").write_text("\n".join(link_lines) + "\n", encoding="ascii")

    label_lines = []
    for item in majors_in_order:
        mid = item["size"] // 2
        label_lines.append(f"{item['id']} {mid} {mid} {item['label']}")
    for item in careers_in_order:
        mid = item["size"] // 2
        label_lines.append(f"{item['id']} {mid} {mid} {item['label']}")
    (BASE_DIR / "labels.txt").write_text("\n".join(label_lines) + "\n", encoding="ascii")

    summary_lines = [
        f"Source CSV: {SOURCE_CSV}",
        f"Filtered rows (visible ribbons from '{VISIBLE_SUBCLUSTER}' only): {len(rows)}",
        "",
        "Major counts:",
    ]
    for item in majors_in_order:
        visibility = "visible ribbons" if item["visible"] else "arc only"
        summary_lines.append(
            f"- {item['name']}: scaled={item['size']}, rows={item['visible_count']} ({item['subcluster']}; {visibility})"
        )
    summary_lines.append("")
    summary_lines.append("Career large-cluster counts:")
    for item in careers_in_order:
        summary_lines.append(f"- {item['name']}: scaled={item['size']}, rows={item['visible_count']}")
    (BASE_DIR / "summary.txt").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    write_colors()
    write_config(majors_in_order, careers_in_order)

    print(f"Wrote Circos files to {BASE_DIR}")
    print(f"Rows visualized: {len(rows)}")


if __name__ == "__main__":
    build()
