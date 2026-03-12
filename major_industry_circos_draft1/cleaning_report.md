# Major Data Cleaning Report
**Generated:** 2026-02-26 10:07
**Original dataset:** 137 unique majors, 4129 total students
**Sum of all major counts:** 4129

---
## Step 1: Master's/Graduate Programs Removed

**Total Master's/graduate programs removed:** 21
**Total students in removed programs:** 604

### Clearly Labeled Master's Programs (MBA/MS/Master in name)

| Program | Students | Identification |
|---------|----------|----------------|
| MBA | 181 | Master of Business Administration |
| Executive MBA | 30 | Executive Master of Business Administration |
| Health Care MBA | 58 | Master of Business Administration - Health Care |
| MS Business Analytics | 63 | Master of Science in Business Analytics |
| MS Operations & Supply Chain Mgmt | 61 | Master of Science in Operations & Supply Chain Management |
| Comp Science BS (Master Track) | 1 | Computer Science BS to Master's accelerated track |

### Graduate-Level Programs (typically only offered at graduate level)

| Program | Students | Identification |
|---------|----------|----------------|
| Counseling Psychology | 40 | Typically a Master's/Doctoral program (MA/PhD in Counseling Psychology) |
| Organization Develop & Change | 4 | Typically a Master's program (MA in Organization Development) |
| Organization Development | 1 | Typically a Master's program (MA in Organization Development) |
| Educ Leadership & Learning | 15 | Typically a Master's/Doctoral program (M.Ed./Ed.D.) |
| Educational Leadership & Admin | 3 | Typically a Master's/Doctoral program (M.Ed./Ed.D.) |
| Social Work Advanced Standing | 32 | MSW Advanced Standing (graduate-level social work) |
| U.S. Law | 15 | Graduate-level law program (JD/LLM) |
| Leadership In Student Affairs | 12 | Typically a Master's program (M.A. in Student Affairs) |
| Leadership | 4 | Graduate certificate/program in leadership |
| Leadership & Management | 59 | Graduate program in Leadership & Management |
| Technology Management | 6 | Typically a graduate program (MS in Technology Management) |
| Regulatory Science | 3 | Typically a graduate program (MS in Regulatory Science) |
| Publc Safety & Law Enfr Ldrshp | 3 | Graduate certificate in Public Safety & Law Enforcement Leadership |
| Health Care Innovation | 9 | Typically a graduate program/certificate |
| Software Management | 4 | Typically a graduate program (MS in Software Management) |

### Associate Degree Programs

*No Associate degree programs found in this dataset. This appears to be a 4-year university dataset.*

---
## Step 2: Duplicate Majors Combined

The following majors were identified as duplicates and combined:

### Computer Science (114 students)
**Reason:** Same major with and without (BS) degree suffix

| Original Name | Students |
|---------------|----------|
| Computer Science (BS) | 113 |
| Computer Science | 1 |
| **Combined Total** | **114** |

### Biology (142 students)
**Reason:** Same major with and without (BS) degree suffix

| Original Name | Students |
|---------------|----------|
| Biology (BS) | 99 |
| Biology | 43 |
| **Combined Total** | **142** |

### Physics (6 students)
**Reason:** Same major with and without (BS) degree suffix

| Original Name | Students |
|---------------|----------|
| Physics (BS) | 3 |
| Physics | 3 |
| **Combined Total** | **6** |

### Geology (9 students)
**Reason:** Same major with and without (BS) degree suffix

| Original Name | Students |
|---------------|----------|
| Geology (BS) | 7 |
| Geology | 2 |
| **Combined Total** | **9** |

### Environmental Science (21 students)
**Reason:** Environmental Science with different concentration suffixes - all are the same base major

| Original Name | Students |
|---------------|----------|
| Environmental Sci (Biology) | 9 |
| Environmental Sci (Chemistry) | 1 |
| Environmental Sci (Geoscience) | 9 |
| Environmental Science | 2 |
| **Combined Total** | **21** |

**Total duplicate entries eliminated:** 7
**Total merge operations:** 5

---
## Step 3: Liberal Arts Removed

**Reason:** Professor requested removal - not suitable for analysis.

- Removed **Liberal Arts**: 51 students

---
## Step 4: Special Degrees & Certificates Report

The following programs appear to be non-standard degree types (certificates,
endorsements, or special programs) rather than traditional bachelor's degrees:

### Acad Behavioral Strategist
- **Type:** Graduate Certificate/Endorsement
- **Students:** 53
- **Status:** PRESENT in cleaned data
- **Description:** Academic Behavioral Strategist - a specialized certification/endorsement in special education for behavioral intervention strategies. Often a post-baccalaureate or graduate-level add-on credential.
- **Note:** This may have been retained from graduate data. Consider if it should remain.

### Autism Spectrum Disorders
- **Type:** Graduate Certificate/Endorsement
- **Students:** 4
- **Status:** PRESENT in cleaned data
- **Description:** Autism Spectrum Disorders - a specialized certificate focused on ASD intervention and education. Typically a graduate-level endorsement or certificate program.
- **Note:** This may have been retained from graduate data. Consider if it should remain.

