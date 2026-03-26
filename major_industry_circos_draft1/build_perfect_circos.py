import os
import pandas as pd
from pathlib import Path

# Directories
BASE_DIR = Path(r"c:\Users\hoang\Documents\project_test\major_industry_circos_draft1")
CSV_DIR = Path(r"c:\Users\hoang\Documents\project_test\csv_exports")
CUSTOM_DIR = BASE_DIR / "custom_circos"
CUSTOM_DIR.mkdir(parents=True, exist_ok=True)

# Color maps mapped exactly to user screenshot request
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

CAREER_COLOR_RGB = "147,149,152"  # Medium grey for all right-side targets

# We specifically highlight just ONE major's flows based on their request.
TARGET_MAJOR = "BUSINESS & MANAGEMENT"

def load_all_data():
    files = {
        "BUSINESS & MANAGEMENT": "Major_Career_Analysis_v4__BUSINESS & MANAGEMENT.csv",
        "ENGINEERING & TECHNOLOGY": "Major_Career_Analysis_v4__ENGINEERING & TECHNOLOGY.csv",
        "NATURAL & HEALTH SCIENCES": "Major_Career_Analysis_v4__NATURAL & HEALTH SCIENCES.csv",
        "SOCIAL SCIENCES & HUMANITIES": "Major_Career_Analysis_v4__SOCIAL SCIENCES & HUMANITIES.csv",
        "COMMUNICATION & MEDIA": "Major_Career_Analysis_v4__COMMUNICATION & MEDIA.csv",
        "ARTS, LANGUAGES & THEOLOGY": "Major_Career_Analysis_v4__ARTS, LANGUAGES & THEOLOGY.csv",
        "EDUCATION & SOCIAL SERVICES": "Major_Career_Analysis_v4__EDUCATION & SOCIAL SERVICES.csv",
        "Unclassified": "Major_Career_Analysis_v4__Unclassified.csv",
    }
    
    all_data = []
    
    for major, filename in files.items():
        filepath = CSV_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            df = df[df['Major Cluster'].notna()].copy()
            df = df[['Major Cluster', 'Career Cluster', 'Count']]
            df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
            df = df.dropna()
            # If for some reason the Major Cluster name in the file doesn't perfectly match,
            # we enforce it
            df['Major Cluster'] = major
            all_data.append(df)
            
    return pd.concat(all_data, ignore_index=True)

def build_files():
    df = load_all_data()
    
    # Calculate exact scaling to integers
    SCALE = 1
    edges = df.groupby(["Major Cluster", "Career Cluster"])["Count"].sum().reset_index()
    edges["Count"] = (edges["Count"] * SCALE).astype(int)
    
    # Ordered domains
    majors = list(MAJOR_COLORS_RGB.keys())
    # Ensure all majors are actually in the data
    majors = [m for m in majors if m in edges["Major Cluster"].values]
    
    careers = sorted(edges["Career Cluster"].unique())
    
    major_totals = edges.groupby("Major Cluster")["Count"].sum()
    career_totals = edges.groupby("Career Cluster")["Count"].sum()
    
    # KARYOTYPE
    karyotype_lines = []
    major_ids = {}
    career_ids = {}
    
    for i, m in enumerate(majors):
        mid = f"major_{i}"
        major_ids[m] = mid
        length = major_totals[m]
        color = f"cm_{i}"
        karyotype_lines.append(f"chr - {mid} {m.replace(' ', '_')} 0 {length} {color}\n")
        
    for i, c in enumerate(careers):
        cid = f"career_{i}"
        career_ids[c] = cid
        length = career_totals[c]
        color = f"cc_{i}"
        karyotype_lines.append(f"chr - {cid} {c.replace(' ', '_')} 0 {length} {color}\n")
        
    with open(CUSTOM_DIR / "karyotype.txt", "w") as f:
        f.writelines(karyotype_lines)

    # COLORS
    color_lines = ["<colors>\n"]
    for i, m in enumerate(majors):
        color_lines.append(f"cm_{i} = {MAJOR_COLORS_RGB[m]}\n")
        color_lines.append(f"cm_{i}_a5 = {MAJOR_COLORS_RGB[m]},0.5\n")
        color_lines.append(f"cm_{i}_a8 = {MAJOR_COLORS_RGB[m]},0.8\n")
    for i, c in enumerate(careers):
        color_lines.append(f"cc_{i} = {CAREER_COLOR_RGB}\n")
    color_lines.append("</colors>\n")
    
    with open(CUSTOM_DIR / "colors.conf", "w") as f:
        f.writelines(color_lines)
        
    # LINKS
    links_lines = []
    # Cursor to track stacking the ribbons on the ideograms
    major_cursor = {m: 0 for m in majors}
    career_cursor = {c: 0 for c in careers}
    
    edges_sorted = edges.sort_values(["Major Cluster", "Career Cluster"])
    
    for _, row in edges_sorted.iterrows():
        m = row["Major Cluster"]
        c = row["Career Cluster"]
        count = row["Count"]
        
        m_start = major_cursor[m]
        m_end = m_start + count
        major_cursor[m] = m_end
        
        c_start = career_cursor[c]
        c_end = c_start + count
        career_cursor[c] = c_end
        
        # Only output the link if it belongs to the target major
        if m == TARGET_MAJOR:
            mid = major_ids[m]
            cid = career_ids[c]
            m_idx = majors.index(m)
            ribbon_color = f"cm_{m_idx}_a5"
            links_lines.append(f"seg {mid} {m_start} {m_end} {cid} {c_start} {c_end} color={ribbon_color}\n")
            
    with open(CUSTOM_DIR / "links.txt", "w") as f:
        f.writelines(links_lines)
    
    # CIRCOS CONF
    last_major = major_ids[majors[-1]]
    first_career = career_ids[careers[0]]
    last_career = career_ids[careers[-1]]
    first_major = major_ids[majors[0]]

    # Ensure label values are correct
    conf_content = f"""
karyotype = custom_circos/karyotype.txt
chromosomes_units = 1
chromosomes_display_default = yes

<image>
dir = custom_circos
file = major_industry_circos.png
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
file = custom_circos/links.txt
radius = 0.99r
bezier_radius = 0r
thickness = 2
ribbon = yes
</link>
</links>

<<include custom_circos/colors.conf>>
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/colors_fonts_patterns.conf>>
<<include C:/Users/hoang/Downloads/circos-0.69-10/circos-0.69-10/etc/housekeeping.conf>>
"""
    with open(CUSTOM_DIR / "circos.conf", "w") as f:
        f.write(conf_content)
        
    print("Successfully built custom_circos files for " + TARGET_MAJOR)

if __name__ == "__main__":
    build_files()
