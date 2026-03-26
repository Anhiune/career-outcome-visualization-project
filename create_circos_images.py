"""
Generate static circos images for each major cluster showing pathways to careers.
Colorblind-friendly palette with semantic coloring.
"""

import pandas as pd
import json
import os
from pathlib import Path

# ==================== COLOR PALETTE ====================
# Colorblind-friendly palette with semantic mapping
MAJOR_COLORS = {
    "BUSINESS & MANAGEMENT": "#332288",      # Indigo - corporate
    "ENGINEERING & TECHNOLOGY": "#44AA99",   # Teal - technical
    "NATURAL & HEALTH SCIENCES": "#88CCEE",  # Cyan - nature/health
    "SOCIAL SCIENCES & HUMANITIES": "#DDCC77", # Gold - knowledge
    "COMMUNICATION & MEDIA": "#CC6677",      # Rose
    "ARTS, LANGUAGES & THEOLOGY": "#882255", # Wine - creative
    "EDUCATION & SOCIAL SERVICES": "#117733", # Green - nurturing
    "Unclassified": "#999999"                # Gray
}

CAREER_COLORS = {
    "Business & Finance": "#4477AA",      # Blue
    "Technology & Engineering": "#66CCBB", # Teal
    "Healthcare & Science": "#99DDFF",    # Light Cyan
    "Education & Service": "#228833",     # Green
    "Arts, Media & Legal": "#AA3377",     # Magenta
    "Unclassified": "#BBBBBB"             # Light Gray
}

# ==================== DATA LOADING ====================
def load_cluster_data(csv_file):
    """Load data for a specific major cluster"""
    df = pd.read_csv(csv_file)
    # Skip summary rows and get the flow data
    df = df[df['Major Cluster'].notna()].copy()
    df = df[['Major Cluster', 'Career Cluster', 'Count', 'Percentage']]
    df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
    df = df.dropna(subset=['Count'])
    return df

def load_all_clusters():
    """Load all major cluster export files"""
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

