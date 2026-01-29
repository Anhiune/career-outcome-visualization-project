# Major to Industry Data Visualization Project

This project provides two distinct ways to visualize the flow of college majors to industries: a **Static Circos-style Diagram** and an **Interactive Chord Diagram**.

## 1. Project Files

### Source Code
*   **`visualize_connections.py`**:
    *   **Purpose**: Processes the raw data (`data/college.txt`) to generate text files (`karyotype.txt`, `links.txt`) formatted for the Circos software. It also generates a standalone HTML page (`major_industry_map_view.html`) that embeds the resulting diagram image.
    *   **Method**: Static Python processing + Base64 Image Embedding.
*   **`interactive_dashboard.py`**:
    *   **Purpose**: Reads the raw data and generates a fully interactive HTML dashboard (`interactive_dashboard.html`) using the HoloViews and Bokeh libraries.
    *   **Method**: Python Interactive Visualization (HoloViews/Bokeh).

### Output Files (For Sharing)
*   **`major_industry_map_view.html`**:
    *   A single, self-contained HTML file.
    *   Contains the static Circos image embedded directly within it.
    *   **Best for**: Email attachment, offline viewing, printing.
*   **`interactive_dashboard.html`**:
    *   A single HTML file containing the interactive chart data.
    *   **Best for**: Exploration, hovering to see specific values, presentations.
    *   *Note*: Requires an internet connection to load visualization libraries (CDN).
*   **`major_industry_circos.png`**:
    *   The raw static image file.

### Data
*   **`data/college.txt`**: Input dataset linking majors to industries.

---

## 2. Methodology & Constraints

### Method A: Static Visualization (Circos)
This method aims for high-quality, publication-ready static imagery.

*   **Process**:
    1.  Python (`visualize_connections.py`) parses data and outputs configuration files (`karyotype.txt`, `links.txt`).
    2.  *External Step*: The Circos software (Perl-based) uses these files to render `major_industry_circos.png`.
    3.  Python puts this image into a nice HTML wrapper.
*   **Constraints**:
    *   **Not Interactive**: You cannot filter or hover over connections.
    *   **Dependency**: Regenerating the *image itself* requires installing Circos (Perl), which is complex. (Note: The provided HTML currently relies on the pre-generated image).
    *   **Resolution**: Zooming too far may pixelate the image (unless SVG is used).

### Method B: Interactive Visualization (Python/Bokeh)
This method focuses on user exploration and data accessibility.

*   **Process**:
    1.  Python (`interactive_dashboard.py`) loads data into a Pandas DataFrame.
    2.  HoloViews/Bokeh libraries render the visualization directly to HTML.
*   **Constraints**:
    *   **Visual Styling**: Harder to achieve the exact "artistic" look of Circos; generally looks more like a standard chart.
    *   **Browser Dependency**: Requires a modern web browser and (typically) an internet connection to load the JavaScript styling libraries.
    *   **Performance**: Extremely large datasets (thousands of connections) can make the browser laggy.

---

## 3. How to Run

### Prerequisites
*   Python 3.x
*   Conda Environment (recommended): `ml_env`
*   Libraries: `pandas`, `holoviews`, `bokeh`

### Running the Scripts
1.  **Activate Environment**:
    ```bash
    conda activate ml_env
    ```
2.  **Generate Interactive Dashboard**:
    ```bash
    python interactive_dashboard.py
    ```
    *Output*: `interactive_dashboard.html`
3.  **Generate Static Map View**:
    ```bash
    python visualize_connections.py
    ```
    *Output*: `major_industry_map_view.html`
