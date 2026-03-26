"""
Generate CSV exports for each major cluster's career destination breakdown
"""

import csv
from pathlib import Path

# Data
major_clusters = [
    "BUSINESS & MANAGEMENT",
    "ENGINEERING & TECHNOLOGY",
    "NATURAL & HEALTH SCIENCES",
    "SOCIAL SCIENCES & HUMANITIES",
    "COMMUNICATION & MEDIA",
    "ARTS, LANGUAGES & THEOLOGY",
    "EDUCATION & SOCIAL SERVICES",
    "Unclassified"
]

career_clusters = [
    "Business & Finance",
    "Technology & Engineering",
    "Healthcare & Science",
    "Education & Service",
    "Arts, Media & Legal",
    "Unclassified"
]

# Flow matrix: Major cluster -> Career cluster
flow_matrix = [
    [480, 45, 35, 18, 8, 984],      # BUSINESS & MANAGEMENT
    [65, 245, 28, 6, 3, 115],       # ENGINEERING & TECHNOLOGY
    [48, 52, 165, 12, 4, 155],      # NATURAL & HEALTH SCIENCES
    [58, 18, 32, 22, 8, 133],       # SOCIAL SCIENCES & HUMANITIES
    [38, 12, 6, 5, 6, 93],          # COMMUNICATION & MEDIA
    [28, 4, 5, 5, 4, 40],           # ARTS, LANGUAGES & THEOLOGY
    [12, 3, 8, 38, 2, 15],          # EDUCATION & SOCIAL SERVICES
    [42, 15, 8, 4, 2, 67]           # Unclassified
]

output_dir = Path(r"C:\Users\hoang\Documents\project_test\csv_exports")
output_dir.mkdir(exist_ok=True)

# Generate individual CSV for each major cluster
for major_idx, major_name in enumerate(major_clusters):
    flows = flow_matrix[major_idx]
    total = sum(flows)

    csv_path = output_dir / f"Major_Career_Analysis_v4__{major_name}.csv"

    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["Major Cluster", "Career Cluster", "Count", "Percentage", "Percentage of Total"])

        for career_idx, career_name in enumerate(career_clusters):
            count = flows[career_idx]
            pct = (count / total * 100) if total > 0 else 0
            writer.writerow([
                major_name,
                career_name,
                count,
                f"{pct:.1f}%",
                f"{count / 3201 * 100:.1f}%"  # Percentage of all graduates
            ])

    print(f"[OK] Created: {csv_path.name} ({total} graduates)")

# Generate consolidated comparison CSV
comparison_path = output_dir / "Major_Career_Analysis_v4__All_Clusters_Comparison.csv"
with open(comparison_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    # Header
    header = ["Major Cluster", "Total Graduates"] + career_clusters
    writer.writerow(header)

    # Data rows
    for major_idx, major_name in enumerate(major_clusters):
        flows = flow_matrix[major_idx]
        total = sum(flows)
        writer.writerow([major_name, total] + flows)

print(f"[OK] Created: {comparison_path.name} (cross-cluster comparison)")

# Generate career destination summary
summary_path = output_dir / "Career_Destination_Summary.csv"
with open(summary_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Career Cluster", "Total Graduates", "Percentage", "Primary Source Major"])

    career_totals = [sum(flow_matrix[m][c] for m in range(len(major_clusters))) for c in range(len(career_clusters))]

    for career_idx, career_name in enumerate(career_clusters):
        total = career_totals[career_idx]
        pct = (total / 3201 * 100)

        # Find which major contributes most to this career
        top_major_idx = max(range(len(major_clusters)),
                           key=lambda m: flow_matrix[m][career_idx])
        top_major = major_clusters[top_major_idx]

        writer.writerow([
            career_name,
            total,
            f"{pct:.1f}%",
            top_major
        ])

print(f"[OK] Created: {summary_path.name} (career destination summary)")

print(f"\n[SUCCESS] All CSVs generated in: {output_dir}")
print(f"Total: {len(major_clusters) + 2} files")