### Early Childhood Special Educ
- **Type:** Licensure/Endorsement Program
- **Students:** 3
- **Status:** PRESENT in cleaned data
- **Description:** Early Childhood Special Education - may function as a teaching licensure or endorsement rather than a standalone bachelor's degree in some institutions.
- **Note:** Could be a valid bachelor's track or a post-bac endorsement.

### Individualized
- **Type:** Special/Self-Designed Degree
- **Students:** 10
- **Status:** PRESENT in cleaned data
- **Description:** Individualized major - a self-designed or interdisciplinary major where students create their own curriculum. This is a valid bachelor's degree but non-standard.
- **Note:** Valid degree type but does not fit neatly into any discipline cluster.

### Catholic Studies
- **Type:** Certificate/Minor that may function as a major
- **Students:** 46
- **Status:** PRESENT in cleaned data
- **Description:** Catholic Studies - often offered as a certificate or minor program. May be combined with another major.
- **Note:** Check if these students also have a primary major listed.

### Family Studies
- **Type:** Certificate or Minor Program
- **Students:** 8
- **Status:** PRESENT in cleaned data
- **Description:** Family Studies - sometimes offered as a certificate or as part of a broader Social Work or Psychology program.
- **Note:** Small program (8 students). May warrant special attention in analysis.

### Pastoral Leadership
- **Type:** Ministry Certificate/Program
- **Students:** 5
- **Status:** PRESENT in cleaned data
- **Description:** Pastoral Leadership - may be a seminary/divinity certificate or a specialized ministry program rather than a traditional academic degree.
- **Note:** Check if this is a bachelor's completion or a certificate program.

### Pastoral Ministry
- **Type:** Ministry Certificate/Program
- **Students:** 1
- **Status:** PRESENT in cleaned data
- **Description:** Pastoral Ministry - similar to Pastoral Leadership, may function as a ministry preparation certificate.
- **Note:** Very small (1 student). May be a certificate completion.

### Legal Studies
- **Type:** Pre-Professional/Certificate Program
- **Students:** 11
- **Status:** PRESENT in cleaned data
- **Description:** Legal Studies - sometimes functions as a pre-law certificate or a paralegal certification rather than a full bachelor's degree.
- **Note:** Could be a valid BA in Legal Studies or a certificate. Verify with registrar data.

> **Recommendation:** Review these programs with your professor to determine
> if any should be excluded from the analysis or reclassified.

---
## Step 5: Economics & Engineering Cluster Restructuring

### Economics - New Independent Small Cluster

Economics and its variants have been separated from the 'Social Sciences' small
cluster into their own 'Economics' small cluster under SOCIAL SCIENCES & HUMANITIES.

| Economics Major | Students |
|----------------|----------|
| Economics | 25 |
| Economics - Business | 44 |
| Economics - International | 5 |
| Economics - Mathematical | 9 |
| Economics - Public Policy | 11 |
| **Total** | **94** |

### Engineering - Confirmed as Independent Small Cluster

'Engineering Disciplines' is confirmed as its own small cluster separate from
'Computer Science & IT'. Computer Engineering moved to Engineering Disciplines.

| Engineering Major | Students |
|-------------------|----------|
| Mechanical Engineering | 228 |
| Electrical Engineering | 72 |
| Civil Engineering | 51 |
| Manufacturing Engineering | 10 |
| Systems Engineering | 6 |
| Computer Engineering | 36 |
| **Total** | **403** |

---
## Summary

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Unique Majors | 137 | 108 | -29 |
| Total Student Records | 4129 | 3474 | -655 |

### Actions Taken
1. **Master's/Graduate programs removed:** 21 programs (604 students)
2. **Duplicate majors combined:** 5 merge operations (7 entries eliminated)
3. **Liberal Arts removed:** 1 program (51 students)
4. **Special degrees/certificates identified:** 9 programs flagged for review
5. **Economics:** Separated into its own small cluster (94 students)
6. **Engineering Disciplines:** Confirmed as own small cluster with Computer Engineering (403 students)

### Remaining Majors (Cleaned)

