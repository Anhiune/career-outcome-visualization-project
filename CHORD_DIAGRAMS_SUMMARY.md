# Circular Chord Diagrams - Career Pathways Analysis

## Overview
Generated **7 interactive HTML & static PNG circular chord diagrams** for each major cluster showing pathways to career destinations.

## Generated Files

**Location:** `C:\Users\hoang\Documents\project_test\chord_diagrams\`
- **HTML (Interactive):** `chord_diagrams/html/` - Open in browser for interactivity
- **PNG (Static Images):** `chord_diagrams/png/` - Ready for presentations, reports, publications

## 7 Major Clusters Visualized

| # | Major Cluster | File | File Size | Total Students |
|---|---|---|---|---|
| 1 | BUSINESS & MANAGEMENT | 01_BUSINESS_MANAGEMENT.png | 129 KB | 1,570 |
| 2 | ENGINEERING & TECHNOLOGY | 02_ENGINEERING_TECHNOLOGY.png | 128 KB | 462 |
| 3 | NATURAL & HEALTH SCIENCES | 03_NATURAL_HEALTH SCIENCES.png | 128 KB | 436 |
| 4 | SOCIAL SCIENCES & HUMANITIES | 04_SOCIAL SCIENCES_HUMANITIES.png | 128 KB | 271 |
| 5 | COMMUNICATION & MEDIA | 05_COMMUNICATION_MEDIA.png | 128 KB | 160 |
| 6 | ARTS, LANGUAGES & THEOLOGY | 06_ARTS_LANGUAGES_THEOLOGY.png | 129 KB | 86 |
| 7 | EDUCATION & SOCIAL SERVICES | 07_EDUCATION_SOCIAL SERVICES.png | 128 KB | 78 |

**Total:** 896 KB PNG images

## Diagram Features

### Visual Elements
- **Center Node (Major Cluster):** Large colored circle showing the academic major
- **Outer Nodes (Career Clusters):** 6 career destination circles arranged in a circle
- **Flow Lines:** Curved ribbons connecting major to careers
  - **Line Thickness:** Proportional to number of students (thicker = more students)
  - **Line Color:** Matches career cluster color for easy identification
  - **Transparency:** 50% opacity, becomes 90% on hover
- **Student Counts:** Numbers shown below each career node
- **Distribution Table:** Summary statistics at bottom showing exact counts and percentages

### Colorblind-Friendly Palette

**Major Clusters (Center Node)**
- BUSINESS & MANAGEMENT: #332288 (Indigo - corporate)
- ENGINEERING & TECHNOLOGY: #44AA99 (Teal - technical)
- NATURAL & HEALTH SCIENCES: #88CCEE (Cyan - health/science)
- SOCIAL SCIENCES & HUMANITIES: #DDCC77 (Gold - knowledge)
- COMMUNICATION & MEDIA: #CC6677 (Rose)
- ARTS, LANGUAGES & THEOLOGY: #882255 (Wine - creative)
- EDUCATION & SOCIAL SERVICES: #117733 (Green - service/education)

**Career Destinations (Outer Nodes)**
- Business & Finance: #4477AA (Blue)
- Technology & Engineering: #66CCBB (Teal)
- Healthcare & Science: #99DDFF (Light Cyan)
- Education & Service: #228833 (Green)
- Arts, Media & Legal: #AA3377 (Magenta)
- Unclassified: #BBBBBB (Gray)

## Key Insights

| Major Cluster | Top Career Destination | Count | % |
|---|---|---|---|
| Business & Management | Unclassified | 984 | 62.7% |
| Engineering & Technology | Technology & Engineering | 245 | 53.0% |
| Natural & Health Sciences | Healthcare & Science | 165 | 37.8% |
| Social Sciences & Humanities | Unclassified | 133 | 49.1% |
| Communication & Media | Business & Finance | 58 | 36.3% |
| Arts, Languages & Theology | Business & Finance | 19 | 22.1% |
| Education & Social Services | Education & Service | 50 | 64.1% |

## Usage

### View PNG Images (Static)
- Open any `.png` file in image viewer, browser, or presentation software
- Ready for: PowerPoint, Google Slides, reports, papers, websites

### View HTML Interactive (Interactive)
- Double-click any `.html` file to open in default browser
- **Hover** over flow lines to see:
  - Source and destination
  - Student count
  - Percentage of total
- Responsive design works on desktop/tablet

## Technical Details

- **Generated with:** Python + Pandas + D3.js
- **Data source:** Major_Career_Analysis_v4 CSV files
- **Resolution:** 800×800 SVG (converts to high-quality PNG)
- **Format:** Standalone, no server required
- **Colorblind accessible:** No red/green contrast

## Next Steps

1. **Use PNG images** for presentations, reports, dissertations
2. **Share HTML files** for interactive exploration in browser
3. **Export PNG** at higher resolution using Chrome dev tools if needed
4. **Customize colors** by editing the HTML color values if desired

---
Generated: 2026-03-18
Data: Major Career Analysis v4
