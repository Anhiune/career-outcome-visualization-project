# Incoming → Graduating Major: Grouping Analysis & Decision Document

## 1. Visualization Objective

**What this visualization shows:** How students' majors change from when they *enter* the university (incoming/declared major) to when they *graduate* (final major on record).

**Target Audience:**
- Academic advisors (understanding major migration patterns)
- Prospective students & families (seeing where students end up)
- Department chairs & deans (retention and recruitment insights)
- University leadership (enrollment planning, resource allocation)

**Key Questions This Should Answer:**
1. Which majors retain the most students from entry to graduation?
2. Where do students migrate *to* when they switch out of a major?
3. Where do students migrate *from* when they switch into a major?
4. Are there predictable "pipelines" between academic areas?
5. Which major groups are net gainers vs. net losers of students?

---

## 2. Why the Existing Groupings Don't Work As-Is

The current Major → Industry circos uses **7 major clusters** designed for *career outcome analysis*:

| Existing Cluster | Designed For |
|---|---|
| ARTS, LANGUAGES & THEOLOGY | Career mapping |
| BUSINESS & MANAGEMENT | Career mapping |
| COMMUNICATION & MEDIA | Career mapping |
| EDUCATION & SOCIAL SERVICES | Career mapping |
| ENGINEERING & TECHNOLOGY | Career mapping |
| NATURAL & HEALTH SCIENCES | Career mapping |
| SOCIAL SCIENCES & HUMANITIES | Career mapping |

### Problems with reusing these for Incoming → Graduating:

1. **Both sides are majors.** In the existing circos, one side = majors, other side = industries. Here, both sides are the *same set* of major groups. The diagram must show flows *within and between* the same categories.

2. **Imbalanced sizes.** BUSINESS & MANAGEMENT has 1,758 students vs. COMMUNICATION & MEDIA with 165. This creates an unreadable circos where one arc dominates.

3. **"Unclassified" bucket.** The current grouping puts Leadership & Management, Mathematics, Statistics, Legal Studies, and others in "Unclassified" — these are real majors that need proper homes.

4. **Different audience, different logic.** Career outcomes group by *employment sector*. Major migration should group by *academic affinity* — what fields are intellectually adjacent and likely migration paths.

5. **Incoming majors may include categories not in graduating data.** Students may enter as "Undeclared," "Exploratory," "Pre-Med," "Pre-Law," etc. — categories that don't appear in the graduation data. The grouping must accommodate these.

---

## 3. Complete Major Inventory (91 Graduating Majors)

All majors from the dataset, sorted by count:

