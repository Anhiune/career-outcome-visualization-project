"""
Reusable chart components for the Career Pathways Dashboard.

All functions accept a DataFrame (or aggregated data) and return a Plotly
figure object.  The dashboard pages import these instead of building charts
inline, which keeps the visualization logic centralized and testable.
"""

from __future__ import annotations

import math
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from dashboard.config import MAJOR_CLUSTER_COLORS, INDUSTRY_COLORS


# ── Helper: hex colour with alpha ────────────────────────────────────────────

def _hex_to_rgba(hex_color: str, alpha: float = 0.45) -> str:
    """Convert '#RRGGBB' to 'rgba(R,G,B,alpha)'."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# ── Chord / Circos Diagram ──────────────────────────────────────────────────

def _arc_points(theta_start: float, theta_end: float, r: float, n: int = 60):
    """Return x, y arrays tracing an arc from theta_start to theta_end."""
    angles = np.linspace(theta_start, theta_end, n)
    return r * np.cos(angles), r * np.sin(angles)


def _ribbon_path(
    src_start: float, src_end: float,
    tgt_start: float, tgt_end: float,
    r: float = 0.92,
) -> str:
    """SVG path for a Bézier ribbon between two arcs on the circle."""
    # Source arc endpoints
    sx0, sy0 = r * math.cos(src_start), r * math.sin(src_start)
    sx1, sy1 = r * math.cos(src_end),   r * math.sin(src_end)
    # Target arc endpoints
    tx0, ty0 = r * math.cos(tgt_start), r * math.sin(tgt_start)
    tx1, ty1 = r * math.cos(tgt_end),   r * math.sin(tgt_end)

    # Build path: source arc → Bézier to target start → target arc → Bézier back
    def arc_svg(t0, t1, radius, n=30):
        angles = np.linspace(t0, t1, n)
        pts = [f"L {radius*math.cos(a):.4f} {radius*math.sin(a):.4f}" for a in angles[1:]]
        return " ".join(pts)

    path = (
        f"M {sx0:.4f} {sy0:.4f} "
        + arc_svg(src_start, src_end, r)
        + f" Q 0 0 {tx0:.4f} {ty0:.4f} "
        + arc_svg(tgt_start, tgt_end, r)
        + f" Q 0 0 {sx0:.4f} {sy0:.4f} Z"
    )
    return path


def chord_major_industry(df: pd.DataFrame) -> go.Figure:
    """Circos-style chord diagram: Major Cluster ↔ Industry Group."""

    ct = pd.crosstab(df["Major Cluster"], df["Industry Group"])
    majors = list(ct.index)
    industries = list(ct.columns)
    all_labels = majors + industries
    n = len(all_labels)

    # Total flow for each node (determines arc width)
    totals = []
    for m in majors:
        totals.append(int(ct.loc[m].sum()))
    for ind in industries:
        totals.append(int(ct[ind].sum()))

    grand_total = sum(totals)
    gap_frac = 0.02          # gap between arcs (fraction of circle)
    total_gap = gap_frac * n
    arc_total = 2 * math.pi * (1 - total_gap / (2 * math.pi + total_gap))
    # Simpler: total angle for arcs = 2π - n*gap_angle
    gap_angle = 2 * math.pi * gap_frac
    arc_angle_total = 2 * math.pi - n * gap_angle

    # Compute start/end angle for each node
    node_angles = []  # list of (start, end) in radians
    cursor = 0.0
    for t in totals:
        span = arc_angle_total * (t / grand_total)
        node_angles.append((cursor, cursor + span))
        cursor += span + gap_angle

    # ── Outer arcs (thick coloured bands) ────────────────────────────────
    shapes = []
    annotations = []
    arc_traces = []     # invisible scatter for hover

    r_inner, r_outer = 0.92, 1.0
    r_label = 1.10

    for i, label in enumerate(all_labels):
        t0, t1 = node_angles[i]
        color = (MAJOR_CLUSTER_COLORS.get(label)
                 or INDUSTRY_COLORS.get(label)
                 or "#888888")

        # Draw thick arc as an SVG path (filled wedge between r_inner and r_outer)
        n_pts = 40
        angles = np.linspace(t0, t1, n_pts)
        outer_x = r_outer * np.cos(angles)
        outer_y = r_outer * np.sin(angles)
        inner_x = r_inner * np.cos(angles[::-1])
        inner_y = r_inner * np.sin(angles[::-1])

        xs = np.concatenate([outer_x, inner_x, [outer_x[0]]])
        ys = np.concatenate([outer_y, inner_y, [outer_y[0]]])

        # Build SVG path for the arc band
        path_d = f"M {xs[0]:.4f} {ys[0]:.4f} "
        path_d += " ".join(f"L {x:.4f} {y:.4f}" for x, y in zip(xs[1:], ys[1:]))
        path_d += " Z"

        shapes.append(dict(
            type="path", path=path_d,
            fillcolor=color, line=dict(color=color, width=0.5),
            layer="above",
        ))

        # Label
        mid_angle = (t0 + t1) / 2
        lx = r_label * math.cos(mid_angle)
        ly = r_label * math.sin(mid_angle)
        angle_deg = math.degrees(mid_angle)
        # Flip text on left side so it reads correctly
        text_angle = -angle_deg if -90 < angle_deg < 90 or angle_deg > 270 else 180 - angle_deg
        # Wrapping long labels
        display_label = label.replace(" & ", " &<br>").replace(" / ", " /<br>")

        annotations.append(dict(
            x=lx, y=ly, text=f"<b>{display_label}</b>",
            showarrow=False,
            font=dict(size=9, color=color),
            textangle=text_angle if abs(text_angle) < 90 else 0,
            xanchor="center", yanchor="middle",
        ))

        # Invisible trace for hover on the arc
        hover_x, hover_y = _arc_points(t0, t1, (r_inner + r_outer) / 2, 10)
        arc_traces.append(go.Scatter(
            x=hover_x, y=hover_y,
            mode="markers", marker=dict(size=6, color=color, opacity=0),
            hoverinfo="text",
            text=f"<b>{label}</b><br>{totals[i]:,} graduates",
            showlegend=False,
        ))

    # ── Ribbons (chords) ─────────────────────────────────────────────────
    # Track how much of each node's arc has been consumed
    consumed = [0.0] * n

    for i, major in enumerate(majors):
        for j, industry in enumerate(industries):
            val = int(ct.loc[major, industry])
            if val == 0:
                continue

            j_global = len(majors) + j

            # Source arc sub-span
            src_span = node_angles[i][1] - node_angles[i][0]
            src_start = node_angles[i][0] + consumed[i]
            src_frac = val / totals[i] * src_span
            src_end = src_start + src_frac
            consumed[i] += src_frac

            # Target arc sub-span
            tgt_span = node_angles[j_global][1] - node_angles[j_global][0]
            tgt_start = node_angles[j_global][0] + consumed[j_global]
            tgt_frac = val / totals[j_global] * tgt_span
            tgt_end = tgt_start + tgt_frac
            consumed[j_global] += tgt_frac

            color = MAJOR_CLUSTER_COLORS.get(major, "#888")
            ribbon_path = _ribbon_path(src_start, src_end, tgt_start, tgt_end, r=r_inner)

            shapes.append(dict(
                type="path", path=ribbon_path,
                fillcolor=_hex_to_rgba(color, 0.35),
                line=dict(color=_hex_to_rgba(color, 0.55), width=0.5),
                layer="below",
            ))

            # Hover point at midpoint of the chord
            mid_src = (src_start + src_end) / 2
            mid_tgt = (tgt_start + tgt_end) / 2
            hx = 0.4 * (math.cos(mid_src) + math.cos(mid_tgt))
            hy = 0.4 * (math.sin(mid_src) + math.sin(mid_tgt))
            arc_traces.append(go.Scatter(
                x=[hx], y=[hy],
                mode="markers", marker=dict(size=8, color=color, opacity=0),
                hoverinfo="text",
                text=f"<b>{major}</b> → <b>{industry}</b><br>{val:,} graduates",
                showlegend=False,
            ))

    # ── Assemble figure ──────────────────────────────────────────────────
    fig = go.Figure(data=arc_traces)
    fig.update_layout(
        shapes=shapes,
        annotations=annotations,
        title=dict(text="Major Cluster ↔ Industry Group (Chord Diagram)", font_size=16),
        xaxis=dict(visible=False, range=[-1.4, 1.4]),
        yaxis=dict(visible=False, range=[-1.4, 1.4], scaleanchor="x"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=750,
        width=750,
        margin=dict(l=60, r=60, t=60, b=60),
        showlegend=False,
    )
    return fig


# ── Sankey / Alluvial (kept for Career Pathways page) ────────────────────────

def sankey_major_industry(df: pd.DataFrame) -> go.Figure:
    """Create a Sankey diagram: Major Cluster → Industry Group."""
    ct = pd.crosstab(df["Major Cluster"], df["Industry Group"])
    sources, targets, values = [], [], []

    labels = list(ct.index) + list(ct.columns)
    n_src = len(ct.index)

    for i, src in enumerate(ct.index):
        for j, tgt in enumerate(ct.columns):
            val = ct.loc[src, tgt]
            if val > 0:
                sources.append(i)
                targets.append(n_src + j)
                values.append(int(val))

    # Colors
    node_colors = [MAJOR_CLUSTER_COLORS.get(l, "#888") for l in ct.index]
    node_colors += [INDUSTRY_COLORS.get(l, "#888") for l in ct.columns]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15, thickness=20,
            label=labels,
            color=node_colors,
        ),
        link=dict(source=sources, target=targets, value=values),
    ))
    fig.update_layout(
        title_text="Major Cluster → Industry Group (Student Flow)",
        font_size=12,
        height=600,
    )
    return fig


def sankey_three_level(df: pd.DataFrame) -> go.Figure:
    """Create a 3-level Sankey: Major Cluster → Industry Group → Job Function."""
    # Level 1: Major Cluster → Industry Group
    ct1 = pd.crosstab(df["Major Cluster"], df["Industry Group"])
    # Level 2: Industry Group → Job Function
    ct2 = pd.crosstab(df["Industry Group"], df["Job Function"])

    all_labels = (
        list(ct1.index)      # major clusters
        + list(ct1.columns)  # industry groups
        + list(ct2.columns)  # job functions
    )
    n_mc = len(ct1.index)
    n_ig = len(ct1.columns)

    sources, targets, values = [], [], []

    for i, mc in enumerate(ct1.index):
        for j, ig in enumerate(ct1.columns):
            v = ct1.loc[mc, ig]
            if v > 0:
                sources.append(i)
                targets.append(n_mc + j)
                values.append(int(v))

    for j, ig in enumerate(ct2.index):
        for k, jf in enumerate(ct2.columns):
            v = ct2.loc[ig, jf]
            if v > 0:
                sources.append(n_mc + j)
                targets.append(n_mc + n_ig + k)
                values.append(int(v))

    node_colors = (
        [MAJOR_CLUSTER_COLORS.get(l, "#888") for l in ct1.index]
        + [INDUSTRY_COLORS.get(l, "#888") for l in ct1.columns]
        + ["#ccc"] * len(ct2.columns)
    )

    fig = go.Figure(go.Sankey(
        node=dict(pad=15, thickness=18, label=all_labels, color=node_colors),
        link=dict(source=sources, target=targets, value=values),
    ))
    fig.update_layout(
        title_text="Major Cluster → Industry Group → Job Function",
        font_size=11,
        height=800,
    )
    return fig


# ── Bar Charts ───────────────────────────────────────────────────────────────

def stacked_bar_clusters(df: pd.DataFrame) -> go.Figure:
    """Stacked bar: Industry Group breakdown per Major Cluster."""
    ct = pd.crosstab(df["Major Cluster"], df["Industry Group"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100

    fig = go.Figure()
    for col in ct_pct.columns:
        fig.add_trace(go.Bar(
            name=col, x=ct_pct.index, y=ct_pct[col],
            marker_color=INDUSTRY_COLORS.get(col, "#888"),
        ))
    fig.update_layout(
        barmode="stack",
        title="Industry Destination by Major Cluster (%)",
        yaxis_title="Percentage",
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=-0.4),
    )
    return fig


def top_majors_bar(df: pd.DataFrame, n: int = 20) -> go.Figure:
    """Horizontal bar of top-n majors by student count."""
    counts = df["Major"].value_counts().head(n).sort_values()
    fig = px.bar(
        x=counts.values, y=counts.index,
        orientation="h",
        labels={"x": "Number of Graduates", "y": "Major"},
        title=f"Top {n} Majors by Number of Graduates",
    )
    fig.update_layout(height=max(400, n * 25))
    return fig


def job_function_bar(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar of job function distribution."""
    counts = df["Job Function"].value_counts().sort_values()
    fig = px.bar(
        x=counts.values, y=counts.index,
        orientation="h",
        labels={"x": "Number of Graduates", "y": "Job Function"},
        title="Career Outcomes by Job Function",
    )
    fig.update_layout(height=550)
    return fig


