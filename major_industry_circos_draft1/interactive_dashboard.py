import pandas as pd
import holoviews as hv
from holoviews import opts, dim
import os

# Initialize HoloViews with Bokeh backend
hv.extension('bokeh')

# Paths
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_DIR, "data")
INFILE = os.path.join(DATA_DIR, "college.txt")
OUTPUT_HTML = os.path.join(PROJECT_DIR, "interactive_dashboard.html")

print(f"Loading data from {INFILE}...")

# Load and Preprocess Data
df = pd.read_csv(INFILE)
df.columns = [c.strip().lower() for c in df.columns]
df = df[["major", "industry"]].dropna()

# Mapping dictionaries (Same as your Circos script)
major_map = {1: "Major 1", 2: "Major 2", 3: "Major 3", 4: "Major 4"}
industry_map = {1: "Industry 1", 2: "Industry 2", 3: "Industry 3", 4: "Industry 4", 5: "Industry 5", 6: "Industry 6"}

# Apply mappings
df["major"] = df["major"].astype(int).map(major_map).fillna(df["major"].astype(str).radd("Major "))
df["industry"] = df["industry"].astype(int).map(industry_map).fillna(df["industry"].astype(str).radd("Industry "))

# Aggregate data for the Chord diagram
# We need columns: [source, target, value]
flows = df.groupby(["major", "industry"]).size().reset_index(name="count")

# Create a dataset for HoloViews
# The Chord element expects a DataFrame with Source, Target, Value columns
chord_data = hv.Dataset(flows, ['major', 'industry'], 'count')

# Create the Chord diagram
chord = hv.Chord(chord_data).select(value=(1, None)) # Filter out 0 flows if any

# Customize styling
# - cmap='Category20': Distinct colors
# - edge_cmap='Category20': Color ribbons by source
# - labels='label': Show labels on the nodes
# - node_color: Color nodes by their index/category
chord_opts = opts.Chord(
    cmap='Category20', 
    edge_cmap='Category20', 
    edge_color=dim('major').str(), 
    labels='label', 
    node_color=dim('index').str(),
    width=800, 
    height=800,
    title="Interactive Major-Industry Connections"
)

visual = chord.opts(chord_opts)

print(f"Generating dashboard at {OUTPUT_HTML}...")

# Save to HTML
hv.save(visual, OUTPUT_HTML)

print("Done! Open interactive_dashboard.html to view the visualization.")
