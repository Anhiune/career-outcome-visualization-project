import os
import pandas as pd
from pathlib import Path
import subprocess

# Directories
BASE_DIR = Path(r"c:\Users\hoang\Documents\project_test\major_industry_circos_draft1")
CSV_PATH = Path(r"c:\Users\hoang\Documents\project_test\csv_exports\Major_to_Industry_Match_v3.csv")
CUSTOM_DIR = BASE_DIR / "custom_circos_v3"
CUSTOM_DIR.mkdir(parents=True, exist_ok=True)

# Aesthetic Colors
MAJOR_COLOR = "74,123,183"  # Blue for the Major
CAREER_COLOR_RGB = "147,149,152"  # Medium grey for all right-side targets

# Target
TARGET_MAJOR = "Finance & Accounting"

def build_files():
    df = pd.read_csv(CSV_PATH)
    
    # We only want flows FOR this exact major to make "1 image from circos for 1 major"
    df_filtered = df[df['Major (Small Cluster)'] == TARGET_MAJOR].copy()
    
    # Karyotype needs TARGET_MAJOR + all connected industries
    majors = [TARGET_MAJOR]
    careers = sorted(df_filtered['Industry (Job Function)'].unique())
    
    major_totals = df_filtered.groupby("Major (Small Cluster)")["Count"].sum()
    career_totals = df_filtered.groupby("Industry (Job Function)")["Count"].sum()
    
    # KARYOTYPE
    karyotype_lines = []
    major_ids = {}
    career_ids = {}
    
    # Process Majors
    for i, m in enumerate(majors):
        mid = f"major_{i}"
        major_ids[m] = mid
        length = major_totals[m]
        color = f"cm_{i}"
        karyotype_lines.append(f"chr - {mid} {m.replace(' ', '_').replace('&', 'and')} 0 {length} {color}\n")
        
    # Process Careers
    for i, c in enumerate(careers):
        cid = f"career_{i}"
        career_ids[c] = cid
        length = career_totals[c]
        color = f"cc_{i}"
        karyotype_lines.append(f"chr - {cid} {c.replace(' ', '_').replace('&', 'and')} 0 {length} {color}\n")
        
    with open(CUSTOM_DIR / "karyotype.txt", "w") as f:
        f.writelines(karyotype_lines)

    # COLORS
    color_lines = ["<colors>\n"]
    for i, m in enumerate(majors):
        color_lines.append(f"cm_{i} = {MAJOR_COLOR}\n")
        color_lines.append(f"cm_{i}_a5 = {MAJOR_COLOR},0.5\n")
    for i, c in enumerate(careers):
        color_lines.append(f"cc_{i} = {CAREER_COLOR_RGB}\n")
    color_lines.append("</colors>\n")
    
    with open(CUSTOM_DIR / "colors.conf", "w") as f:
        f.writelines(color_lines)
        
    # LINKS
    links_lines = []
    major_cursor = {m: 0 for m in majors}
    career_cursor = {c: 0 for c in careers}
    
    for _, row in df_filtered.iterrows():
        m = row["Major (Small Cluster)"]
        c = row["Industry (Job Function)"]
        count = row["Count"]
        
        m_start = major_cursor[m]
        m_end = m_start + count
        major_cursor[m] = m_end
        
        c_start = career_cursor[c]
        c_end = c_start + count
        career_cursor[c] = c_end
        
        mid = major_ids[m]
        cid = career_ids[c]
        m_idx = majors.index(m)
        ribbon_color = "74,123,183,0.5" # Blue
        
        links_lines.append(f"{mid} {m_start} {m_end} {cid} {c_start} {c_end} color={ribbon_color}\n")
            
    with open(CUSTOM_DIR / "links.txt", "w") as f:
        f.writelines(links_lines)
    
    # CIRCOS CONF
    last_major = major_ids[majors[-1]]
    first_career = career_ids[careers[0]]
    last_career = career_ids[careers[-1]]
    first_major = major_ids[majors[0]]

    conf_content = f"""
karyotype = { (CUSTOM_DIR / 'karyotype.txt').as_posix() }
chromosomes_units = 1
chromosomes_display_default = yes

<image>
dir = { CUSTOM_DIR.as_posix() }
file = v3_major_industry_circos.png
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
  label_size = 32
  label_parallel = yes
</ideogram>

show_ticks = no
show_tick_labels = no

<links>
<link>
file = { (CUSTOM_DIR / 'links.txt').as_posix() }
radius = 0.84r
bezier_radius = 0.5r
thickness = 2
ribbon = yes
</link>
</links>

<<include { (CUSTOM_DIR / 'colors.conf').as_posix() }>>
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/colors_fonts_patterns.conf>>
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/housekeeping.conf>>
"""
    with open(CUSTOM_DIR / "circos.conf", "w") as f:
        f.write(conf_content)
        
    print(f"Successfully built custom_circos_v3 files for {TARGET_MAJOR}")

if __name__ == "__main__":
    build_files()
    print("Running Circos...")
    try:
        cmd = ["perl", r"C:\Users\hoang\Downloads\circos-0.69-10\circos-0.69-10\bin\circos", "-conf", r"c:\Users\hoang\Documents\project_test\major_industry_circos_draft1\custom_circos_v3\circos.conf"]
        subprocess.run(cmd, check=True)
        print("Circos image generated successfully at custom_circos_v3/v3_major_industry_circos.png")
    except Exception as e:
        print(f"Error running circos: {e}")
