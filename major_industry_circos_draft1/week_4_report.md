# Week 4 Report — Major Data Cleaning & Restructuring
**Date:** February 26, 2026  
**Project:** Major-Industry Career Pathway Analysis  

---

## 1. Overview

This report documents all data cleaning operations performed on the major dataset during Week 4. The goal was to prepare a clean, accurate dataset of undergraduate majors for the career pathway visualization by removing graduate-level programs, merging duplicate entries, eliminating unsuitable majors, and restructuring cluster groupings.

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Unique Majors | 137 | 108 | -29 |
| Total Student Records | 4,129 | 3,474 | -655 |

---

## 2. Master's & Graduate Programs Removed

**21 programs removed** — 604 students total.

These entries represent graduate-level degrees (Master's, MBA, MS, JD/LLM, graduate certificates) that were mixed into the dataset alongside undergraduate majors and needed to be separated out.

### 2.1 Clearly Labeled Master's Programs (MBA/MS in name)

| Program | Students | Identification |
|---------|----------|----------------|
| MBA | 181 | Master of Business Administration |
| Executive MBA | 30 | Executive Master of Business Administration |
| Health Care MBA | 58 | Master of Business Administration — Health Care |
| MS Business Analytics | 63 | Master of Science in Business Analytics |
| MS Operations & Supply Chain Mgmt | 61 | Master of Science in Operations & Supply Chain Management |
| Comp Science BS (Master Track) | 1 | Computer Science BS-to-Master's accelerated track |

### 2.2 Graduate-Level Programs (by program type)

| Program | Students | Identification |
|---------|----------|----------------|
| Counseling Psychology | 40 | MA/PhD in Counseling Psychology |
| Organization Develop & Change | 4 | MA in Organization Development |
| Organization Development | 1 | MA in Organization Development |
| Educ Leadership & Learning | 15 | M.Ed./Ed.D. program |
| Educational Leadership & Admin | 3 | M.Ed./Ed.D. program |
| Social Work Advanced Standing | 32 | MSW Advanced Standing |
| U.S. Law | 15 | JD/LLM law program |
| Leadership In Student Affairs | 12 | MA in Student Affairs |
| Leadership | 4 | Graduate certificate/program |
| Leadership & Management | 59 | Graduate program |
| Technology Management | 6 | MS in Technology Management |
| Regulatory Science | 3 | MS in Regulatory Science |
| Publc Safety & Law Enfr Ldrshp | 3 | Graduate certificate |
| Health Care Innovation | 9 | Graduate program/certificate |
| Software Management | 4 | MS in Software Management |

### 2.3 Associate Degree Programs

No Associate degree programs were found. This dataset is from a 4-year university.

---

## 3. Duplicate Majors Combined

**5 merge operations** performed — 7 duplicate entries eliminated.

Several majors appeared multiple times under slightly different names (typically with and without a "(BS)" degree suffix, or with different concentration labels). These were identified and merged into a single entry.

### 3.1 Computer Science
**Reason:** Same major listed with and without (BS) degree suffix.

| Original Name | Students |
|---------------|----------|
| Computer Science (BS) | 113 |
| Computer Science | 1 |
| **Combined → Computer Science** | **114** |

### 3.2 Biology
**Reason:** Same major listed with and without (BS) degree suffix.

| Original Name | Students |
|---------------|----------|
| Biology (BS) | 99 |
| Biology | 43 |
| **Combined → Biology** | **142** |

### 3.3 Physics
**Reason:** Same major listed with and without (BS) degree suffix.

| Original Name | Students |
|---------------|----------|
| Physics (BS) | 3 |
| Physics | 3 |
| **Combined → Physics** | **6** |

### 3.4 Geology
**Reason:** Same major listed with and without (BS) degree suffix.

| Original Name | Students |
|---------------|----------|
| Geology (BS) | 7 |
| Geology | 2 |
| **Combined → Geology** | **9** |

### 3.5 Environmental Science
**Reason:** Same base major with different concentration suffixes — all Environmental Science.

| Original Name | Students |
|---------------|----------|
| Environmental Sci (Biology) | 9 |
| Environmental Sci (Chemistry) | 1 |
| Environmental Sci (Geoscience) | 9 |
| Environmental Science | 2 |
| **Combined → Environmental Science** | **21** |

---

## 4. Liberal Arts Major Removed

**Reason:** Professor requested removal — not suitable for this analysis.

| Major | Students Removed |
|-------|-----------------|
| Liberal Arts | 51 |

---

## 5. Special Degrees & Certificates Identified

The following 9 programs were flagged as potentially non-standard degree types (certificates, endorsements, or special programs) that may not represent traditional bachelor's degrees. They remain in the dataset pending review.

| Program | Type | Students | Notes |
|---------|------|----------|-------|
| Acad Behavioral Strategist | Graduate Certificate/Endorsement | 53 | Specialized special education endorsement; may have been retained from graduate data |
| Autism Spectrum Disorders | Graduate Certificate/Endorsement | 4 | Specialized ASD certificate; typically graduate-level |
| Early Childhood Special Educ | Licensure/Endorsement | 3 | Could be a valid bachelor's track or post-bac endorsement |
| Individualized | Self-Designed Degree | 10 | Valid bachelor's but non-standard; student-designed curriculum |
| Catholic Studies | Certificate/Minor as Major | 46 | Often offered as a certificate or minor; check if students have a primary major |
| Family Studies | Certificate/Minor | 8 | Sometimes part of Social Work or Psychology programs |
| Pastoral Leadership | Ministry Certificate | 5 | May be seminary/divinity certificate rather than academic degree |
| Pastoral Ministry | Ministry Certificate | 1 | Similar to Pastoral Leadership; very small program |
| Legal Studies | Pre-Professional/Certificate | 11 | Could be valid BA or a paralegal certificate |

> **Recommendation:** Review these programs with your professor to determine if any should be excluded or reclassified.

---

## 6. Cluster Restructuring

Two key changes were made to the small cluster groupings:

### 6.1 Economics — New Independent Small Cluster

Economics and its variants were separated from the "Social Sciences" small cluster into their own **"Economics"** small cluster under SOCIAL SCIENCES & HUMANITIES. This reflects that Economics functions as a distinct discipline with its own career pathways.

| Economics Major | Students |
|----------------|----------|
| Economics | 25 |
| Economics - Business | 44 |
| Economics - International | 5 |
| Economics - Mathematical | 9 |
| Economics - Public Policy | 11 |
| **Total** | **94** |

### 6.2 Engineering Disciplines — Confirmed as Independent Small Cluster

"Engineering Disciplines" was confirmed as its own small cluster, separate from "Computer Science & IT." Computer Engineering was moved from the CS/IT cluster into Engineering Disciplines where it fits more naturally.

| Engineering Major | Students |
|-------------------|----------|
| Mechanical Engineering | 228 |
| Electrical Engineering | 72 |
| Civil Engineering | 51 |
| Computer Engineering | 36 |
| Manufacturing Engineering | 10 |
| Systems Engineering | 6 |
| **Total** | **403** |

---

## 7. Final Cleaned Major List

108 unique majors remain after all cleaning operations. Top 30 by enrollment:

| # | Major | Students | % of Total |
|---|-------|----------|------------|
| 1 | Financial Management | 373 | 10.74% |
| 2 | Marketing Management | 323 | 9.30% |
| 3 | Mechanical Engineering | 228 | 6.56% |
| 4 | Accounting | 145 | 4.17% |
| 5 | Biology | 142 | 4.09% |
| 6 | Gen Business Mgmt | 124 | 3.57% |
| 7 | Computer Science | 114 | 3.28% |
| 8 | Entrepreneurship | 106 | 3.05% |
| 9 | Psychology | 99 | 2.85% |
| 10 | Social Work | 95 | 2.73% |
| 11 | Actuarial Science | 86 | 2.48% |
| 12 | Data Science | 80 | 2.30% |
| 13 | Electrical Engineering | 72 | 2.07% |
| 14 | Neuroscience | 68 | 1.96% |
| 15 | Exercise Science | 64 | 1.84% |
| 16 | Operations Management | 55 | 1.58% |
| 17 | Acad Behavioral Strategist | 53 | 1.53% |
| 18 | Civil Engineering | 51 | 1.47% |
| 19 | Human Resources Management | 51 | 1.47% |
| 20 | Political Science | 50 | 1.44% |
| 21 | Catholic Studies | 46 | 1.32% |
| 22 | Economics - Business | 44 | 1.27% |
| 23 | Biochemistry | 41 | 1.18% |
| 24 | Philosophy | 39 | 1.12% |
| 25 | Software Engineering | 39 | 1.12% |
| 26 | Real Estate Studies | 37 | 1.07% |
| 27 | Computer Engineering | 36 | 1.04% |
| 28 | Elementary Education (K-6) | 32 | 0.92% |
| 29 | Bus Admin - Communication | 31 | 0.89% |
| 30 | Law & Compliance | 30 | 0.86% |

---

## 8. Files Modified

| File | Change |
|------|--------|
| `data_analysis_results_cleaned.json` | New cleaned dataset (108 majors, 3,474 students) |
| `clean_majors.py` | New reusable cleaning script |
| `create_analysis_excel.py` | Updated large & small cluster definitions |
| `unified_dashboard.py` | Updated large & small cluster definitions |
| `update_analysis.py` | Updated cluster definitions, cleaning logic, graduate program filter |

---

*End of Week 4 Report*
