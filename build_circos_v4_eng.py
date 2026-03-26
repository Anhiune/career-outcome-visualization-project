import os
import pandas as pd
from pathlib import Path
import subprocess

# Directories
BASE_DIR = Path(r"c:\Users\hoang\Documents\project_test\major_industry_circos_draft1")
RAW_DATA_PATH = Path(r"c:\Users\hoang\Documents\project_test\data\career_outcomes_final.csv")
CUSTOM_DIR = BASE_DIR / "custom_circos_v4_eng"
CUSTOM_DIR.mkdir(parents=True, exist_ok=True)

# Aesthetic Colors (from Implementation Plan)
MAJOR_COLORS = {
    "COMMUNICATION & MEDIA": "74,123,183",      # Blue
    "ARTS, LANGUAGES & THEOLOGY": "230,208,172", # Tan
    "SOCIAL SCIENCES & HUMANITIES": "216,133,59", # Orange
    "BUSINESS & MANAGEMENT": "171,73,24",       # Brown
    "EDUCATION & SOCIAL SERVICES": "187,217,177", # Light Green
    "NATURAL & HEALTH SCIENCES": "107,176,92",   # Green
    "ENGINEERING & TECHNOLOGY": "128,130,133",   # Dark Grey
    "Unclassified": "167,169,172",              # Light Grey
}
CAREER_COLOR_RGB = "147,149,152"  # Medium grey

# Target
TARGET_MAJOR_CLUSTER = "ENGINEERING & TECHNOLOGY"

def build_files():
    print("Loading raw data...")
    df = pd.read_csv(RAW_DATA_PATH)
    
    # Career Clusters mapping (from earlier data exploration)
    # We need to map 'Industry Group' to the broader V4 Career Clusters if possible, 
    # or just use Industry Group names.
    # The user rule for V4 was: "knowing what job tile go to what industry int eh forht data"
    # Actually, let's use 'Industry Group' (the 1 of 10 categories) as the targets.
    
    df_filtered = df[df['Major Cluster'] == TARGET_MAJOR_CLUSTER].copy()
    
    majors = [TARGET_MAJOR_CLUSTER]
    careers = sorted(df_filtered['Industry Group'].dropna().unique())
    
    major_totals = df_filtered.groupby("Major Cluster").size()
    career_totals = df_filtered.groupby("Industry Group").size()
    
    # 1. KARYOTYPE
    karyotype_lines = []
    major_ids = {TARGET_MAJOR_CLUSTER: "major_0"}
    karyotype_lines.append(f"chr - major_0 {TARGET_MAJOR_CLUSTER.replace(' ', '_')} 0 {major_totals[TARGET_MAJOR_CLUSTER]} cm_0\n")
    
    career_ids = {}
    for i, c in enumerate(careers):
        cid = f"career_{i}"
        career_ids[c] = cid
        karyotype_lines.append(f"chr - {cid} {c.replace(' ', '_').replace(',', '').replace('&', 'and')} 0 {career_totals[c]} cc_{i}\n")
        
    with open(CUSTOM_DIR / "karyotype.txt", "w") as f:
        f.writelines(karyotype_lines)

    # 2. COLORS
    major_rgb = MAJOR_COLORS.get(TARGET_MAJOR_CLUSTER, "128,130,133")
    color_lines = [
        "<colors>\n",
        f"cm_0 = {major_rgb}\n",
        f"cm_0_a5 = {major_rgb},0.5\n"
    ]
    for i in range(len(careers)):
        color_lines.append(f"cc_{i} = {CAREER_COLOR_RGB}\n")
    color_lines.append("</colors>\n")
    
    with open(CUSTOM_DIR / "colors.conf", "w") as f:
        f.writelines(color_lines)
        
    # 3. LINKS
    links_lines = []
    major_cursor = {TARGET_MAJOR_CLUSTER: 0}
    career_cursor = {c: 0 for c in careers}
    
    # Group by both to get counts
    edges = df_filtered.groupby(['Major Cluster', 'Industry Group']).size().reset_index(name='Count')
    
    for _, row in edges.iterrows():
        m = row["Major Cluster"]
        c = row["Industry Group"]
        count = row["Count"]
        
        m_start = major_cursor[m]
        m_end = m_start + count
        major_cursor[m] = m_end
        
        c_start = career_cursor[c]
        c_end = c_start + count
        career_cursor[c] = c_end
        
        mid = major_ids[m]
        cid = career_ids[c]
        links_lines.append(f"{mid} {m_start} {m_end} {cid} {c_start} {c_end} color=128,130,133,0.5\n")
            
    with open(CUSTOM_DIR / "links.txt", "w") as f:
        f.writelines(links_lines)
    
    # 4. CIRCOS CONF (Using Absolute Paths)
    last_major = "major_0"
    first_career = "career_0"
    last_career = f"career_{len(careers)-1}"
    first_major = "major_0"

    conf_content = f"""
karyotype = {(CUSTOM_DIR / 'karyotype.txt').as_posix()}
chromosomes_units = 1
chromosomes_display_default = yes

<image>
dir = {CUSTOM_DIR.as_posix()}
file = v4_eng_circos.png
png = yes
svg = no
radius = 1500p
background = white
angle_offset = -90
auto_alpha_colors = yes
auto_alpha_steps = 5
</image>

<ideogram>
  <spacing>
    default = 0.005r
    <pairwise {last_major} {first_career}>
      spacing = 15r
    </pairwise>
    <pairwise {last_career} {first_major}>
      spacing = 15r
    </pairwise>
  </spacing>
  radius = 0.85r
  thickness = 40p
  fill = yes
  stroke_color = white
  stroke_thickness = 4p
  
  show_label = yes
  label_font = default
  label_radius = 1.05r
  label_size = 40
  label_parallel = yes
</ideogram>

show_ticks = no
show_tick_labels = no

<links>
<link>
file = {(CUSTOM_DIR / 'links.txt').as_posix()}
radius = 0.84r
bezier_radius = 0.5r
thickness = 2
ribbon = yes
</link>
</links>

<<include {(CUSTOM_DIR / 'colors.conf').as_posix()}>>
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/colors_fonts_patterns.conf>>
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/housekeeping.conf>>
"""
    with open(CUSTOM_DIR / "circos.conf", "w") as f:
        f.write(conf_content)
        
    print(f"Successfully built custom_circos_v4_eng files")

if __name__ == "__main__":
    build_files()
    print("Running Circos...")
    try:
        cmd = ["perl", r"C:\Users\hoang\Downloads\circos-0.69-10\circos-0.69-10\bin\circos", "-conf", (CUSTOM_DIR / "circos.conf").as_posix()]
        subprocess.run(cmd, check=True)
        print("Circos image generated success at custom_circos_v4_eng/v4_eng_circos.png")
    except Exception as e:
        print(f"Error running circos: {e}")
