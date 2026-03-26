"""
Generate static PNG images of each isolated circos diagram
Requires: pip install playwright
"""

import subprocess
import sys
import os
from pathlib import Path

# Install playwright if not already installed
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Installing playwright...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
    from playwright.sync_api import sync_playwright

def install_browser():
    """Install chromium browser for playwright"""
    print("Installing Chromium browser...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])

def generate_images():
    """Generate PNG images for each circos cluster"""

    # Install browser if needed
    try:
        from playwright.sync_api import sync_playwright
        sync_playwright().__enter__()
    except:
        install_browser()

    html_file = r"C:\Users\hoang\Documents\project_test\major_industry_circos_draft1\williams_isolated_clusters.html"
    output_dir = r"C:\Users\hoang\Documents\project_test\major_industry_circos_draft1\screenshots"

    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)

    # Cluster names for filenames
    clusters = [
        "01_Business_Management",
        "02_Engineering_Technology",
        "03_Natural_Health_Sciences",
        "04_Social_Sciences_Humanities",
        "05_Communication_Media",
        "06_Arts_Languages_Theology",
        "07_Education_Social_Services",
        "08_Unclassified"
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 1400})

        # Load HTML file
        file_url = f"file:///{html_file}".replace("\\", "/")
        print(f"Loading: {file_url}")
        page.goto(file_url)
        print("Page loaded, waiting for scripts to initialize...")
        page.wait_for_timeout(3000)  # Wait for D3 to render

        # Take screenshots for each tab
        for idx, cluster_name in enumerate(clusters):
            print(f"Capturing {idx + 1}/8: {cluster_name}...")

            # Click tab
            tabs = page.locator(".tab")
            tabs.nth(idx).click()
            page.wait_for_timeout(2000)  # Wait for chart to re-render

            # Take full page screenshot
            output_file = os.path.join(output_dir, f"{cluster_name}.png")
            page.screenshot(path=output_file, full_page=True)
            print(f"✓ Saved: {output_file}")

        # Also take a screenshot of the tab bar showing all tabs
        page.goto(file_url)
        page.wait_for_timeout(2000)
        tab_screenshot = os.path.join(output_dir, "00_All_Tabs_Navigation.png")
        page.locator(".tabs").screenshot(path=tab_screenshot)
        print(f"✓ Saved tab navigation: {tab_screenshot}")

        browser.close()

    print(f"\n✅ All images generated in: {output_dir}")
    print(f"Total: {len(clusters)} cluster visualizations + tab navigation")

if __name__ == "__main__":
    try:
        generate_images()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the HTML file exists at the specified path")
        sys.exit(1)