# ==================== CIRCOS HTML GENERATION ====================
def generate_circos_html(major_cluster, df, cluster_index):
    """Generate HTML for a single circos diagram"""

    # Prepare data
    major_color = MAJOR_COLORS.get(major_cluster, "#999999")
    connections = []

    for _, row in df.iterrows():
        career = row['Career Cluster']
        count = int(row['Count'])
        career_color = CAREER_COLORS.get(career, "#BBBBBB")

        connections.append({
            "source": major_cluster,
            "target": career,
            "value": count,
            "sourceColor": major_color,
            "targetColor": career_color
        })

    # Calculate total
    total = df['Count'].sum()

    # Prepare JavaScript data
    connections_json = json.dumps(connections)

    # Create HTML
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>""" + major_cluster + """ - Career Pathways Circos</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #f5f1e7 0%, #e9e2d1 100%);
            font-family: "Manrope", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
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
            margin: 0 0 10px 0;
            color: #1e1f1b;
            font-size: 28px;
            font-weight: 700;
        }

        .subtitle {
            text-align: center;
            color: rgba(30, 31, 27, 0.7);
            margin: 0 0 30px 0;
            font-size: 14px;
        }

        #circos {
            width: 100%;
            height: 600px;
            display: flex;
            justify-content: center;
        }

        .tooltip {
            position: absolute;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            pointer-events: none;
            display: none;
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
        }

        .legend-item {
            display: inline-block;
            margin-right: 24px;
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
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>""" + major_cluster + """</h1>
        <div class="subtitle">Career Pathways Flow - Total: """ + str(int(total)) + """ graduates</div>

        <div id="circos"></div>
        <div class="tooltip"></div>

        <div class="legend">
            <div class="legend-title">Career Destinations</div>
"""

    # Add career legend
    careers = df['Career Cluster'].unique()
    for career in sorted(careers):
        career_color = CAREER_COLORS.get(career, "#BBBBBB")
        html += f"""            <div class="legend-item">
                <span class="legend-color" style="background: {career_color};"></span>{career}
            </div>
"""

    # Add statistics
    html += """        </div>

        <div class="stats">
            <strong>Distribution by Career Cluster:</strong><br>
"""

    career_stats = df.groupby('Career Cluster')['Count'].sum().sort_values(ascending=False)
    for career, count in career_stats.items():
        pct = (count / total) * 100
        html += f"            {career}: {int(count)} ({pct:.1f}%)<br>\n"

    html += """        </div>
    </div>

    <script>
    const connections = """ + connections_json + """;
    const totalCount = """ + str(int(total)) + """;

    function createCircos() {
        const margin = {top: 20, right: 20, bottom: 20, left: 20};
        const containerWidth = document.getElementById('circos').offsetWidth;
        const width = containerWidth - margin.left - margin.right;
        const height = 600 - margin.top - margin.bottom;
        const radius = Math.min(width, height) / 2 - 60;

        const svg = d3.select('#circos')
            .append('svg')
            .attr('width', containerWidth)
            .attr('height', 600)
            .append('g')
            .attr('transform', 'translate(' + (containerWidth/2) + ',300)');

        // Get unique nodes
        const nodes = new Map();
        connections.forEach(d => {
            if (!nodes.has(d.source))
                nodes.set(d.source, {id: d.source, type: 'major', color: d.sourceColor});
            if (!nodes.has(d.target))
                nodes.set(d.target, {id: d.target, type: 'career', color: d.targetColor});
        });

        const nodeArray = Array.from(nodes.values());
        const majorNode = nodeArray.filter(n => n.type === 'major');
        const careerNodes = nodeArray.filter(n => n.type === 'career');

        // Position nodes
        const nodePositions = new Map();
        nodePositions.set(majorNode[0].id, {
            x: -radius,
            y: 0,
            angle: Math.PI
        });

        careerNodes.forEach((node, i) => {
            const angle = (Math.PI * 2 * i) / careerNodes.length;
            nodePositions.set(node.id, {
                x: radius * Math.cos(angle),
                y: radius * Math.sin(angle),
                angle: angle
            });
        });

        // Draw connections (ribbons)
        connections.forEach(function(d) {
            const source = nodePositions.get(d.source);
            const target = nodePositions.get(d.target);

            const dx = target.x - source.x;
            const dy = target.y - source.y;
            const dist = Math.sqrt(dx*dx + dy*dy);

            // Calculate thickness based on value
            const thickness = Math.max(1, (d.value / totalCount) * 20);

            // Draw bezier curve
            const midX = (source.x + target.x) / 2;
            const midY = (source.y + target.y) / 2;

            const path = 'M ' + source.x + ',' + source.y + ' Q ' + midX + ',' + midY + ' ' + target.x + ',' + target.y;

            svg.append('path')
                .attr('d', path)
                .attr('stroke', d.sourceColor)
                .attr('stroke-width', thickness)
                .attr('fill', 'none')
                .attr('opacity', 0.4)
                .style('pointer-events', 'stroke')
                .on('mouseover', function() {
                    d3.select(this).attr('opacity', 0.8).attr('stroke-width', thickness * 1.5);
                    const pct = ((d.value / totalCount) * 100).toFixed(1);
                    showTooltip(d.source + ' -> ' + d.target + ': ' + d.value + ' (' + pct + '%)');
                })
                .on('mouseout', function() {
                    d3.select(this).attr('opacity', 0.4).attr('stroke-width', thickness);
                    hideTooltip();
                });
        });

        // Draw nodes
        nodeArray.forEach(node => {
            const pos = nodePositions.get(node.id);
            const nodeSize = node.type === 'major' ? 20 : 12;

            svg.append('circle')
                .attr('cx', pos.x)
                .attr('cy', pos.y)
                .attr('r', nodeSize)
                .attr('fill', node.color)
                .attr('stroke', '#fff')
                .attr('stroke-width', 2)
                .raise();
        });

        // Add labels
        nodeArray.forEach(node => {
            const pos = nodePositions.get(node.id);
            const isLeft = node.type === 'major';
            const anchor = isLeft ? 'end' : 'start';
            const dx = isLeft ? -30 : 30;

            svg.append('text')
                .attr('x', pos.x + dx)
                .attr('y', pos.y + 4)
                .attr('text-anchor', anchor)
                .attr('font-size', node.type === 'major' ? '14px' : '12px')
                .attr('font-weight', node.type === 'major' ? '600' : '400')
                .attr('fill', '#1e1f1b')
                .text(node.id);
        });
    }

    function showTooltip(text) {
        const tooltip = document.querySelector('.tooltip');
        tooltip.textContent = text;
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

    window.addEventListener('load', createCircos);
    window.addEventListener('resize', function() {
        document.getElementById('circos').innerHTML = '';
        createCircos();
    });
    </script>
</body>
</html>"""

    return html

# ==================== MAIN EXECUTION ====================
def main():
    output_dir = r"C:\Users\hoang\Documents\project_test\circos_outputs\html"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print("\n" + "="*60)
    print("CIRCOS VISUALIZATION GENERATOR - MAJOR CLUSTERS")
    print("="*60 + "\n")

    # Load data
    clusters = load_all_clusters()

    if not clusters:
        print("\n[ERROR] No cluster data found!")
        return

    print(f"\n[OK] Loaded {len(clusters)} major clusters\n")

    # Generate HTML for each cluster
    for idx, (cluster_name, df) in enumerate(clusters.items(), 1):
        print(f"{idx}. Generating circos for {cluster_name}...")

        html = generate_circos_html(cluster_name, df, idx)

        # Save HTML
        safe_cluster_name = cluster_name.replace(' & ', '_').replace('/', '_').replace(', ', '_').replace("'", "").replace("(", "").replace(")", "")
        output_file = os.path.join(output_dir, f"{idx:02d}_{safe_cluster_name}.html")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"   [SAVED] {output_file}")

    print("\n" + "="*60)
    print(f"[OK] Generated {len(clusters)} circos HTML files")
    print(f"  Output directory: {output_dir}")
    print("="*60 + "\n")

    # Next step: screenshot generation
    print("\nNEXT STEP: Convert HTML to PNG screenshots")
    print("Run: create_circos_screenshots.py\n")

if __name__ == "__main__":
    main()
