# UST Career Pathways Analysis

**Where do our graduates work?**  Maps Majors → Industries → Job Functions for University of St. Thomas alumni.

---

## Quick Start (3 steps)

### 1. Set up the environment

**Option A — Conda (recommended):**
```bash
conda env create -f environment.yml
conda activate ust-career-pathways
```

**Option B — pip:**
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure your data
Open **`settings.py`** and set two things:

```python
# Point at your Excel or CSV file:
INPUT_FILE = "my_data.xlsx"

# Map YOUR column names to ours:
YOUR_COLUMN_NAMES = {
    "major":     "Program Name/Major",   # column with the student's major
    "job_title": "Job Title",            # column with their post-grad job title
    "company":   "Employing Organization",
    # ... see settings.py for all options
}
```

Or leave `INPUT_FILE = None` to use built-in mock data for testing.

### 3. Run
```
python run.py
```

This will:
1. Clean your raw data
2. Classify majors → clusters, companies → industries, titles → job functions
3. Validate the output
4. Launch an interactive dashboard at **http://localhost:8501**

Done.

---

## Command options

| Command | What it does |
|---------|-------------|
| `python run.py` | Full pipeline + dashboard |
| `python run.py --mock` | Use mock data (skip your file) |
| `python run.py --no-dash` | Pipeline only, no dashboard |
| `python run.py --dash` | Dashboard only (skip pipeline) |
| `python run.py --stage 3` | Re-run from stage 3 onward |

---

## Project structure

```
settings.py              ← THE ONE FILE YOU EDIT
run.py                   ← One command to run everything

dashboard/
  app.py                 ← Streamlit entry point
  data_loader.py         ← Auto-loads mock or real data
  config.py              ← Re-exports from settings.py
  components/
    charts.py            ← All Plotly chart functions
    filters.py           ← Sidebar filter widgets
  pages/
    overview.py          ← KPIs, distributions, treemap
    major_industry.py    ← Sankey: Major → Industry
    job_functions.py     ← Job function analysis
    career_pathways.py   ← 3-level Sankey explorer
  mock_data/
    generate_mock.py     ← Synthetic data generator

reproducibility/
  run_pipeline.py        ← Runs all 4 stages
  validate.py            ← Checks outputs are valid
  config.py              ← Re-exports from settings.py
  stages/
    stage_01_clean.py    ← Load + rename + filter
    stage_02_classify.py ← Major/Industry/Job classification
    stage_03_analyze.py  ← Summary statistics & cross-tabs
    stage_04_export.py   ← Final CSV + report

data/                    ← Created by pipeline
  career_outcomes_final.csv
  intermediate/
```

---

## Using your own data

Your input file needs at minimum:
- A column with **student majors** (e.g., "Computer Science")
- A column with **job titles** (e.g., "Software Engineer")

Optional but recommended:
- Company/employer name
- Graduation date or year
- Degree level
- Academic school/division
- Employment state

Open `settings.py` and map your column names — the comments explain each one.

### Improving classification accuracy

The pipeline classifies every row into Major Clusters, Industry Groups, and Job Functions. After your first run, check the terminal output for warnings like:

```
[Stage 02] ⚠️  42 rows have unmapped majors
           → Add them to MAJOR_TO_CLUSTER in stage_02_classify.py
```

Open the relevant file and add your mappings to improve coverage.

---

## Requirements

- Python 3.9+
- streamlit, pandas, plotly, numpy, openpyxl

Install with conda:
```bash
conda env create -f environment.yml
conda activate ust-career-pathways
```
Or with pip: `pip install -r requirements.txt`