| # | Major | Count | Current Cluster |
|---|---|---|---|
| 1 | Financial Management | 370 | BUSINESS & MANAGEMENT |
| 2 | Marketing Management | 323 | BUSINESS & MANAGEMENT |
| 3 | Mechanical Engineering | 209 | ENGINEERING & TECHNOLOGY |
| 4 | Accounting | 145 | BUSINESS & MANAGEMENT |
| 5 | Biology | 142 | NATURAL & HEALTH SCIENCES |
| 6 | Gen Business Mgmt | 124 | BUSINESS & MANAGEMENT |
| 7 | Computer Science | 114 | ENGINEERING & TECHNOLOGY |
| 8 | Entrepreneurship | 106 | BUSINESS & MANAGEMENT |
| 9 | Psychology | 99 | SOCIAL SCIENCES & HUMANITIES |
| 10 | Economics | 94 | BUSINESS & MANAGEMENT |
| 11 | Actuarial Science | 86 | BUSINESS & MANAGEMENT |
| 12 | Neuroscience | 68 | NATURAL & HEALTH SCIENCES |
| 13 | Exercise Science | 64 | NATURAL & HEALTH SCIENCES |
| 14 | MS Operations & Supply Chain Mgmt | 61 | BUSINESS & MANAGEMENT |
| 15 | Leadership & Management | 59 | Unclassified |
| 16 | Operations Management | 55 | BUSINESS & MANAGEMENT |
| 17 | Electrical Engineering | 51 | ENGINEERING & TECHNOLOGY |
| 18 | Civil Engineering | 51 | ENGINEERING & TECHNOLOGY |
| 19 | Human Resources Management | 51 | BUSINESS & MANAGEMENT |
| 20 | Political Science | 50 | SOCIAL SCIENCES & HUMANITIES |
| 21 | Biochemistry | 41 | NATURAL & HEALTH SCIENCES |
| 22 | Philosophy | 39 | SOCIAL SCIENCES & HUMANITIES |
| 23 | Real Estate Studies | 37 | BUSINESS & MANAGEMENT |
| 24 | Computer Engineering | 36 | ENGINEERING & TECHNOLOGY |
| 25 | Elementary Education (K-6) | 32 | EDUCATION & SOCIAL SERVICES |
| 26 | Bus Admin - Communication | 31 | BUSINESS & MANAGEMENT |
| 27 | Law & Compliance | 30 | BUSINESS & MANAGEMENT |
| 28 | Catholic Studies | 30 | ARTS, LANGUAGES & THEOLOGY |
| 29 | Data Analytics | 29 | BUSINESS & MANAGEMENT |
| 30 | Social Work | 26 | EDUCATION & SOCIAL SERVICES |
| 31 | Public Health | 26 | NATURAL & HEALTH SCIENCES |
| 32 | Digital Media Arts | 25 | COMMUNICATION & MEDIA |
| 33 | Chemistry | 24 | NATURAL & HEALTH SCIENCES |
| 34 | Criminal Justice | 24 | SOCIAL SCIENCES & HUMANITIES |
| 35 | Communication Studies | 23 | COMMUNICATION & MEDIA |
| 36 | Mathematics | 22 | Unclassified |
| 37 | Strategic Comm: Ad and PR | 22 | COMMUNICATION & MEDIA |
| 38 | English - Creative Writing | 21 | COMMUNICATION & MEDIA |
| 39 | International Business | 21 | BUSINESS & MANAGEMENT |
| 40 | COJO Strategic Communications | 20 | COMMUNICATION & MEDIA |
| 41 | History | 18 | SOCIAL SCIENCES & HUMANITIES |
| 42 | Statistics | 18 | Unclassified |
| 43 | Biology of Global Health | 17 | NATURAL & HEALTH SCIENCES |
| 44 | Journalism | 17 | COMMUNICATION & MEDIA |
| 45 | English | 14 | ARTS, LANGUAGES & THEOLOGY |
| 46 | Middle/Secondary Education | 14 | EDUCATION & SOCIAL SERVICES |
| 47 | COJO Journalism | 12 | COMMUNICATION & MEDIA |
| 48 | Environmental Studies | 12 | NATURAL & HEALTH SCIENCES |
| 49 | Justice & Peace Studies | 11 | SOCIAL SCIENCES & HUMANITIES |
| 50 | Music - Business | 11 | ARTS, LANGUAGES & THEOLOGY |
| 51 | Sociology | 11 | SOCIAL SCIENCES & HUMANITIES |
| 52 | Intl Studies - Pol Sci | 10 | SOCIAL SCIENCES & HUMANITIES |
| 53 | Individualized | 10 | Unclassified |
| 54 | Legal Studies | 10 | Unclassified |
| 55 | Geology | 9 | NATURAL & HEALTH SCIENCES |
| 56 | COJO Creative Multimedia | 9 | COMMUNICATION & MEDIA |
| 57 | Environmental Sci (Geoscience) | 9 | Unclassified |
| 58 | English - Professional Writing | 9 | ARTS, LANGUAGES & THEOLOGY |
| 59 | Health Promotion & Wellness | 9 | NATURAL & HEALTH SCIENCES |
| 60 | Environmental Sci (Biology) | 9 | NATURAL & HEALTH SCIENCES |
| 61 | Family Studies | 8 | Unclassified |
| 62 | COJO Persuasion/Soc Influence | 7 | COMMUNICATION & MEDIA |
| 63 | Physics | 6 | NATURAL & HEALTH SCIENCES |
| 64 | Geography - Geo Info Sys (GIS) | 5 | NATURAL & HEALTH SCIENCES |
| 65 | Spanish Cultural/Literary St. | 5 | ARTS, LANGUAGES & THEOLOGY |
| 66 | Intl Studies - Economics | 4 | SOCIAL SCIENCES & HUMANITIES |
| 67 | Intl Studies - History | 3 | SOCIAL SCIENCES & HUMANITIES |
| 68 | Theology | 3 | ARTS, LANGUAGES & THEOLOGY |
| 69 | Business Communication | 3 | BUSINESS & MANAGEMENT |
| 70 | K-12 Music Education | 3 | EDUCATION & SOCIAL SERVICES |
| 71 | Spanish Linguistics/Lang. St. | 3 | ARTS, LANGUAGES & THEOLOGY |
| 72 | French | 3 | ARTS, LANGUAGES & THEOLOGY |
| 73 | Music | 3 | ARTS, LANGUAGES & THEOLOGY |
| 74 | Social Work Advanced Standing | 2 | EDUCATION & SOCIAL SERVICES |
| 75 | Art History | 2 | ARTS, LANGUAGES & THEOLOGY |
| 76 | Risk Management and Insurance | 2 | BUSINESS & MANAGEMENT |
| 77 | Communication and Journalism | 2 | COMMUNICATION & MEDIA |
| 78 | Environmental Science | 2 | NATURAL & HEALTH SCIENCES |
| 79 | Music - Performance | 2 | ARTS, LANGUAGES & THEOLOGY |
| 80 | Classical Civilization | 2 | SOCIAL SCIENCES & HUMANITIES |
| 81 | Comp Science BS (Master Track) | 1 | Unclassified |
| 82 | Family Business | 1 | BUSINESS & MANAGEMENT |
| 83 | Quant Methods - Computer Sci | 1 | ENGINEERING & TECHNOLOGY |
| 84 | K-12 World Lang. & Cultures | 1 | EDUCATION & SOCIAL SERVICES |
| 85 | German | 1 | ARTS, LANGUAGES & THEOLOGY |
| 86 | MS Business Analytics | 1 | BUSINESS & MANAGEMENT |
| 87 | Environmental Sci (Chemistry) | 1 | Unclassified |
| 88 | COJO Interpersonal Comm | 1 | COMMUNICATION & MEDIA |
| 89 | Geography | 1 | NATURAL & HEALTH SCIENCES |
| 90 | Strategic Communication | 1 | COMMUNICATION & MEDIA |
| 91 | Nursing | 1 | NATURAL & HEALTH SCIENCES |

