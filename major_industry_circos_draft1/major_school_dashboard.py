import pandas as pd
import holoviews as hv
from holoviews import opts, dim
import os

# Initialize HoloViews with Bokeh backend
hv.extension('bokeh')

# Paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
INFILE = os.path.join(PROJECT_DIR, "Ire Anh Data 1.22.26 (1).xlsx")
OUTPUT_HTML = os.path.join(PROJECT_DIR, "major_school_dashboard.html")

print(f"Loading data from {INFILE}...")

# Load and Preprocess Data
try:
    # Use openpyxl as engine for xlsx files
    df = pd.read_excel(INFILE, engine='openpyxl')
except Exception as e:
    print(f"Error loading Excel file: {e}")
    # Fallback to default if engine not specified/installed
    df = pd.read_excel(INFILE)

# Identify required columns
major_col = 'Program Name/Major'
school_col = 'Academic Division/School'

# Check if columns exist
if major_col not in df.columns or school_col not in df.columns:
    print(f"Error: Required columns not found. Available columns: {df.columns.tolist()}")
    exit(1)

# Drop missing values and strip whitespace
df = df[[major_col, school_col]].dropna()
df[major_col] = df[major_col].astype(str).str.strip()
df[school_col] = df[school_col].astype(str).str.strip()

# Aggregate data for the Chord diagram
# Source: Program Name/Major, Target: Academic Division/School
flows = df.groupby([major_col, school_col]).size().reset_index(name="count")

print(f"Processing {len(flows)} unique major-school connections...")

# Create a dataset for HoloViews
chord_data = hv.Dataset(flows, [major_col, school_col], 'count')

# Create the Chord diagram
chord = hv.Chord(chord_data)

# Customize styling
chord_opts = opts.Chord(
    cmap='Category20', 
    edge_cmap='Category20', 
    edge_color=dim(major_col).str(), 
    labels='label', 
    node_color=dim('index').str(),
    width=900, 
    height=900,
    title="Interactive Major-School Connections",
    label_text_font_size='10pt'
)

visual = chord.opts(chord_opts)

print(f"Generating dashboard at {OUTPUT_HTML}...")

# Save to HTML
hv.save(visual, OUTPUT_HTML)

print(f"Done! Open {os.path.basename(OUTPUT_HTML)} to view the visualization.")
