"""
Generate true Circos diagrams using Circos.js library
Official JavaScript port of the Circos visualization tool
"""

import pandas as pd
import json
import os
from pathlib import Path

MAJOR_COLORS = {
    "BUSINESS & MANAGEMENT": "#332288",
    "ENGINEERING & TECHNOLOGY": "#44AA99",
    "NATURAL & HEALTH SCIENCES": "#88CCEE",
    "SOCIAL SCIENCES & HUMANITIES": "#DDCC77",
    "COMMUNICATION & MEDIA": "#CC6677",
    "ARTS, LANGUAGES & THEOLOGY": "#882255",
    "EDUCATION & SOCIAL SERVICES": "#117733",
}

CAREER_COLORS = {
    "Business & Finance": "#4477AA",
    "Technology & Engineering": "#66CCBB",
    "Healthcare & Science": "#99DDFF",
    "Education & Service": "#228833",
    "Arts, Media & Legal": "#AA3377",
    "Unclassified": "#BBBBBB"
}

def load_cluster_data(csv_file):
    df = pd.read_csv(csv_file)
    df = df[df['Major Cluster'].notna()].copy()
    df = df[['Major Cluster', 'Career Cluster', 'Count', 'Percentage']]
    df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
    df = df.dropna(subset=['Count'])
    return df

def load_all_clusters():
    csv_dir = r"C:\Users\hoang\Documents\project_test\csv_exports"
    cluster_files = {
        "BUSINESS & MANAGEMENT": "Major_Career_Analysis_v4__BUSINESS & MANAGEMENT.csv",
        "ENGINEERING & TECHNOLOGY": "Major_Career_Analysis_v4__ENGINEERING & TECHNOLOGY.csv",
        "NATURAL & HEALTH SCIENCES": "Major_Career_Analysis_v4__NATURAL & HEALTH SCIENCES.csv",
        "SOCIAL SCIENCES & HUMANITIES": "Major_Career_Analysis_v4__SOCIAL SCIENCES & HUMANITIES.csv",
        "COMMUNICATION & MEDIA": "Major_Career_Analysis_v4__COMMUNICATION & MEDIA.csv",
        "ARTS, LANGUAGES & THEOLOGY": "Major_Career_Analysis_v4__ARTS, LANGUAGES & THEOLOGY.csv",
        "EDUCATION & SOCIAL SERVICES": "Major_Career_Analysis_v4__EDUCATION & SOCIAL SERVICES.csv",
    }

    clusters = {}
    for cluster_name, filename in cluster_files.items():
        filepath = os.path.join(csv_dir, filename)
        if os.path.exists(filepath):
            clusters[cluster_name] = load_cluster_data(filepath)
            print(f"[OK] Loaded {cluster_name}")
        else:
            print(f"[SKIP] Not found: {filepath}")

    return clusters

