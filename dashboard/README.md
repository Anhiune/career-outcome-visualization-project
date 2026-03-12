# Dashboard — UST Career Pathways

Interactive Streamlit dashboard for exploring career outcomes of University of St. Thomas graduates.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch (uses mock data by default)
streamlit run dashboard/app.py
```

## Structure

```
dashboard/
├── app.py              # Main entry point (multi-page Streamlit app)
├── config.py           # All constants, schemas, color palettes
├── data_loader.py      # Loads mock or real data (swap with one toggle)
├── components/
│   ├── charts.py       # Reusable Plotly chart functions
│   └── filters.py      # Sidebar filter widgets
├── mock_data/
│   ├── generate_mock.py   # Generates realistic synthetic dataset
│   └── mock_dataset.csv   # Pre-generated mock data (auto-created)
└── pages/
    ├── overview.py         # KPIs, distributions, trends
    ├── major_industry.py   # Sankey, heatmap, stacked bars
    ├── job_functions.py    # Function distribution, sunburst
    └── career_pathways.py  # 3-level Sankey, drill-down, pathway search
```

## Switching to Real Data

1. Run the reproducibility pipeline (see `reproducibility/README.md`)
2. Edit `dashboard/config.py`:
   ```python
   DATA_SOURCE = "real"
   ```
3. Re-launch: `streamlit run dashboard/app.py`

## Pages

| Page | Description |
|------|-------------|
| **Overview** | KPI cards, cluster/industry bar charts, treemap, graduation trends |
| **Major → Industry** | Sankey diagram, heatmap, stacked percentage bars |
| **Job Functions** | Horizontal bar chart, cluster × function heatmap, sunburst |
| **Career Pathways** | 3-level Sankey, per-major drill-down, pathway search tool |