| # | Major | Students | % of Total |
|---|-------|----------|------------|
| 1 | Financial Management | 373 | 10.74% |
| 2 | Marketing Management | 323 | 9.3% |
| 3 | Mechanical Engineering | 228 | 6.56% |
| 4 | Accounting | 145 | 4.17% |
| 5 | Biology | 142 | 4.09% |
| 6 | Gen Business Mgmt | 124 | 3.57% |
| 7 | Computer Science | 114 | 3.28% |
| 8 | Entrepreneurship | 106 | 3.05% |
| 9 | Psychology | 99 | 2.85% |
| 10 | Social Work | 95 | 2.73% |
| 11 | Actuarial Science | 86 | 2.48% |
| 12 | Data Science | 80 | 2.3% |
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
| 31 | Data Analytics | 29 | 0.83% |
| 32 | Public Health | 26 | 0.75% |
| 33 | Digital Media Arts | 25 | 0.72% |
| 34 | Economics | 25 | 0.72% |
| 35 | Chemistry | 24 | 0.69% |
| 36 | Criminal Justice | 24 | 0.69% |
| 37 | Communication Studies | 23 | 0.66% |
| 38 | Strategic Comm: Ad and PR | 22 | 0.63% |
| 39 | English - Creative Writing | 21 | 0.6% |
| 40 | International Business | 21 | 0.6% |
| 41 | Environmental Science | 21 | 0.6% |
| 42 | COJO Strategic Communications | 20 | 0.58% |
| 43 | English | 18 | 0.52% |
| 44 | History | 18 | 0.52% |
| 45 | Statistics | 18 | 0.52% |
| 46 | Biology of Global Health | 17 | 0.49% |
| 47 | Journalism | 17 | 0.49% |
| 48 | Educational Studies | 14 | 0.4% |
| 49 | Mathematics (Applied Track) | 14 | 0.4% |
| 50 | Middle/Secondary Education | 14 | 0.4% |
| 51 | COJO Journalism | 12 | 0.35% |
| 52 | Environmental Studies | 12 | 0.35% |
| 53 | Economics - Public Policy | 11 | 0.32% |
| 54 | Justice & Peace Studies | 11 | 0.32% |
| 55 | Legal Studies | 11 | 0.32% |
| 56 | Music - Business | 11 | 0.32% |
| 57 | Sociology | 11 | 0.32% |
| 58 | Individualized | 10 | 0.29% |
| 59 | Intl Studies - Pol Sci | 10 | 0.29% |
| 60 | Manufacturing Engineering | 10 | 0.29% |
| 61 | COJO Creative Multimedia | 9 | 0.26% |
| 62 | Economics - Mathematical | 9 | 0.26% |
| 63 | English - Professional Writing | 9 | 0.26% |
| 64 | Health Promotion & Wellness | 9 | 0.26% |
| 65 | Nursing | 9 | 0.26% |
| 66 | Geology | 9 | 0.26% |
| 67 | Family Studies | 8 | 0.23% |
| 68 | COJO Persuasion/Soc Influence | 7 | 0.2% |
| 69 | Music Education | 7 | 0.2% |
| 70 | Information Technology | 6 | 0.17% |
| 71 | Org. Ethics & Compliance | 6 | 0.17% |
| 72 | Systems Engineering | 6 | 0.17% |
| 73 | Physics | 6 | 0.17% |
| 74 | Art History | 5 | 0.14% |
| 75 | Creative Writing & Publishing | 5 | 0.14% |
| 76 | Economics - International | 5 | 0.14% |
| 77 | Geography - Geo Info Sys (GIS) | 5 | 0.14% |
| 78 | Pastoral Leadership | 5 | 0.14% |
| 79 | Spanish Cultural/Literary St. | 5 | 0.14% |
| 80 | Teacher Preparation-Elem K-6 | 5 | 0.14% |
| 81 | Theology | 5 | 0.14% |
| 82 | Autism Spectrum Disorders | 4 | 0.12% |
| 83 | Intl Studies - Economics | 4 | 0.12% |
| 84 | Mathematics (Education Track) | 4 | 0.12% |
| 85 | Teacher Preparation-Secondary | 4 | 0.12% |
| 86 | Business Communication | 3 | 0.09% |
| 87 | Early Childhood Special Educ | 3 | 0.09% |
| 88 | French | 3 | 0.09% |
| 89 | Intl Studies - History | 3 | 0.09% |
| 90 | K-12 Music Education | 3 | 0.09% |
| 91 | Mathematics (Pure Track) | 3 | 0.09% |
| 92 | Music | 3 | 0.09% |
| 93 | Spanish Linguistics/Lang. St. | 3 | 0.09% |
| 94 | Classical Civilization | 2 | 0.06% |
| 95 | Communication and Journalism | 2 | 0.06% |
| 96 | Music - Performance | 2 | 0.06% |
| 97 | Risk Management and Insurance | 2 | 0.06% |
| 98 | Teacher Preparation - K-12 | 2 | 0.06% |
| 99 | COJO Interpersonal Comm | 1 | 0.03% |
| 100 | Family Business | 1 | 0.03% |
| 101 | Geography | 1 | 0.03% |
| 102 | German | 1 | 0.03% |
| 103 | K-12 World Lang. & Cultures | 1 | 0.03% |
| 104 | Mathematics (Statistics Track) | 1 | 0.03% |
| 105 | Pastoral Ministry | 1 | 0.03% |
| 106 | Quant Methods - Computer Sci | 1 | 0.03% |
| 107 | Spanish | 1 | 0.03% |
| 108 | Strategic Communication | 1 | 0.03% |

---
*Cleaned data saved to `data_analysis_results_cleaned.json`*