---

## 4. Design Constraints for Incoming → Graduating Circos

| Constraint | Requirement |
|---|---|
| **Max groups** | 8–12 arcs per side. More than ~12 makes the circos unreadable. |
| **Size balance** | No single group should exceed ~30% of total. Ideal: each group = 5–15% of total. |
| **Semantic clarity** | Groups must be intuitively understandable to a general audience (not just registrar staff). |
| **Migration logic** | Groups should cluster majors that share *academic prerequisites* and *likely switch paths*, not career outcomes. |
| **Symmetry** | The same grouping must work on BOTH sides (incoming and graduating), since students switch within the same taxonomy. |
| **Accommodate incoming-only categories** | The incoming side will likely include "Undeclared / Exploratory," "Pre-Professional" tracks, etc. Reserve slots for these. |

---

## 5. Proposed Grouping: Option A — 10 Academic Divisions

This grouping prioritizes **academic affinity** (students switching between related fields) and **visual balance**.

### Grouping Table

| Group # | Group Name | Majors Included | Graduating Count | % of Total |
|---|---|---|---|---|
| **1** | **Finance & Accounting** | Financial Management, Accounting, Actuarial Science, Risk Management and Insurance | 603 | 18.8% |
| **2** | **Marketing & Business Operations** | Marketing Management, Gen Business Mgmt, Entrepreneurship, Bus Admin - Communication, Business Communication, Family Business, International Business, Real Estate Studies, MS Business Analytics | 667 | 20.8% |
| **3** | **Management & Analytics** | MS Operations & Supply Chain Mgmt, Operations Management, Human Resources Management, Leadership & Management, Data Analytics, Statistics, Law & Compliance, Legal Studies, Economics | 451 | 14.1% |
| **4** | **Engineering** | Mechanical Engineering, Electrical Engineering, Civil Engineering, Computer Engineering | 347 | 10.8% |
| **5** | **Computer Science & Math** | Computer Science, Comp Science BS (Master Track), Quant Methods - Computer Sci, Mathematics | 138 | 4.3% |
| **6** | **Biological & Health Sciences** | Biology, Neuroscience, Biochemistry, Biology of Global Health, Exercise Science, Public Health, Health Promotion & Wellness, Environmental Sci (Biology), Nursing | 355 | 11.1% |
| **7** | **Physical & Environmental Sciences** | Chemistry, Physics, Geology, Environmental Studies, Environmental Sci (Geoscience), Environmental Sci (Chemistry), Environmental Science, Geography, Geography - Geo Info Sys (GIS) | 64 | 2.0% |
| **8** | **Communication & Media** | Communication Studies, Strategic Comm: Ad and PR, COJO Strategic Communications, Digital Media Arts, Journalism, COJO Journalism, COJO Creative Multimedia, English - Creative Writing, COJO Persuasion/Soc Influence, Communication and Journalism, COJO Interpersonal Comm, Strategic Communication | 170 | 5.3% |
| **9** | **Social Sciences & Public Affairs** | Psychology, Political Science, Criminal Justice, Social Work, Social Work Advanced Standing, Justice & Peace Studies, Sociology, Family Studies, Intl Studies - Pol Sci, Intl Studies - Economics, Intl Studies - History, Individualized | 260 | 8.1% |
| **10** | **Arts, Humanities & Languages** | Catholic Studies, Philosophy, History, English, English - Professional Writing, Music - Business, Music, Music - Performance, Art History, Classical Civilization, Theology, Spanish Cultural/Literary St., Spanish Linguistics/Lang. St., French, German, K-12 Music Education, K-12 World Lang. & Cultures, Elementary Education (K-6), Middle/Secondary Education | 163 | 5.1% |