def generate_circos_js_html(major_cluster, df):
    """Generate Circos visualization using Circos.js library"""

    major_color = MAJOR_COLORS.get(major_cluster, "#999999")

    # Prepare data for Circos
    careers = sorted(df['Career Cluster'].unique().tolist())
    total_count = int(df['Count'].sum())

    # Create ideogram data (sectors on the circle)
    ideograms = [{"id": major_cluster, "label": major_cluster, "len": total_count, "color": major_color}]

    for career in careers:
        count = int(df[df['Career Cluster'] == career]['Count'].values[0])
        color = CAREER_COLORS.get(career, "#BBBBBB")
        ideograms.append({"id": career, "label": career, "len": count, "color": color})

    # Create links (connections between major and careers)
    links = []
    for career in careers:
        count = int(df[df['Career Cluster'] == career]['Count'].values[0])
        links.append({
            "source": {"id": major_cluster, "start": 0, "end": total_count},
            "target": {"id": career, "start": 0, "end": count},
            "value": count
        })

    ideograms_json = json.dumps(ideograms)
    links_json = json.dumps(links)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + major_cluster + """ - Circos Diagram</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/circos@2.3.0/dist/circos.min.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: "Manrope", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: linear-gradient(135deg, #f5f1e7 0%, #e9e2d1 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 24px;
            box-shadow: 0 30px 80px rgba(30, 31, 27, 0.18);
            padding: 40px;
            max-width: 1000px;
            width: 100%;
        }

        h1 {
            text-align: center;
            margin-bottom: 10px;
            color: #1e1f1b;
            font-size: 28px;
            font-weight: 700;
        }

        .subtitle {
            text-align: center;
            color: rgba(30, 31, 27, 0.7);
            margin-bottom: 30px;
            font-size: 14px;
        }

        #circos {
            display: flex;
            justify-content: center;
            background: radial-gradient(circle at center, rgba(255,255,255,0.95) 0%, transparent 70%);
            padding: 30px;
            border-radius: 16px;
            margin-bottom: 30px;
            min-height: 800px;
        }

        svg {
            max-width: 100%;
            height: auto;
        }

        .legend {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e0e0e0;
        }

        .legend-title {
            font-weight: 600;
            margin-bottom: 12px;
            color: #1e1f1b;
            font-size: 14px;
        }

        .legend-item {
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 8px;
            font-size: 13px;
        }

        .legend-color {
            display: inline-block;
            width: 14px;
            height: 14px;
            border-radius: 3px;
            margin-right: 6px;
            vertical-align: middle;
        }

        .stats {
            margin-top: 20px;
            padding: 16px;
            background: #f9f7f2;
            border-radius: 12px;
            font-size: 13px;
            color: #555;
            line-height: 1.6;
        }

        .tooltip {
            position: fixed;
            padding: 10px 14px;
            background: rgba(30, 31, 27, 0.92);
            color: white;
            border-radius: 6px;
            font-size: 12px;
            pointer-events: none;
            display: none;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>""" + major_cluster + """</h1>
        <div class="subtitle">Career Pathways - Circos.js Visualization</div>

        <div id="circos"></div>
        <div class="tooltip"></div>

        <div class="legend">
            <div class="legend-title">Career Destinations</div>
"""

    # Add legend
    for career in careers:
        color = CAREER_COLORS.get(career, "#BBBBBB")
        count = int(df[df['Career Cluster'] == career]['Count'].values[0])
        pct = (count / total_count) * 100
        html += f"""            <div class="legend-item">
                <span class="legend-color" style="background: {color};"></span>{career} ({pct:.1f}%)
            </div>
"""

    # Add statistics
    html += """        </div>

        <div class="stats">
            <strong>Distribution by Career Cluster:</strong><br>
"""

    career_stats = df.groupby('Career Cluster')['Count'].sum().sort_values(ascending=False)
    for career, count in career_stats.items():
        pct = (count / total_count) * 100
        html += f"            {career}: {int(count)} ({pct:.1f}%)<br>\n"

    html += """        </div>
    </div>

    <script>
    const ideograms = """ + ideograms_json + """;
    const links = """ + links_json + """;

    const container = document.querySelector('#circos');

    const circos = new Circos({
        container: container,
        width: 700,
        height: 700
    });

    // Render ideograms (sectors)
    circos
        .layout(ideograms, {
            innerRadius: 200,
            outerRadius: 250,
            cornerRadius: 10,
            gap: 0.04,
            labels: {
                display: true,
                size: 11,
                color: '#1e1f1b',
                radialOffset: 15
            },
            ticks: { display: false }
        })
        .render();

    // Draw chords/ribbons
    circos.chords(
        links.map(link => ({
            source: {id: link.source.id, start: 0, end: link.source.end},
            target: {id: link.target.id, start: 0, end: link.target.end},
            value: link.value
        })),
        {
            radius: 190,
            logScale: false,
            colorA: '#AAA',
            colorB: '#AAA',
            opacity: 0.5,
            strokeWidth: 0.5
        }
    );

    // Add interactivity
    container.addEventListener('mouseover', function(e) {
        if (e.target.tagName === 'text') {
            const label = e.target.textContent;
            const tooltip = document.querySelector('.tooltip');
            tooltip.textContent = label;
            tooltip.style.display = 'block';
        }
    });

    container.addEventListener('mousemove', function(e) {
        const tooltip = document.querySelector('.tooltip');
        if (tooltip.style.display === 'block') {
            tooltip.style.left = (e.pageX + 10) + 'px';
            tooltip.style.top = (e.pageY + 10) + 'px';
        }
    });

    container.addEventListener('mouseout', function() {
        document.querySelector('.tooltip').style.display = 'none';
    });
    </script>
</body>
</html>"""

    return html

def main():
    output_dir = r"C:\Users\hoang\Documents\project_test\circos_js_diagrams\html"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print("\n" + "="*60)
    print("CIRCOS.JS DIAGRAM GENERATOR")
    print("(Official JavaScript implementation of Circos)")
    print("="*60 + "\n")

    clusters = load_all_clusters()

    if not clusters:
        print("[ERROR] No cluster data found!")
        return

    print(f"\n[OK] Loaded {len(clusters)} major clusters\n")

    for idx, (cluster_name, df) in enumerate(clusters.items(), 1):
        print(f"{idx}. Generating {cluster_name}...")

        html = generate_circos_js_html(cluster_name, df)

        safe_name = cluster_name.replace(' & ', '_').replace('/', '_').replace(', ', '_').replace("'", "").replace("(", "").replace(")", "")
        output_file = os.path.join(output_dir, f"{idx:02d}_{safe_name}.html")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"   [OK] {output_file}")

    print(f"\n[DONE] {len(clusters)} Circos.js diagrams generated\n")

if __name__ == "__main__":
    main()
