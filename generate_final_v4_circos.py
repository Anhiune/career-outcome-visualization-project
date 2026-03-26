import os
import pandas as pd
from pathlib import Path
import subprocess

# --- SETUP ---
BASE_DIR = Path(r"c:\Users\hoang\Documents\project_test\major_industry_circos_draft1")
RAW_DATA_PATH = Path(r"c:\Users\hoang\Documents\project_test\data\career_outcomes_final.csv")
CIRCOS_BIN = r"C:\Users\hoang\Downloads\circos-0.69-10\circos-0.69-10\bin\circos"
OUTPUT_DIR = BASE_DIR / "final_check_circos"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Define exact color mapping for the 8 Major Clusters
MAJOR_COLORS_RGB = {
    "COMMUNICATION & MEDIA": "74,123,183",      # Blue
    "ARTS, LANGUAGES & THEOLOGY": "230,208,172", # Tan
    "SOCIAL SCIENCES & HUMANITIES": "216,133,59", # Orange
    "BUSINESS & MANAGEMENT": "171,73,24",       # Brown
    "EDUCATION & SOCIAL SERVICES": "187,217,177", # Light Green
    "NATURAL & HEALTH SCIENCES": "107,176,92",   # Green
    "ENGINEERING & TECHNOLOGY": "128,130,133",   # Dark Grey
    "Unclassified": "167,169,172",              # Light Grey
}

CAREER_COLOR_RGB = "147,149,152"  # Uniform grey for industries

def generate_circos():
    print("Reading data...")
    df = pd.read_csv(RAW_DATA_PATH)
    
    # 1. Group data into Major -> Industry Group flows
    # We use 'Major Cluster' and 'Industry Group'
    edges = df.groupby(['Major Cluster', 'Industry Group']).size().reset_index(name='Count')
    
    # Sort majors by our defined sequence for the gradient effect
    majors_order = list(MAJOR_COLORS_RGB.keys())
    # Ensure all are strings and match case
    edges['Major Cluster'] = edges['Major Cluster'].astype(str)
    edges['Industry Group'] = edges['Industry Group'].astype(str)
    
    # Filter for entries that exist in our color map
    edges = edges[edges['Major Cluster'].isin(majors_order)]
    
    industries = sorted(edges['Industry Group'].unique())
    
    major_totals = edges.groupby("Major Cluster")["Count"].sum()
    industry_totals = edges.groupby("Industry Group")["Count"].sum()
    
    # 2. CREATE KARYOTYPE
    karyotype_lines = []
    major_ids = {}
    for i, m in enumerate(majors_order):
        mid = f"major_{i}"
        major_ids[m] = mid
        count = major_totals.get(m, 0)
        label = m.replace(' ', '_').replace('&', 'and')
        karyotype_lines.append(f"chr - {mid} {label} 0 {count} major_{i}\n")
        
    industry_ids = {}
    for i, ind in enumerate(industries):
        iid = f"industry_{i}"
        industry_ids[ind] = iid
        count = industry_totals.get(ind, 0)
        label = ind.replace(' ', '_').replace('&', 'and').replace(',', '')
        karyotype_lines.append(f"chr - {iid} {label} 0 {count} ind_{i}\n")
        
    with open(OUTPUT_DIR / "karyotype.txt", "w") as f:
        f.writelines(karyotype_lines)

    # 3. CREATE COLORS
    color_lines = ["<colors>\n"]
    for i, m in enumerate(majors_order):
        color_lines.append(f"major_{i} = {MAJOR_COLORS_RGB[m]}\n")
        color_lines.append(f"major_{i}_a5 = {MAJOR_COLORS_RGB[m]},0.5\n")
    for i, ind in enumerate(industries):
        color_lines.append(f"ind_{i} = {CAREER_COLOR_RGB}\n")
    color_lines.append("</colors>\n")
    
    with open(OUTPUT_DIR / "colors.conf", "w") as f:
        f.writelines(color_lines)
        
    # 4. CREATE LINKS (The ribbons)
    links_lines = []
    major_cursor = {m: 0 for m in majors_order}
    industry_cursor = {ind: 0 for ind in industries}
    
    # We iterate edges to create connections
    for _, row in edges.iterrows():
        m = row['Major Cluster']
        ind = row['Industry Group']
        count = row['Count']
        
        m_start = major_cursor[m]
        m_end = m_start + count
        major_cursor[m] = m_end
        
        i_start = industry_cursor[ind]
        i_end = i_start + count
        industry_cursor[ind] = i_end
        
        mid = major_ids[m]
        iid = industry_ids[ind]
        m_idx = majors_order.index(m)
        ribbon_color = f"major_{m_idx}_a5"
        
        links_lines.append(f"{mid} {m_start} {m_end} {iid} {i_start} {i_end} color={ribbon_color}\n")
            
    with open(OUTPUT_DIR / "links.txt", "w") as f:
        f.writelines(links_lines)
        
    # 5. CREATE CIRCOS.CONF
    # Hemisphere gap logic
    last_major = major_ids[majors_order[-1]]
    first_industry = industry_ids[industries[0]]
    last_industry = industry_ids[industries[-1]]
    first_major = major_ids[majors_order[0]]

    conf_content = f"""
karyotype = {(OUTPUT_DIR / 'karyotype.txt').as_posix()}
chromosomes_units = 1
chromosomes_display_default = yes

<image>
dir = {OUTPUT_DIR.as_posix()}
file = final_static_circos.png
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
    # Large 15 degree gaps between hemispheres
    <pairwise {last_major} {first_industry}>
      spacing = 15r
    </pairwise>
    <pairwise {last_industry} {first_major}>
      spacing = 15r
    </pairwise>
  </spacing>
  radius = 0.85r
  thickness = 40p
  fill = yes
  stroke_color = white
  stroke_thickness = 4p
  
  show_label = yes
  label_font = oswald_regular
  label_radius = 1.10r
  label_size = 38
  label_parallel = yes
</ideogram>

show_ticks = no
show_tick_labels = no

<links>
<link>
file = {(OUTPUT_DIR / 'links.txt').as_posix()}
radius = 0.84r
bezier_radius = 0.5r
thickness = 1
ribbon = yes
flat = yes
</link>
</links>

<<include {(OUTPUT_DIR / 'colors.conf').as_posix()}>>
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/colors_fonts_patterns.conf>>
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/housekeeping.conf>>

# Font customization for premium look
<fonts>
oswald_regular = C:/Windows/Fonts/oswald_regular.ttf
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/fonts.conf>>
</fonts>
"""
    # Note: If oswald font is missing, it skips or falls back.
    # I'll use default font to avoid failure if the TTF isn't at that path.
    conf_content = conf_content.replace('oswald_regular', 'default')

    with open(OUTPUT_DIR / "circos.conf", "w") as f:
        f.write(conf_content)
        
    print("Configuration files generated.")

    # 6. RUN CIRCOS
    print("Running Perl Circos engine...")
    try:
        cmd = ["perl", CIRCOS_BIN, "-conf", (OUTPUT_DIR / "circos.conf").as_posix()]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Final PNG generated successfully at final_check_circos/final_static_circos.png")
    except Exception as e:
        print(f"Error executing Circos: {e}")
        if hasattr(e, 'stderr'): print(e.stderr)

if __name__ == "__main__":
    generate_circos()