> **Note:** "Undeclared / Exploratory" will appear on the incoming side only, once data is available.

### Size Distribution Analysis

```
Finance & Accounting         ████████████████████  18.8%
Marketing & Business Ops     █████████████████████ 20.8%
Management & Analytics       ██████████████       14.1%
Engineering                  ███████████          10.8%
Computer Science & Math      ████                  4.3%
Biological & Health Sciences ███████████          11.1%
Physical & Env Sciences      ██                    2.0%
Communication & Media        █████                 5.3%
Social Sciences & Public     ████████              8.1%
Arts, Humanities & Lang.     █████                 5.1%
```

### Pros
- Groups reflect *academic adjacency* (where students are likely to switch)
- Business mega-cluster is split into 3 logical sub-groups (Finance, Marketing/General, Management/Analytics)
- Education majors placed with Humanities (their academic home) rather than isolated
- Previously "Unclassified" majors are all assigned

### Cons
- Physical & Environmental Sciences group is very small (2.0%) — thin arc on circos
- Business still dominates with 3 groups totaling ~54%
- Computer Science & Math is also small (4.3%)

---

## 6. Proposed Grouping: Option B — 8 Balanced Divisions (Recommended)

This grouping prioritizes **visual balance** — merging small groups and splitting large ones.

### Grouping Table

