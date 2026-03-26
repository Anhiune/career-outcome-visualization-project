# Circos Career Pathways Visualizations - Summary

## Overview
Created **7 static circos diagrams** showing career pathways for each major cluster, using colorblind-friendly palette with semantic coloring.

## Generated Files

### Output Locations
- **HTML (Interactive)**: `circos_outputs/html/`
- **PNG (Static Images)**: `circos_outputs/png/`

### Major Clusters (7 Total)

| # | Major Cluster | PNG File | Total Graduates | Largest Career Cluster |
|---|---|---|---|---|
| 1 | BUSINESS & MANAGEMENT | 01_BUSINESS_MANAGEMENT.png | 1,570 | Business & Finance (480, 30.6%) |
| 2 | ENGINEERING & TECHNOLOGY | 02_ENGINEERING_TECHNOLOGY.png | 462 | Technology & Engineering (245, 53.0%) |
| 3 | NATURAL & HEALTH SCIENCES | 03_NATURAL_HEALTH SCIENCES.png | 436 | Healthcare & Science (165, 37.8%) |
| 4 | SOCIAL SCIENCES & HUMANITIES | 04_SOCIAL SCIENCES_HUMANITIES.png | 271 | (Diverse distribution) |
| 5 | COMMUNICATION & MEDIA | 05_COMMUNICATION_MEDIA.png | 160 | Business & Finance |
| 6 | ARTS, LANGUAGES & THEOLOGY | 06_ARTS_LANGUAGES_THEOLOGY.png | 86 | Business & Finance |
| 7 | EDUCATION & SOCIAL SERVICES | 07_EDUCATION_SOCIAL SERVICES.png | 78 | Education & Service |

## Color Palette

### Major Clusters (Left Node - Semantic Colors)
- **BUSINESS & MANAGEMENT**: #332288 (Indigo - Corporate)
- **ENGINEERING & TECHNOLOGY**: #44AA99 (Teal - Technical)
- **NATURAL & HEALTH SCIENCES**: #88CCEE (Cyan - Nature/Health)
- **SOCIAL SCIENCES & HUMANITIES**: #DDCC77 (Gold - Knowledge)
- **COMMUNICATION & MEDIA**: #CC6677 (Rose)
- **ARTS, LANGUAGES & THEOLOGY**: #882255 (Wine - Creative)
- **EDUCATION & SOCIAL SERVICES**: #117733 (Green - Nurturing)

### Career Clusters (Right Nodes)
- **Business & Finance**: #4477AA (Blue)
- **Technology & Engineering**: #66CCBB (Teal)
- **Healthcare & Science**: #99DDFF (Light Cyan)
- **Education & Service**: #228833 (Green)
- **Arts, Media & Legal**: #AA3377 (Magenta)
- **Unclassified**: #BBBBBB (Light Gray)

## Visualization Features

### Each Circos Diagram Shows:
1. **Left Node**: Major cluster (labeled)
2. **Right Nodes**: Career destination clusters (arranged in circle)
3. **Flow Lines**: Bezier curves connecting major to career clusters
   - **Line Thickness**: Proportional to number of students
   - **Line Color**: Matches major cluster color
   - **Transparency**: 40% opacity, 80% on hover
4. **Legend**: Color legend with all career destinations
5. **Statistics**: Distribution breakdown showing percentages

### Interactive HTML Features:
- Hover on flows to see student counts and percentages
- Responsive design that adapts to screen size
- Clean typography with Manrope font
- Colorblind-friendly palette (no red/green contrast)

## Data Source
- Source: `Major_Career_Analysis_v4__*` CSV files
- Analysis: Major cluster → Career cluster pathways
- Total Students: 3,201

## Technical Details
- Generated with: Python + pandas + D3.js
- Browser compatibility: Modern browsers (Chrome, Firefox, Safari, Edge)
- Image format: PNG at 1200x800px
- HTML format: Standalone, no server required

## Key Insights

| Cluster | Key Finding |
|---|---|
| Business & Management | Largest cluster (1,570 students); 62.7% unclassified, 30.6% to Business & Finance |
| Engineering & Technology | Strong technical pipeline; 53% to Technology & Engineering roles |
| Natural & Health Sciences | Balanced between healthcare (37.8%) and tech (11.9%) roles |
| Social Sciences & Humanities | Diverse pathways, requires further analysis |
| Communication & Media | Small cluster; leads primarily to Business & Finance |
| Arts, Languages & Theology | Smallest cluster; mixed career destinations |
| Education & Social Services | Smallest cluster; 64.1% to Education & Service roles |

## Files Generated
✓ 7 HTML interactive visualizations
✓ 7 PNG static images
✓ Each PNG: ~127 KB
✓ Total PNG size: ~896 KB
