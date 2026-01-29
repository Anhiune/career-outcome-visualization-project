# How to Create the Major-Industry Visualization

This guide covers how to set up your environment, run the visualization script, and interact with the result.

## 1. Update Your Environment

We added new libraries (`holoviews`, `bokeh`) to the `environment.yml` file. You need to update your existing `ml_env` environment.

1.  Open your terminal in VS Code (Ctrl+`).
2.  Run the following command:

    ```bash
    conda env update -f environment.yml --prune
    ```

3.  Activate the environment:

    ```bash
    conda activate ml_env
    ```

### Option B: Quick Start (If Conda fails)
If `conda` isn't working for you, you can install the libraries directly into your current Python:

```bash
pip install pandas holoviews bokeh
```

## 2. Run the Visualization Script

1.  Navigate to the project folder if you aren't already there:
    ```bash
    cd c:\Users\hoang\Documents\project_test
    ```

2.  Run the Python script:
    ```bash
    python major_industry_circos_draft1/visualize_connections.py
    ```

    You should see output indicating that the data is loading and the visualization is being saved.

## 3. View the Result

1.  After the script finishes, a new file named `major_industry_chord.html` will appear in the `major_industry_circos_draft1` folder.
2.  Open this file in your web browser. A convenient way to do this from VS Code is:
    *   Right-click `major_industry_chord.html` in the file explorer.
    *   Select **"Open in Default Browser"** (or similar option).
    *   OR, locate the file in your Windows File Explorer and double-click it.

## 4. Interacting with the Visualization

*   **Hover**: Move your mouse over any arc (representing a Major or Industry) to highlight the connections associated with it.
*   **Colors**: The colors are based on the custom palette (Purple, Grey, Green) you requested.

---
**Note**: The visualization uses the numeric IDs from your data (e.g., "4", "5") because the original file contains numbers. If you interpret these numbers as names, the visualization will show those connections.