| Group # | Group Name | Majors Included | Graduating Count | % of Total |
|---|---|---|---|---|
| **1** | **Finance & Accounting** | Financial Management, Accounting, Actuarial Science, Economics, Risk Management and Insurance | 697 | 21.8% |
| **2** | **Business & Marketing** | Marketing Management, Gen Business Mgmt, Entrepreneurship, Bus Admin - Communication, Business Communication, International Business, Real Estate Studies, Family Business, MS Business Analytics | 667 | 20.8% |
| **3** | **Operations, Analytics & Law** | MS Operations & Supply Chain Mgmt, Operations Management, Human Resources Management, Leadership & Management, Data Analytics, Statistics, Mathematics, Law & Compliance, Legal Studies | 451 | 14.1% |
| **4** | **Engineering & Computer Science** | Mechanical Engineering, Electrical Engineering, Civil Engineering, Computer Engineering, Computer Science, Comp Science BS (Master Track), Quant Methods - Computer Sci | 463 | 14.5% |
| **5** | **Biological & Health Sciences** | Biology, Neuroscience, Biochemistry, Biology of Global Health, Exercise Science, Public Health, Health Promotion & Wellness, Environmental Sci (Biology), Nursing | 355 | 11.1% |
| **6** | **Physical, Environmental & Quantitative Sciences** | Chemistry, Physics, Geology, Environmental Studies, Environmental Sci (Geoscience), Environmental Sci (Chemistry), Environmental Science, Geography, Geography - Geo Info Sys (GIS) | 64 | 2.0% |
| **7** | **Communication, Media & Writing** | Communication Studies, Strategic Comm: Ad and PR, COJO Strategic Communications, COJO Persuasion/Soc Influence, COJO Interpersonal Comm, Strategic Communication, Communication and Journalism, Digital Media Arts, Journalism, COJO Journalism, COJO Creative Multimedia, English - Creative Writing, English, English - Professional Writing | 184 | 5.7% |
| **8** | **Social Sciences, Humanities & Education** | Psychology, Political Science, Criminal Justice, Social Work, Social Work Advanced Standing, Justice & Peace Studies, Sociology, Family Studies, Individualized, Intl Studies - Pol Sci, Intl Studies - Economics, Intl Studies - History, Philosophy, History, Classical Civilization, Catholic Studies, Theology, Music - Business, Music, Music - Performance, Art History, Spanish Cultural/Literary St., Spanish Linguistics/Lang. St., French, German, K-12 Music Education, K-12 World Lang. & Cultures, Elementary Education (K-6), Middle/Secondary Education | 423 | 13.2% |

> **Note:** "Undeclared / Exploratory" will appear on the incoming side only.

### Size Distribution Analysis

```
Finance & Accounting         █████████████████████ 21.8%
Business & Marketing         ████████████████████  20.8%
Operations, Analytics & Law  ██████████████       14.1%
Engineering & CS             ██████████████       14.5%
Biological & Health Sci      ███████████          11.1%
Physical & Env Sciences      ██                    2.0%
Communication & Media        ██████                5.7%
Soc Sci, Humanities & Ed     █████████████        13.2%
```

### Pros
- Only 8 groups = cleaner circos visual
- Better balance (most groups 11–22%)
- Engineering + CS merged = realistic switch pathway
- Social Sciences + Humanities + Education = captures liberal arts migration
- No "Unclassified" bucket

### Cons
- Physical & Environmental Sciences still small (2.0%) — consider merging with Biological & Health Sciences
- Social Sciences, Humanities & Education is a catch-all (very diverse internally)

---

## 7. Proposed Grouping: Option C — 8 Groups, Maximum Balance

Optimized to eliminate the tiny Physical & Env Sciences group.

### Grouping Table

| Group # | Group Name | Abbrev (for circos label) | Majors Included | Count | % |
|---|---|---|---|---|---|
| **1** | **Finance & Accounting** | FIN | Financial Management, Accounting, Actuarial Science, Economics, Risk Management and Insurance | 697 | 21.8% |
| **2** | **Business & Marketing** | BUS | Marketing Management, Gen Business Mgmt, Entrepreneurship, Bus Admin - Communication, Business Communication, International Business, Real Estate Studies, Family Business, MS Business Analytics | 667 | 20.8% |
| **3** | **Operations, Analytics & Law** | OPS | MS Operations & Supply Chain Mgmt, Operations Management, Human Resources Management, Leadership & Management, Data Analytics, Statistics, Mathematics, Law & Compliance, Legal Studies | 451 | 14.1% |
| **4** | **Engineering & Computer Science** | ENG | Mechanical Engineering, Electrical Engineering, Civil Engineering, Computer Engineering, Computer Science, Comp Science BS (Master Track), Quant Methods - Computer Sci | 463 | 14.5% |
| **5** | **Sciences & Health** | SCI | Biology, Neuroscience, Biochemistry, Biology of Global Health, Exercise Science, Public Health, Health Promotion & Wellness, Nursing, Environmental Sci (Biology), Chemistry, Physics, Geology, Environmental Studies, Environmental Sci (Geoscience), Environmental Sci (Chemistry), Environmental Science, Geography, Geography - Geo Info Sys (GIS) | 419 | 13.1% |
| **6** | **Communication, Media & Writing** | COM | Communication Studies, Strategic Comm: Ad and PR, COJO Strategic Communications, COJO Persuasion/Soc Influence, COJO Interpersonal Comm, Strategic Communication, Communication and Journalism, Digital Media Arts, Journalism, COJO Journalism, COJO Creative Multimedia, English - Creative Writing, English, English - Professional Writing | 184 | 5.7% |
| **7** | **Social Sciences & Public Affairs** | SOC | Psychology, Political Science, Criminal Justice, Social Work, Social Work Advanced Standing, Justice & Peace Studies, Sociology, Family Studies, Individualized, Intl Studies - Pol Sci, Intl Studies - Economics, Intl Studies - History | 260 | 8.1% |
| **8** | **Arts, Humanities & Education** | AHE | Philosophy, History, Classical Civilization, Catholic Studies, Theology, Music - Business, Music, Music - Performance, Art History, Spanish Cultural/Literary St., Spanish Linguistics/Lang. St., French, German, K-12 Music Education, K-12 World Lang. & Cultures, Elementary Education (K-6), Middle/Secondary Education | 163 | 5.1% |

