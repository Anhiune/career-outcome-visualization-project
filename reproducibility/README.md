# Reproducibility Package — UST Career Pathways Analysis

## Overview

This package provides a **fully reproducible pipeline** that transforms raw career-outcomes data into the final dataset consumed by the interactive dashboard.  Every step—from cleaning through classification, analysis, and export—is scripted, parameterized, and version-controlled.

The design follows a **"drop-in" philosophy**: the dashboard and this pipeline share a common schema (`data/career_outcomes_final.csv`).  You can run the dashboard with synthetic mock data today, then re-run the pipeline with real data when it's ready—the dashboard picks it up automatically.

---

## Directory Structure

```
reproducibility/
│
├── config.py               # All paths, parameters, column definitions
├── run_pipeline.py          # End-to-end pipeline runner (CLI)
├── validate.py              # Post-run validation checks
├── README.md                # ← you are here
│
├── stages/
│   ├── stage_01_clean.py    # Raw Excel → cleaned CSV
│   ├── stage_02_classify.py # Add Major Cluster, Industry Group, Job Function
│   ├── stage_03_analyze.py  # Generate analysis JSON (stats, matrices, pathways)
│   └── stage_04_export.py   # Produce final dashboard-ready CSV + report
│
└── reports/                 # Generated after pipeline run
    └── pipeline_report.json
```

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run with mock data (no real data needed)

```bash
# Generate mock data and run the full pipeline
python -m reproducibility.run_pipeline --mock
```

### 3. Validate outputs

```bash
python -m reproducibility.validate
```

### 4. Launch the dashboard

```bash
# The dashboard auto-detects mock vs real data
streamlit run dashboard/app.py
```

---

## Running with Real Data

1. Place the raw Excel file at:
   ```
   data/raw/career_outcomes_raw.xlsx
   ```
   Expected columns: `Program Name/Major`, `Academic Division/School`, `Degree Level`, `Graduation Date`, `Job Title`, `Employing Organization`, `Position Location - State`

2. Run the pipeline:
   ```bash
   python -m reproducibility.run_pipeline
   ```

3. Switch the dashboard to real data:  
   Edit `dashboard/config.py`:
   ```python
   DATA_SOURCE = "real"
   ```

4. Launch the dashboard:
   ```bash
   streamlit run dashboard/app.py
   ```

---

## Pipeline Stages

| Stage | Script | Input | Output | Description |
|-------|--------|-------|--------|-------------|
| 01 | `stage_01_clean.py` | Raw Excel | `data/intermediate/01_cleaned.csv` | Filter undergrads, merge duplicates, standardize columns |
| 02 | `stage_02_classify.py` | Cleaned CSV | `data/intermediate/02_classified.csv` | Add Major Cluster (7), Industry Group (10), Job Function (21) |
| 03 | `stage_03_analyze.py` | Classified CSV | `data/intermediate/03_analysis.json` | Cross-tabs, top pathways, diversity scores, trends |
| 04 | `stage_04_export.py` | Classified CSV | `data/career_outcomes_final.csv` | Final schema alignment + pipeline report |

### Running individual stages

```bash
python -m reproducibility.stages.stage_01_clean
python -m reproducibility.stages.stage_02_classify
python -m reproducibility.stages.stage_03_analyze
python -m reproducibility.stages.stage_04_export
```

### Resuming from a specific stage

```bash
python -m reproducibility.run_pipeline --stage 3  # skip stages 01–02
```

---

## Configuration

All parameters are in `reproducibility/config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `exclude_degree_levels` | Master's, Doctorate, Certificate | Degree levels to filter out |
| `min_major_count` | 1 | Drop majors with fewer students |
| `merge_duplicates` | True | Merge known duplicate major names |
| `industry_group_count` | 10 | Target number of industry groups |
| `job_function_count` | 21 | Target number of job function categories |
| `top_n_majors` | 20 | Number of top majors in analysis output |
| `top_n_pathways` | 20 | Number of top pathways in analysis output |

---

## Data Schema

The final output CSV (`data/career_outcomes_final.csv`) has these columns:

| Column | Type | Description |
|--------|------|-------------|
| Major | string | Student's undergraduate major |
| Major Cluster | string | One of 7 tier-3 clusters |
| Major Subcluster | string | One of ~29 tier-2 clusters |
| Academic Division | string | College/school within the university |
| Degree Level | string | Bachelor's, etc. |
| Graduation Year | int | Year of graduation |
| Job Title | string | Post-graduation job title |
| Job Function | string | One of 21 classified functions |
| Company | string | Employing organization |
| Industry Group | string | One of 10 industry groups |
| State | string | US state of employment |

---

## Extending the Pipeline

### Adding new company → industry mappings

Edit the `COMPANY_INDUSTRY_STUB` dictionary in `stage_02_classify.py`, or import the full mapping from the existing `classify_companies_jobs.py`.

### Adding new job title rules

Add regex patterns to the `JOB_TITLE_RULES` list in `stage_02_classify.py`.

### Adding new major → cluster mappings

Extend the `MAJOR_TO_CLUSTER` dictionary in `stage_02_classify.py`.

---

## Validation

`validate.py` checks:
- All intermediate and final output files exist
- Final CSV has the correct columns
- No null values in critical fields
- Multiple categories present in cluster/industry/function columns
- Analysis JSON contains expected keys

```bash
python -m reproducibility.validate
# Exit code 0 = all checks pass
```
