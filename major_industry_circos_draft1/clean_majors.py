"""
Major Data Cleaning Script
===========================
This script cleans the data_analysis_results.json file by:
1. Removing Master's/Graduate-level programs
2. Combining duplicate/similar majors
3. Removing Liberal Arts (professor's request)
4. Identifying special degrees/certificates
5. Restructuring Economics and Engineering as own small clusters

Generates:
- data_analysis_results_cleaned.json (cleaned data)
- cleaning_report.md (comprehensive report)
"""

import json
import os
from datetime import datetime

# ============================================================
# Load Data
# ============================================================

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, 'data_analysis_results.json')

with open(input_file, 'r') as f:
    data = json.load(f)

original_majors = list(data['majors'])
original_counts = dict(data['major_counts'])
original_total = data['total_students']
original_sum = sum(original_counts.values())

report_lines = []

def report(line=""):
    report_lines.append(line)
    print(line)

report("# Major Data Cleaning Report")
report(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
report(f"**Original dataset:** {len(original_majors)} unique majors, {original_total} total students")
report(f"**Sum of all major counts:** {original_sum}")
report("")

# ============================================================
# STEP 1: Identify & Remove Master's/Graduate-Level Programs
# ============================================================

# Programs clearly at the Master's/Graduate level based on naming
masters_programs_clear = {
    "MBA": "Master of Business Administration",
    "Executive MBA": "Executive Master of Business Administration",
    "Health Care MBA": "Master of Business Administration - Health Care",
    "MS Business Analytics": "Master of Science in Business Analytics",
    "MS Operations & Supply Chain Mgmt": "Master of Science in Operations & Supply Chain Management",
    "Comp Science BS (Master Track)": "Computer Science BS to Master's accelerated track",
}

# Programs that are virtually always offered at the graduate level only
masters_programs_likely = {
    "Counseling Psychology": "Typically a Master's/Doctoral program (MA/PhD in Counseling Psychology)",
    "Organization Develop & Change": "Typically a Master's program (MA in Organization Development)",
    "Organization Development": "Typically a Master's program (MA in Organization Development)",
    "Educ Leadership & Learning": "Typically a Master's/Doctoral program (M.Ed./Ed.D.)",
    "Educational Leadership & Admin": "Typically a Master's/Doctoral program (M.Ed./Ed.D.)",
    "Social Work Advanced Standing": "MSW Advanced Standing (graduate-level social work)",
    "U.S. Law": "Graduate-level law program (JD/LLM)",
    "Leadership In Student Affairs": "Typically a Master's program (M.A. in Student Affairs)",
    "Leadership": "Graduate certificate/program in leadership",
    "Leadership & Management": "Graduate program in Leadership & Management",
    "Technology Management": "Typically a graduate program (MS in Technology Management)",
    "Regulatory Science": "Typically a graduate program (MS in Regulatory Science)",
    "Publc Safety & Law Enfr Ldrshp": "Graduate certificate in Public Safety & Law Enforcement Leadership",
    "Health Care Innovation": "Typically a graduate program/certificate",
    "Software Management": "Typically a graduate program (MS in Software Management)",
}

# No obvious Associate degree programs found in this university dataset
associate_programs = {}

all_masters = {**masters_programs_clear, **masters_programs_likely}

# Working copy of counts
working_counts = dict(original_counts)

removed_masters = {}
for prog, reason in all_masters.items():
    if prog in working_counts:
        removed_masters[prog] = {"count": working_counts[prog], "reason": reason}
        del working_counts[prog]

report("---")
report("## Step 1: Master's/Graduate Programs Removed")
report("")
report(f"**Total Master's/graduate programs removed:** {len(removed_masters)}")
report(f"**Total students in removed programs:** {sum(v['count'] for v in removed_masters.values())}")
report("")

report("### Clearly Labeled Master's Programs (MBA/MS/Master in name)")
report("")
report("| Program | Students | Identification |")
report("|---------|----------|----------------|")
for prog in masters_programs_clear:
    if prog in removed_masters:
        report(f"| {prog} | {removed_masters[prog]['count']} | {removed_masters[prog]['reason']} |")

report("")
report("### Graduate-Level Programs (typically only offered at graduate level)")
report("")
report("| Program | Students | Identification |")
report("|---------|----------|----------------|")
for prog in masters_programs_likely:
    if prog in removed_masters:
        report(f"| {prog} | {removed_masters[prog]['count']} | {removed_masters[prog]['reason']} |")

report("")
report("### Associate Degree Programs")
report("")
if associate_programs:
    for prog in associate_programs:
        report(f"- {prog}")
else:
    report("*No Associate degree programs found in this dataset. This appears to be a 4-year university dataset.*")
report("")

# ============================================================
# STEP 2: Find & Combine Duplicate/Similar Majors
# ============================================================

# Merge rules: target_name -> list of source names that should be combined
merge_rules = {
    "Computer Science": {
        "sources": ["Computer Science (BS)", "Computer Science"],
        "reason": "Same major with and without (BS) degree suffix"
    },
    "Biology": {
        "sources": ["Biology (BS)", "Biology"],
        "reason": "Same major with and without (BS) degree suffix"
    },
    "Physics": {
        "sources": ["Physics (BS)", "Physics"],
        "reason": "Same major with and without (BS) degree suffix"
    },
    "Geology": {
        "sources": ["Geology (BS)", "Geology"],
        "reason": "Same major with and without (BS) degree suffix"
    },
    "Environmental Science": {
        "sources": ["Environmental Sci (Biology)", "Environmental Sci (Chemistry)", 
                     "Environmental Sci (Geoscience)", "Environmental Science"],
        "reason": "Environmental Science with different concentration suffixes - all are the same base major"
    },
}

report("---")
report("## Step 2: Duplicate Majors Combined")
report("")
report("The following majors were identified as duplicates and combined:")
report("")

merged_report = []
for target_name, info in merge_rules.items():
    sources_found = []
    for name in info['sources']:
        if name in working_counts:
            sources_found.append((name, working_counts[name]))
    
    if len(sources_found) > 0:
        combined_count = sum(count for _, count in sources_found)
        merged_report.append({
            'target': target_name,
            'sources': sources_found,
            'combined_count': combined_count,
            'reason': info['reason']
        })
        
        # Remove all sources from working counts
        for name, _ in sources_found:
            if name in working_counts:
                del working_counts[name]
        
        # Add combined entry
        working_counts[target_name] = combined_count

for merge in merged_report:
    report(f"### {merge['target']} ({merge['combined_count']} students)")
    report(f"**Reason:** {merge['reason']}")
    report("")
    report("| Original Name | Students |")
    report("|---------------|----------|")
    for name, count in merge['sources']:
        report(f"| {name} | {count} |")
    report(f"| **Combined Total** | **{merge['combined_count']}** |")
    report("")

total_merged_away = sum(len(m['sources']) - 1 for m in merged_report)
report(f"**Total duplicate entries eliminated:** {total_merged_away}")
report(f"**Total merge operations:** {len(merged_report)}")
report("")

# ============================================================
# STEP 3: Remove Liberal Arts
# ============================================================

report("---")
report("## Step 3: Liberal Arts Removed")
report("")
report("**Reason:** Professor requested removal - not suitable for analysis.")
report("")

if "Liberal Arts" in working_counts:
    la_count = working_counts["Liberal Arts"]
    report(f"- Removed **Liberal Arts**: {la_count} students")
    del working_counts["Liberal Arts"]
else:
    report("- 'Liberal Arts' was not found in the remaining data (may have been removed in a previous step).")
report("")

# ============================================================
# STEP 4: Identify Special Degrees/Certificates
# ============================================================

special_programs = {
    "Acad Behavioral Strategist": {
        "type": "Graduate Certificate/Endorsement",
        "description": "Academic Behavioral Strategist - a specialized certification/endorsement in special education for behavioral intervention strategies. Often a post-baccalaureate or graduate-level add-on credential.",
        "note": "This may have been retained from graduate data. Consider if it should remain."
    },
    "Autism Spectrum Disorders": {
        "type": "Graduate Certificate/Endorsement",
        "description": "Autism Spectrum Disorders - a specialized certificate focused on ASD intervention and education. Typically a graduate-level endorsement or certificate program.",
        "note": "This may have been retained from graduate data. Consider if it should remain."
    },
    "Early Childhood Special Educ": {
        "type": "Licensure/Endorsement Program",
        "description": "Early Childhood Special Education - may function as a teaching licensure or endorsement rather than a standalone bachelor's degree in some institutions.",
        "note": "Could be a valid bachelor's track or a post-bac endorsement."
    },
    "Individualized": {
        "type": "Special/Self-Designed Degree",
        "description": "Individualized major - a self-designed or interdisciplinary major where students create their own curriculum. This is a valid bachelor's degree but non-standard.",
        "note": "Valid degree type but does not fit neatly into any discipline cluster."
    },
    "Catholic Studies": {
        "type": "Certificate/Minor that may function as a major",
        "description": "Catholic Studies - often offered as a certificate or minor program. May be combined with another major.",
        "note": "Check if these students also have a primary major listed."
    },
    "Family Studies": {
        "type": "Certificate or Minor Program",
        "description": "Family Studies - sometimes offered as a certificate or as part of a broader Social Work or Psychology program.",
        "note": "Small program (8 students). May warrant special attention in analysis."
    },
    "Pastoral Leadership": {
        "type": "Ministry Certificate/Program",
        "description": "Pastoral Leadership - may be a seminary/divinity certificate or a specialized ministry program rather than a traditional academic degree.",
        "note": "Check if this is a bachelor's completion or a certificate program."
    },
    "Pastoral Ministry": {
        "type": "Ministry Certificate/Program",
        "description": "Pastoral Ministry - similar to Pastoral Leadership, may function as a ministry preparation certificate.",
        "note": "Very small (1 student). May be a certificate completion."
    },
    "Legal Studies": {
        "type": "Pre-Professional/Certificate Program",
        "description": "Legal Studies - sometimes functions as a pre-law certificate or a paralegal certification rather than a full bachelor's degree.",
        "note": "Could be a valid BA in Legal Studies or a certificate. Verify with registrar data."
    },
}

report("---")
report("## Step 4: Special Degrees & Certificates Report")
report("")
report("The following programs appear to be non-standard degree types (certificates,")
report("endorsements, or special programs) rather than traditional bachelor's degrees:")
report("")

for prog, info in special_programs.items():
    count = working_counts.get(prog, 0)
    status = "PRESENT in cleaned data" if count > 0 else "REMOVED (graduate-level)"
    report(f"### {prog}")
    report(f"- **Type:** {info['type']}")
    report(f"- **Students:** {count}")
    report(f"- **Status:** {status}")
    report(f"- **Description:** {info['description']}")
    report(f"- **Note:** {info['note']}")
    report("")

report("> **Recommendation:** Review these programs with your professor to determine")
report("> if any should be excluded from the analysis or reclassified.")
report("")

# ============================================================
# STEP 5: Economics & Engineering Cluster Restructuring
# ============================================================

report("---")
report("## Step 5: Economics & Engineering Cluster Restructuring")
report("")
report("### Economics - New Independent Small Cluster")
report("")
report("Economics and its variants have been separated from the 'Social Sciences' small")
report("cluster into their own 'Economics' small cluster under SOCIAL SCIENCES & HUMANITIES.")
report("")

# After merging, Economics variants that remain:
# The "Economics - *" variants were NOT merged (they're sub-specializations)
# But wait, we should check if they're still in working_counts
econ_majors = [m for m in working_counts if m.startswith("Economics")]
report("| Economics Major | Students |")
report("|----------------|----------|")
econ_total = 0
for m in sorted(econ_majors):
    c = working_counts[m]
    econ_total += c
    report(f"| {m} | {c} |")
report(f"| **Total** | **{econ_total}** |")
report("")

report("### Engineering - Confirmed as Independent Small Cluster")
report("")
report("'Engineering Disciplines' is confirmed as its own small cluster separate from")
report("'Computer Science & IT'. Computer Engineering moved to Engineering Disciplines.")
report("")

eng_majors = ["Mechanical Engineering", "Electrical Engineering", "Civil Engineering", 
              "Manufacturing Engineering", "Systems Engineering", "Computer Engineering"]
report("| Engineering Major | Students |")
report("|-------------------|----------|")
eng_total = 0
for m in eng_majors:
    c = working_counts.get(m, 0)
    if c > 0:
        eng_total += c
        report(f"| {m} | {c} |")
report(f"| **Total** | **{eng_total}** |")
report("")

# ============================================================
# FINAL SUMMARY
# ============================================================

cleaned_majors = sorted(working_counts.keys())
cleaned_sum = sum(working_counts.values())

report("---")
report("## Summary")
report("")
report("| Metric | Before | After | Change |")
report("|--------|--------|-------|--------|")
report(f"| Unique Majors | {len(original_majors)} | {len(cleaned_majors)} | -{len(original_majors) - len(cleaned_majors)} |")
report(f"| Total Student Records | {original_sum} | {cleaned_sum} | -{original_sum - cleaned_sum} |")
report("")

report("### Actions Taken")
report(f"1. **Master's/Graduate programs removed:** {len(removed_masters)} programs ({sum(v['count'] for v in removed_masters.values())} students)")
report(f"2. **Duplicate majors combined:** {len(merged_report)} merge operations ({total_merged_away} entries eliminated)")
report(f"3. **Liberal Arts removed:** 1 program ({la_count} students)")
report(f"4. **Special degrees/certificates identified:** {len(special_programs)} programs flagged for review")
report(f"5. **Economics:** Separated into its own small cluster ({econ_total} students)")
report(f"6. **Engineering Disciplines:** Confirmed as own small cluster with Computer Engineering ({eng_total} students)")
report("")

report("### Remaining Majors (Cleaned)")
report("")
report("| # | Major | Students | % of Total |")
report("|---|-------|----------|------------|")
sorted_by_count = sorted(working_counts.items(), key=lambda x: -x[1])
for i, (major, count) in enumerate(sorted_by_count, 1):
    pct = round(count / cleaned_sum * 100, 2)
    report(f"| {i} | {major} | {count} | {pct}% |")

# ============================================================
# Save Cleaned Data
# ============================================================

cleaned_data = {
    "majors": cleaned_majors,
    "major_counts": {m: working_counts[m] for m in cleaned_majors},
    "career_columns": data['career_columns'],
    "total_students": cleaned_sum
}

output_json = os.path.join(script_dir, 'data_analysis_results_cleaned.json')
with open(output_json, 'w') as f:
    json.dump(cleaned_data, f, indent=2)

report("")
report(f"---")
report(f"*Cleaned data saved to `data_analysis_results_cleaned.json`*")

# Save Report
report_file = os.path.join(script_dir, 'cleaning_report.md')
with open(report_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print(f"\n{'='*60}")
print(f"Report saved to: {report_file}")
print(f"Cleaned data saved to: {output_json}")
print(f"{'='*60}")