> **Incoming-only group (when data available):** "Undeclared / Exploratory" — students who enter without a declared major.

### Size Distribution Analysis

```
Finance & Accounting          █████████████████████ 21.8%
Business & Marketing          ████████████████████  20.8%
Operations, Analytics & Law   ██████████████       14.1%
Engineering & Computer Sci    ██████████████       14.5%
Sciences & Health             █████████████        13.1%
Communication, Media & Writ.  ██████                5.7%
Social Sciences & Pub Affairs ████████              8.1%
Arts, Humanities & Education  █████                 5.1%
```

### Pros
- **Best balance**: Range is 5.1% – 21.8% (no 2% sliver)
- All sciences united — reflects that Bio↔Chem↔Physics switches are common
- Clear, intuitive group names
- Short abbreviations for circos labels
- 8 groups = optimal for readability

### Cons
- Business still split 3 ways (intentional — it's 54% of graduates; a single "Business" arc would dwarf everything)
- Communication, Media & Writing and Arts, Humanities & Education are on the small side

---

## 8. Decision Matrix

| Criteria (weight) | Option A (10 groups) | Option B (8 groups) | Option C (8 groups, balanced) |
|---|---|---|---|
| Visual balance (30%) | ⬤⬤◯ Phys/Env Sci = 2% | ⬤⬤◯ Phys/Env Sci = 2% | ⬤⬤⬤ No group < 5% |
| Readability (25%) | ⬤⬤◯ 10 arcs is dense | ⬤⬤⬤ 8 arcs, clean | ⬤⬤⬤ 8 arcs, clean |
| Academic affinity (20%) | ⬤⬤⬤ Fine-grained | ⬤⬤◯ Humanities+Ed is broad | ⬤⬤⬤ All groups coherent |
| Audience clarity (15%) | ⬤⬤◯ Too many groups to scan | ⬤⬤⬤ Easy to understand | ⬤⬤⬤ Easy to understand |
| Accommodates incoming data (10%) | ⬤⬤⬤ Room for Undeclared | ⬤⬤⬤ Room for Undeclared | ⬤⬤⬤ Room for Undeclared |
| **Weighted Score** | **2.30** | **2.55** | **2.85** |

### ✅ Recommendation: **Option C**

---

## 9. Mapping Reference Table (Option C)

This is the complete mapping of every major → group for implementation.

```
GROUP: Finance & Accounting (FIN)
  - Financial Management
  - Accounting
  - Actuarial Science
  - Economics
  - Risk Management and Insurance

GROUP: Business & Marketing (BUS)
  - Marketing Management
  - Gen Business Mgmt
  - Entrepreneurship
  - Bus Admin - Communication
  - Business Communication
  - International Business
  - Real Estate Studies
  - Family Business
  - MS Business Analytics

GROUP: Operations, Analytics & Law (OPS)
  - MS Operations & Supply Chain Mgmt
  - Operations Management
  - Human Resources Management
  - Leadership & Management
  - Data Analytics
  - Statistics
  - Mathematics
  - Law & Compliance
  - Legal Studies

GROUP: Engineering & Computer Science (ENG)
  - Mechanical Engineering
  - Electrical Engineering
  - Civil Engineering
  - Computer Engineering
  - Computer Science
  - Comp Science BS (Master Track)
  - Quant Methods - Computer Sci

GROUP: Sciences & Health (SCI)
  - Biology
  - Neuroscience
  - Biochemistry
  - Biology of Global Health
  - Exercise Science
  - Public Health
  - Health Promotion & Wellness
  - Nursing
  - Environmental Sci (Biology)
  - Chemistry
  - Physics
  - Geology
  - Environmental Studies
  - Environmental Sci (Geoscience)
  - Environmental Sci (Chemistry)
  - Environmental Science
  - Geography
  - Geography - Geo Info Sys (GIS)

GROUP: Communication, Media & Writing (COM)
  - Communication Studies
  - Strategic Comm: Ad and PR
  - COJO Strategic Communications
  - COJO Persuasion/Soc Influence
  - COJO Interpersonal Comm
  - Strategic Communication
  - Communication and Journalism
  - Digital Media Arts
  - Journalism
  - COJO Journalism
  - COJO Creative Multimedia
  - English - Creative Writing
  - English
  - English - Professional Writing

GROUP: Social Sciences & Public Affairs (SOC)
  - Psychology
  - Political Science
  - Criminal Justice
  - Social Work
  - Social Work Advanced Standing
  - Justice & Peace Studies
  - Sociology
  - Family Studies
  - Individualized
  - Intl Studies - Pol Sci
  - Intl Studies - Economics
  - Intl Studies - History

GROUP: Arts, Humanities & Education (AHE)
  - Philosophy
  - History
  - Classical Civilization
  - Catholic Studies
  - Theology
  - Music - Business
  - Music
  - Music - Performance
  - Art History
  - Spanish Cultural/Literary St.
  - Spanish Linguistics/Lang. St.
  - French
  - German
  - K-12 Music Education
  - K-12 World Lang. & Cultures
  - Elementary Education (K-6)
  - Middle/Secondary Education

INCOMING-ONLY (when data available):
  - Undeclared / Exploratory
  - Pre-Professional (Pre-Med, Pre-Law, Pre-Dental, etc.)
```

---

## 10. Open Questions & Next Steps

### Data Needed
- [ ] Incoming major data (what major did each student declare upon entry?)
- [ ] Student-level linkage (same student's incoming major ↔ graduating major)
- [ ] Cohort scope (which graduation years? Same 2021–2024 window?)
- [ ] Should "Undeclared" be its own group, or split into the group they *eventually* join?

### Design Decisions Still Pending
- [ ] Color palette for 8 groups (keep consistent with existing circos, or new palette?)
- [ ] Whether to show self-loops (students who stay in the same group)
- [ ] Minimum threshold for showing a flow (e.g., ignore flows < 5 students?)
- [ ] Whether the circos should show absolute counts or percentages
- [ ] Label placement strategy — abbreviated labels on arcs, full names in legend?

### Implementation Steps (Once Data Available)
1. Obtain incoming-major-to-graduating-major paired data
2. Apply this grouping to both incoming and graduating sides
3. Build flow matrix (group_incoming × group_graduating)
4. Generate karyotype + links files for Circos
5. Render and iterate on visual design

---

## 11. Appendix: Grouping Rationale by Major

| Major | Assigned Group | Rationale |
|---|---|---|
| Financial Management | FIN | Core finance |
| Accounting | FIN | Core finance |
| Actuarial Science | FIN | Quantitative finance |
| Economics | FIN | Economics → Finance is the most common switch path |
| Risk Management and Insurance | FIN | Financial risk |
| Marketing Management | BUS | Core business |
| Gen Business Mgmt | BUS | General business |
| Entrepreneurship | BUS | Business venture |
| Bus Admin - Communication | BUS | Business administration track |
| Business Communication | BUS | Business administration track |
| International Business | BUS | Business specialization |
| Real Estate Studies | BUS | Business specialization |
| Family Business | BUS | Business specialization |
| MS Business Analytics | BUS | Graduate business track |
| MS Operations & Supply Chain Mgmt | OPS | Operations discipline |
| Operations Management | OPS | Operations discipline |
| Human Resources Management | OPS | Organizational management |
| Leadership & Management | OPS | Organizational management |
| Data Analytics | OPS | Quantitative/analytical |
| Statistics | OPS | Quantitative, often switches with Data Analytics |
| Mathematics | OPS | Quantitative, applied math → analytics pipeline |
| Law & Compliance | OPS | Regulatory/professional |
| Legal Studies | OPS | Regulatory/professional |
| Mechanical Engineering | ENG | Core engineering |
| Electrical Engineering | ENG | Core engineering |
| Civil Engineering | ENG | Core engineering |
| Computer Engineering | ENG | Engineering + CS overlap |
| Computer Science | ENG | CS ↔ Engineering is a common switch |
| Comp Science BS (Master Track) | ENG | CS variant |
| Quant Methods - Computer Sci | ENG | CS variant |
| Biology | SCI | Core biological science |
| Neuroscience | SCI | Biological science |
| Biochemistry | SCI | Biological science |
| Biology of Global Health | SCI | Health-focused biology |
| Exercise Science | SCI | Health science |
| Public Health | SCI | Health science |
| Health Promotion & Wellness | SCI | Health science |
| Nursing | SCI | Health profession |
| Environmental Sci (Biology) | SCI | Environmental/biological |
| Chemistry | SCI | Physical science |
| Physics | SCI | Physical science |
| Geology | SCI | Earth science |
| Environmental Studies | SCI | Environmental science |
| Environmental Sci (Geoscience) | SCI | Environmental science |
| Environmental Sci (Chemistry) | SCI | Environmental science |
| Environmental Science | SCI | Environmental science |
| Geography | SCI | Earth/environmental |
| Geography - Geo Info Sys (GIS) | SCI | Applied geography |
| Communication Studies | COM | Core communication |
| Strategic Comm: Ad and PR | COM | Communication specialization |
| COJO Strategic Communications | COM | Communication specialization |
| COJO Persuasion/Soc Influence | COM | Communication specialization |
| COJO Interpersonal Comm | COM | Communication specialization |
| Strategic Communication | COM | Communication specialization |
| Communication and Journalism | COM | Communication/journalism |
| Digital Media Arts | COM | Media production |
| Journalism | COM | Journalism/media |
| COJO Journalism | COM | Journalism/media |
| COJO Creative Multimedia | COM | Media production |
| English - Creative Writing | COM | Writing → media pipeline |
| English | COM | English → writing/media pipeline |
| English - Professional Writing | COM | Writing specialization |
| Psychology | SOC | Core social science |
| Political Science | SOC | Core social science |
| Criminal Justice | SOC | Applied social science |
| Social Work | SOC | Applied social science |
| Social Work Advanced Standing | SOC | Applied social science |
| Justice & Peace Studies | SOC | Social justice focus |
| Sociology | SOC | Core social science |
| Family Studies | SOC | Applied social science |
| Individualized | SOC | Often social-science oriented self-design |
| Intl Studies - Pol Sci | SOC | Political/international studies |
| Intl Studies - Economics | SOC | International studies |
| Intl Studies - History | SOC | International studies |
| Philosophy | AHE | Core humanities |
| History | AHE | Core humanities |
| Classical Civilization | AHE | Humanities |
| Catholic Studies | AHE | Theology/humanities |
| Theology | AHE | Theology/humanities |
| Music - Business | AHE | Arts |
| Music | AHE | Arts |
| Music - Performance | AHE | Arts |
| Art History | AHE | Arts/humanities |
| Spanish Cultural/Literary St. | AHE | Languages |
| Spanish Linguistics/Lang. St. | AHE | Languages |
| French | AHE | Languages |
| German | AHE | Languages |
| K-12 Music Education | AHE | Education/arts |
| K-12 World Lang. & Cultures | AHE | Education/languages |
| Elementary Education (K-6) | AHE | Education |
| Middle/Secondary Education | AHE | Education |
