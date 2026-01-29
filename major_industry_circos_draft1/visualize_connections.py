import base64
from pathlib import Path
import pandas as pd

# Constants
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
ETC_DIR = PROJECT_DIR / "etc"
INFILE = DATA_DIR / "college.txt"
KARYO_FILE = DATA_DIR / "karyotype.txt"
LINKS_FILE = DATA_DIR / "links.txt"
IMAGE_FILE = PROJECT_DIR / "major_industry_circos.png"
HTML_FILE = PROJECT_DIR / "major_industry_map_view.html"

# Mappings (consider moving these to a separate config if they grow)
MAJOR_MAP = {1: "Major_1", 2: "Major_2", 3: "Major_3", 4: "Major_4"}
INDUSTRY_MAP = {
    1: "Industry_1", 2: "Industry_2", 3: "Industry_3",
    4: "Industry_4", 5: "Industry_5", 6: "Industry_6"
}
SCALE = 10


def load_and_process_data(filepath: Path) -> pd.DataFrame:
    """Loads CSV data and maps major/industry codes to labels."""
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")

    df = pd.read_csv(filepath)
    df.columns = [c.strip().lower() for c in df.columns]
    
    # Filter and drop missing values
    df = df[["major", "industry"]].dropna()

    # Apply mappings
    df["major"] = df["major"].astype(int).map(MAJOR_MAP).fillna(
        df["major"].astype(str).radd("Major ")
    )
    df["industry"] = df["industry"].astype(int).map(INDUSTRY_MAP).fillna(
        df["industry"].astype(str).radd("Industry ")
    )
    return df


def generate_circos_files(df: pd.DataFrame, karyo_path: Path, links_path: Path):
    """Generates the karyotype and links files required by Circos."""
    
    # Calculate edge weights (flow width)
    edges = df.groupby(["major", "industry"]).size().reset_index(name="count")

    majors = sorted(edges["major"].unique())
    industries = sorted(edges["industry"].unique())

    # Calculate segment lengths
    major_totals = edges.groupby("major")["count"].sum().to_dict()
    industry_totals = edges.groupby("industry")["count"].sum().to_dict()

    # Assign IDs
    major_ids = {m: f"M{i+1}" for i, m in enumerate(majors)}
    industry_ids = {ind: f"I{i+1}" for i, ind in enumerate(industries)}

    # 1. Write Karyotype File
    with open(karyo_path, "w", encoding="utf-8") as f:
        # Majors (chr1-chr4...)
        for i, m in enumerate(majors):
            cid = major_ids[m]
            length = int(major_totals[m] * SCALE)
            f.write(f"chr - {cid} {m} 0 {length} chr{i+1}\n")

        # Industries (chr5...)
        offset = len(majors)
        for i, ind in enumerate(industries):
            cid = industry_ids[ind]
            length = int(industry_totals[ind] * SCALE)
            f.write(f"chr - {cid} {ind} 0 {length} chr{i+1+offset}\n")

    # 2. Write Links File
    # Track current position for each segment to stack ribbons
    major_cursor = {mid: 0 for mid in major_ids.values()}
    industry_cursor = {iid: 0 for iid in industry_ids.values()}

    # Sort to ensure deterministic ribbon ordering
    edges_sorted = edges.sort_values(["major", "industry"]).reset_index(drop=True)

    with open(links_path, "w", encoding="utf-8") as f:
        for _, row in edges_sorted.iterrows():
            m_label = row["major"]
            i_label = row["industry"]
            width = int(row["count"] * SCALE)

            m_id = major_ids[m_label]
            i_id = industry_ids[i_label]

            # Calculate start/end positions
            m_start = major_cursor[m_id]
            m_end = m_start + width
            major_cursor[m_id] = m_end

            i_start = industry_cursor[i_id]
            i_end = i_start + width
            industry_cursor[i_id] = i_end

            # Color ribbon by major (using alpha for transparency)
            # Assuming standard Circos colors (chr1, chr2...) match the major index
            # This logic mimics the original simplified coloring
            ribbon_color = f"chr{major_ids[m_label][1:]}_a6" 

            f.write(f"{m_id} {m_start} {m_end} {i_id} {i_start} {i_end} color={ribbon_color}\n")

    print(f"Generated Circos files:\n  - {karyo_path}\n  - {links_path}")


def generate_shareable_html(image_path: Path, output_path: Path):
    """Creates a self-contained HTML file with the image embedded as Base64."""
    if not image_path.exists():
        print(f"Warning: Image file not found at {image_path}. Skipping HTML generation.")
        return

    # Encode image to Base64
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode("utf-8")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Major-Industry Connections</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            background-color: #f9f9f9;
            margin: 0;
            padding: 40px;
            color: #333;
        }}
        h1 {{
            margin-bottom: 10px;
            color: #2c3e50;
        }}
        p.subtitle {{
            color: #7f8c8d;
            margin-bottom: 30px;
        }}
        .visualization-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            display: inline-block;
            max-width: 100%;
        }}
        img {{
            max-width: 100%;
            height: auto;
            display: block;
        }}
        .footer {{
            margin-top: 40px;
            font-size: 0.9em;
            color: #95a5a6;
        }}
    </style>
</head>
<body>

    <h1>Major to Industry Connections</h1>
    <p class="subtitle">Visualizing the flow of graduates from majors to industries</p>

    <div class="visualization-container">
        <!-- Embedded Base64 Image -->
        <img src="data:image/png;base64,{b64_string}" alt="Chord Diagram of Major-Industry Connections">
    </div>

    <div class="footer">
        <p>Generated by automated analysis tools.</p>
    </div>

</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated shareable HTML:\n  - {output_path}")


def main():
    print("Starting data processing...")
    
    # Ensure directories exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ETC_DIR.mkdir(parents=True, exist_ok=True)

    try:
        # Load Data
        df = load_and_process_data(INFILE)
        
        # Generate Data files for Circos
        generate_circos_files(df, KARYO_FILE, LINKS_FILE)

        # Generate Viewable HTML
        generate_shareable_html(IMAGE_FILE, HTML_FILE)
        
        print("Done.")
        
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