# ── Heatmap ──────────────────────────────────────────────────────────────────

def heatmap_major_industry(df: pd.DataFrame) -> go.Figure:
    """Heatmap of Major Cluster × Industry Group (% of cluster total)."""
    ct = pd.crosstab(df["Major Cluster"], df["Industry Group"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100

    fig = go.Figure(go.Heatmap(
        z=ct_pct.values,
        x=ct_pct.columns.tolist(),
        y=ct_pct.index.tolist(),
        colorscale="Blues",
        text=np.round(ct_pct.values, 1),
        texttemplate="%{text}%",
        hovertemplate="Cluster: %{y}<br>Industry: %{x}<br>Share: %{z:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title="Major Cluster → Industry Group (% of cluster graduates)",
        height=450,
        xaxis_tickangle=-40,
    )
    return fig


def heatmap_major_jobfn(df: pd.DataFrame) -> go.Figure:
    """Heatmap of Major Cluster × Job Function (% of cluster total)."""
    ct = pd.crosstab(df["Major Cluster"], df["Job Function"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100

    fig = go.Figure(go.Heatmap(
        z=ct_pct.values,
        x=ct_pct.columns.tolist(),
        y=ct_pct.index.tolist(),
        colorscale="Greens",
        text=np.round(ct_pct.values, 1),
        texttemplate="%{text}%",
        hovertemplate="Cluster: %{y}<br>Function: %{x}<br>Share: %{z:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        title="Major Cluster → Job Function (% of cluster graduates)",
        height=500,
        xaxis_tickangle=-40,
    )
    return fig


# ── Treemap ──────────────────────────────────────────────────────────────────

def treemap_overview(df: pd.DataFrame) -> go.Figure:
    """Treemap: Major Cluster → Major (sized by student count)."""
    agg = df.groupby(["Major Cluster", "Major"]).size().reset_index(name="Count")
    fig = px.treemap(
        agg,
        path=["Major Cluster", "Major"],
        values="Count",
        title="Student Distribution: Major Cluster → Major",
        color="Major Cluster",
        color_discrete_map=MAJOR_CLUSTER_COLORS,
    )
    fig.update_layout(height=600)
    return fig


# ── Sunburst ─────────────────────────────────────────────────────────────────

def sunburst_career(df: pd.DataFrame) -> go.Figure:
    """Sunburst: Industry Group → Job Function (sized by count)."""
    agg = df.groupby(["Industry Group", "Job Function"]).size().reset_index(name="Count")
    fig = px.sunburst(
        agg,
        path=["Industry Group", "Job Function"],
        values="Count",
        title="Career Destinations: Industry → Job Function",
        color="Industry Group",
        color_discrete_map=INDUSTRY_COLORS,
    )
    fig.update_layout(height=600)
    return fig


# ── Trend Line ───────────────────────────────────────────────────────────────

def trend_line(df: pd.DataFrame) -> go.Figure:
    """Line chart of graduates per year, stacked by Major Cluster."""
    yearly = df.groupby(["Graduation Year", "Major Cluster"]).size().reset_index(name="Count")
    fig = px.area(
        yearly,
        x="Graduation Year", y="Count",
        color="Major Cluster",
        color_discrete_map=MAJOR_CLUSTER_COLORS,
        title="Graduation Trends by Major Cluster",
    )
    fig.update_layout(height=400)
    return fig
