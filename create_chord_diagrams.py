"""
Generate TRUE CHORD DIAGRAMS using D3.js chord layout
Creates proper ribbon calculations with matrix-based flow data
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

def generate_true_chord_html(major_cluster, df):
    """Generate TRUE chord diagram using D3 chord layout"""

    major_color = MAJOR_COLORS.get(major_cluster, "#999999")

    # Get career list
    careers = sorted(df['Career Cluster'].unique().tolist())

    # Create matrix: [major_to_careers] and [careers_to_major] (symmetric)
    # Matrix is: rows=major+careers, cols=major+careers
    nodes = [major_cluster] + careers
    node_count = len(nodes)

    # Initialize matrix
    matrix = [[0] * node_count for _ in range(node_count)]

    # Fill matrix: major -> careers
    major_idx = 0
    for career in careers:
        career_idx = nodes.index(career)
        count = int(df[df['Career Cluster'] == career]['Count'].values[0])
        matrix[major_idx][career_idx] = count
        matrix[career_idx][major_idx] = count  # Symmetric for chord layout

    matrix_json = json.dumps(matrix)

    # Create color mapping
    color_map = {major_cluster: major_color}
    for career in careers:
        color_map[career] = CAREER_COLORS.get(career, "#BBBBBB")

    color_map_json = json.dumps(color_map)
    nodes_json = json.dumps(nodes)

    total_count = int(df['Count'].sum())

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + major_cluster + """ - Chord Diagram</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
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

        .chart-wrapper {
            display: flex;
            justify-content: center;
            position: relative;
            margin-bottom: 30px;
            background: radial-gradient(circle at center, rgba(255,255,255,0.9) 0%, transparent 70%);
            padding: 20px;
            border-radius: 16px;
        }

        svg {
            max-width: 100%;
            height: auto;
        }

        .ribbon {
            fill-opacity: 0.65;
            stroke: none;
        }

        .ribbon:hover {
            fill-opacity: 0.9;
            filter: drop-shadow(0 0 4px rgba(0,0,0,0.3));
        }

        .group-arc {
            stroke: white;
            stroke-width: 2;
        }

        .group-label {
            font-size: 11px;
            font-weight: 600;
            pointer-events: none;
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
            max-width: 300px;
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

        .major-indicator {
            text-align: center;
            color: rgba(30, 31, 27, 0.6);
            font-size: 12px;
            margin-top: 10px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>""" + major_cluster + """</h1>
        <div class="subtitle">Career Pathways - True Chord Diagram</div>

        <div class="chart-wrapper">
            <svg id="chord-svg" width="850" height="850"></svg>
            <div class="tooltip"></div>
            <div class="major-indicator">Major Cluster (Left Side)</div>
        </div>

        <div class="legend">
            <div class="legend-title">Career Destinations (Right Side)</div>
"""

    # Add legend for careers
    for career in careers:
        career_color = CAREER_COLORS.get(career, "#BBBBBB")
        html += f"""            <div class="legend-item">
                <span class="legend-color" style="background: {career_color};"></span>{career}
            </div>
"""

    # Add statistics
    html += """        </div>

        <div class="stats">
            <strong>Distribution:</strong><br>
"""

    career_stats = df.groupby('Career Cluster')['Count'].sum().sort_values(ascending=False)
    for career, count in career_stats.items():
        pct = (count / total_count) * 100
        html += f"            {career}: {int(count)} ({pct:.1f}%)<br>\n"

    html += """        </div>
    </div>

    <script>
    const matrix = """ + matrix_json + """;
    const nodes = """ + nodes_json + """;
    const colorMap = """ + color_map_json + """;
    const majorCluster = '""" + major_cluster + """';
    const total = """ + str(total_count) + """;

    function createChordDiagram() {
        const width = 850;
        const height = 850;
        const innerRadius = Math.min(width, height) * 0.3;
        const outerRadius = innerRadius + 40;

        const svg = d3.select('#chord-svg');
        const group = svg.append('g')
            .attr('transform', 'translate(' + width/2 + ',' + height/2 + ')');

        // Create chord layout
        const chordLayout = d3.chord()
            .padAngle(0.05)
            .sortSubgroups(d3.descending);

        const chords = chordLayout(matrix);

        // Create color scale
        const colorScale = d3.scaleOrdinal()
            .domain(nodes)
            .range(nodes.map(d => colorMap[d]));

        // Draw ribbon paths
        const ribbon = d3.ribbon()
            .source(d => d.source)
            .target(d => d.target);

        group.append('g')
            .selectAll('path')
            .data(chords)
            .join('path')
            .attr('class', 'ribbon')
            .attr('d', ribbon)
            .attr('fill', d => colorScale(nodes[d.source.index]))
            .attr('opacity', 0.65)
            .on('mouseover', function(event, d) {
                const source = nodes[d.source.index];
                const target = nodes[d.target.index];
                const value = matrix[d.source.index][d.target.index];
                const pct = ((value / total) * 100).toFixed(1);

                // Highlight this ribbon
                d3.select(this).attr('opacity', 0.9);

                showTooltip(source + ' -> ' + target + '<br>' + value + ' students (' + pct + '%)');
            })
            .on('mouseout', function() {
                d3.select(this).attr('opacity', 0.65);
                hideTooltip();
            });

        // Draw arcs
        const arcGenerator = d3.arc()
            .innerRadius(innerRadius)
            .outerRadius(outerRadius);

        group.append('g')
            .selectAll('g')
            .data(chords.groups)
            .join('g')
            .append('path')
            .attr('class', 'group-arc')
            .attr('d', arcGenerator)
            .attr('fill', d => colorScale(nodes[d.index]))
            .attr('stroke', 'white')
            .attr('stroke-width', 2);

        // Add labels
        group.append('g')
            .selectAll('text')
            .data(chords.groups)
            .join('text')
            .attr('class', 'group-label')
            .attr('dy', d => {
                const angle = (d.startAngle + d.endAngle) / 2;
                return Math.sin(angle) > 0 ? 15 : -5;
            })
            .append('textPath')
            .attr('href', (d, i) => '#arc-' + i)
            .attr('startOffset', '50%')
            .attr('text-anchor', 'middle')
            .text(d => nodes[d.index])
            .style('font-size', '11px')
            .style('font-weight', '600');

        // Draw arcs for path references
        group.selectAll('defs')
            .data(chords.groups)
            .enter()
            .append('defs')
            .append('path')
            .attr('id', (d, i) => 'arc-' + i)
            .attr('d', arcGenerator);
    }

    function showTooltip(html) {
        const tooltip = document.querySelector('.tooltip');
        tooltip.innerHTML = html;
        tooltip.style.display = 'block';
        document.addEventListener('mousemove', moveTooltip);
    }

    function hideTooltip() {
        document.querySelector('.tooltip').style.display = 'none';
        document.removeEventListener('mousemove', moveTooltip);
    }

    function moveTooltip(e) {
        const tooltip = document.querySelector('.tooltip');
        tooltip.style.left = (e.pageX + 10) + 'px';
        tooltip.style.top = (e.pageY + 10) + 'px';
    }

    window.addEventListener('load', createChordDiagram);
    </script>
</body>
</html>"""

    return html

def main():
    output_dir = r"C:\Users\hoang\Documents\project_test\chord_diagrams\html"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print("\n" + "="*60)
    print("TRUE CHORD DIAGRAM GENERATOR (D3 Chord Layout)")
    print("="*60 + "\n")

    clusters = load_all_clusters()

    if not clusters:
        print("[ERROR] No cluster data found!")
        return

    print(f"\n[OK] Loaded {len(clusters)} major clusters\n")

    for idx, (cluster_name, df) in enumerate(clusters.items(), 1):
        print(f"{idx}. Generating {cluster_name}...")

        html = generate_true_chord_html(cluster_name, df)

        safe_name = cluster_name.replace(' & ', '_').replace('/', '_').replace(', ', '_').replace("'", "").replace("(", "").replace(")", "")
        output_file = os.path.join(output_dir, f"{idx:02d}_{safe_name}.html")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"   [OK] {output_file}")

    print(f"\n[DONE] {len(clusters)} TRUE chord diagrams generated\n")

if __name__ == "__main__":
    main()
