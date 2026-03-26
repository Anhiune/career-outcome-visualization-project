import os
import pandas as pd
from pathlib import Path
import subprocess

# Directories
BASE_DIR = Path(r"c:\Users\hoang\Documents\project_test\major_industry_circos_draft1")
RAW_DATA_PATH = Path(r"c:\Users\hoang\Documents\project_test\data\career_outcomes_final.csv")
CUSTOM_DIR = BASE_DIR / "custom_circos_v4_softit"
CUSTOM_DIR.mkdir(parents=True, exist_ok=True)

# Aesthetic Colors
INDUSTRY_COLOR = "74,123,183"  # Blue for the target Industry
JOB_COLOR_RGB = "147,149,152"  # Grey for job titles

# Target Industry Functional Group
TARGET_INDUSTRY = "Software & IT"

def build_files():
    print("Loading raw data...")
    df = pd.read_csv(RAW_DATA_PATH)
    
    # Filter for the target industry group
    df_filtered = df[df['Job Function'] == TARGET_INDUSTRY].copy()
    
    # We want to see which JOB TITLES make up this industry
    # Aggregating top 15 job titles to keep the diagram readable
    job_counts = df_filtered.groupby('Job Title').size().sort_values(ascending=False).head(15).reset_index(name='Count')
    top_jobs = job_counts['Job Title'].tolist()
    df_top = df_filtered[df_filtered['Job Title'].isin(top_jobs)].copy()
    
    industries = [TARGET_INDUSTRY]
    jobs = top_jobs
    
    industry_total = job_counts['Count'].sum()
    
    # 1. KARYOTYPE
    karyotype_lines = []
    # Industry on left
    karyotype_lines.append(f"chr - ind_0 {TARGET_INDUSTRY.replace(' ', '_').replace('&', 'and')} 0 {industry_total} cm_0\n")
    
    # Job Titles on right
    for i, j in enumerate(jobs):
        count = job_counts[job_counts['Job Title'] == j]['Count'].values[0]
        jid = f"job_{i}"
        label = j.replace(' ', '_').replace('&', 'and').replace('/', '_')
        karyotype_lines.append(f"chr - {jid} {label} 0 {count} cc_{i}\n")
        
    with open(CUSTOM_DIR / "karyotype.txt", "w") as f:
        f.writelines(karyotype_lines)

    # 2. COLORS
    color_lines = [
        "<colors>\n",
        f"cm_0 = {INDUSTRY_COLOR}\n",
        f"cm_0_a5 = {INDUSTRY_COLOR},0.5\n"
    ]
    for i in range(len(jobs)):
        color_lines.append(f"cc_{i} = {JOB_COLOR_RGB}\n")
    color_lines.append("</colors>\n")
    
    with open(CUSTOM_DIR / "colors.conf", "w") as f:
        f.writelines(color_lines)
        
    # 3. LINKS
    links_lines = []
    ind_cursor = 0
    
    for i, j in enumerate(jobs):
        count = job_counts[job_counts['Job Title'] == j]['Count'].values[0]
        
        # Link from Industry slice to Job slice
        links_lines.append(f"ind_0 {ind_cursor} {ind_cursor + count} job_{i} 0 {count} color=216,133,59,0.5\n")
        ind_cursor += count
            
    with open(CUSTOM_DIR / "links.txt", "w") as f:
        f.writelines(links_lines)
    
    # 4. CIRCOS CONF
    last_ind = "ind_0"
    first_job = "job_0"
    last_job = f"job_{len(jobs)-1}"
    first_ind = "ind_0"

    conf_content = f"""
karyotype = {(CUSTOM_DIR / 'karyotype.txt').as_posix()}
chromosomes_units = 1
chromosomes_display_default = yes

<image>
dir = {CUSTOM_DIR.as_posix()}
file = v4_job_industry_circos.png
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
    <pairwise {last_ind} {first_job}>
      spacing = 15r
    </pairwise>
    <pairwise {last_job} {first_ind}>
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
  label_size = 35
  label_parallel = yes
</ideogram>

show_ticks = no
show_tick_labels = no

<links>
<link>
file = {(CUSTOM_DIR / 'links.txt').as_posix()}
radius = 0.84r
bezier_radius = 0.5r
thickness = 1
ribbon = yes
flat = yes
</link>
</links>

<<include {(CUSTOM_DIR / 'colors.conf').as_posix()}>>
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/colors_fonts_patterns.conf>>
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/housekeeping.conf>>
"""
    with open(CUSTOM_DIR / "circos.conf", "w") as f:
        f.write(conf_content)
        
    print(f"Successfully built custom_circos_v4_softit files")

if __name__ == "__main__":
    build_files()
    print("Running Circos...")
    try:
        cmd = ["perl", r"C:\Users\hoang\Downloads\circos-0.69-10\circos-0.69-10\bin\circos", "-conf", (CUSTOM_DIR / "circos.conf").as_posix()]
        subprocess.run(cmd, check=True)
        print("Circos image generated success at v4_job_industry_circos.png")
    except Exception as e:
        print(f"Error running circos: {e}")
