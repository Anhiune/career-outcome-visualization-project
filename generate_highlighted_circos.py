import os
import pandas as pd
from pathlib import Path
import subprocess

# --- SETUP ---
BASE_DIR = Path(r"c:\Users\hoang\Documents\project_test\major_industry_circos_draft1")
RAW_DATA_PATH = Path(r"c:\Users\hoang\Documents\project_test\data\career_outcomes_final.csv")
CIRCOS_BIN = r"C:\Users\hoang\Downloads\circos-0.69-10\circos-0.69-10\bin\circos"
OUTPUT_DIR = BASE_DIR / "highlighted_check"
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

# --- TARGET ---
TARGET_MAJOR = "BUSINESS & MANAGEMENT"

def generate_circos():
    print(f"Reading data and highlighting {TARGET_MAJOR}...")
    df = pd.read_csv(RAW_DATA_PATH)
    
    # Ensure all are strings and match case
    df['Major Cluster'] = df['Major Cluster'].astype(str)
    df['Industry Group'] = df['Industry Group'].astype(str)
    
    majors_order = list(MAJOR_COLORS_RGB.keys())
    # Exclude rows where Major Cluster is not in our set of 8
    df = df[df['Major Cluster'].isin(majors_order)]
    
    # 1. Compute totals for ALL majors and ALL industries to keep scale correct
    major_totals = df.groupby("Major Cluster").size()
    industry_totals = df.groupby("Industry Group").size()
    
    industries = sorted(df['Industry Group'].unique())
    
    # 2. CREATE KARYOTYPE (ALL categories with count > 0)
    karyotype_lines = []
    major_ids = {}
    for i, m in enumerate(majors_order):
        count = major_totals.get(m, 0)
        if count == 0: continue
        mid = f"major_{i}"
        major_ids[m] = mid
        label = m.replace(' ', '_').replace('&', 'and')
        karyotype_lines.append(f"chr - {mid} {label} 0 {count} major_{i}\n")
        
    industry_ids = {}
    for i, ind in enumerate(industries):
        count = industry_totals.get(ind, 0)
        if count == 0: continue
        iid = f"industry_{i}"
        industry_ids[ind] = iid
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
        
    # 4. CREATE LINKS (ONLY for TARGET_MAJOR)
    links_lines = []
    
    # We need to compute the offsets correctly. 
    # To do this, we need to know the offset for the TARGET_MAJOR within ITSELF (starts at 0)
    # AND the offset for each INDUSTRY based on ALL majors that contribute to it.
    
    # Group ALL edges to compute accurate industry offsets
    all_edges = df.groupby(['Major Cluster', 'Industry Group']).size().reset_index(name='Count')
    
    # Sort all_edges to match the order of ideograms for consistent stacking
    # We'll use the majors_order for the industry stacking sequence
    all_edges['m_rank'] = all_edges['Major Cluster'].apply(lambda x: majors_order.index(x))
    all_edges = all_edges.sort_values(['Industry Group', 'm_rank'])
    
    industry_cursor = {ind: 0 for ind in industries}
    target_major_cursor = 0
    
    for _, row in all_edges.iterrows():
        m = row['Major Cluster']
        ind = row['Industry Group']
        count = row['Count']
        
        # Calculate current start/end for this flow segment in the industry
        i_start = industry_cursor[ind]
        i_end = i_start + count
        industry_cursor[ind] = i_end
        
        # ONLY if this is the target major, we create a link line
        if m == TARGET_MAJOR:
            m_start = target_major_cursor
            m_end = m_start + count
            target_major_cursor = m_end
            
            mid = major_ids[m]
            iid = industry_ids[ind]
            m_idx = majors_order.index(m)
            ribbon_color = f"major_{m_idx}_a5"
            
            links_lines.append(f"{mid} {m_start} {m_end} {iid} {i_start} {i_end} color={ribbon_color}\n")
        # If it's NOT the target major, we still incremented the industry cursor, 
        # so the target major's ribbons will land on the correct "slice" of the industry arc.

    with open(OUTPUT_DIR / "links.txt", "w") as f:
        f.writelines(links_lines)
        
    # 5. CREATE CIRCOS.CONF
    all_major_ids = list(major_ids.values())
    all_industry_ids = list(industry_ids.values())
    
    last_major = all_major_ids[-1]
    first_industry = all_industry_ids[0]
    last_industry = all_industry_ids[-1]
    first_major = all_major_ids[0]

    conf_content = f"""
karyotype = {(OUTPUT_DIR / 'karyotype.txt').as_posix()}
chromosomes_units = 1
chromosomes_display_default = yes

<image>
dir = {OUTPUT_DIR.as_posix()}
file = highlighted_circos.png
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
  label_font = default
  label_radius = 1.10r
  label_size = 40
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
"""
    with open(OUTPUT_DIR / "circos.conf", "w") as f:
        f.write(conf_content)
        
    # 6. RUN CIRCOS
    try:
        cmd = ["perl", CIRCOS_BIN, "-conf", (OUTPUT_DIR / "circos.conf").as_posix()]
        subprocess.run(cmd, check=True)
        print(f"Highlighted PNG generated success for {TARGET_MAJOR}")
    except Exception as e:
        print(f"Error executing Circos: {e}")

if __name__ == "__main__":
    generate_circos()
