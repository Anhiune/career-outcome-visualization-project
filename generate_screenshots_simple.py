"""
Generate PNG screenshots using Python Playwright - Simplified version
"""

import sys
import os
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    print("[INFO] Playwright imported successfully")
except ImportError:
    print("[ERROR] Playwright not installed")
    sys.exit(1)

html_file = r"C:\Users\hoang\Documents\project_test\major_industry_circos_draft1\williams_isolated_clusters.html"
output_dir = r"C:\Users\hoang\Documents\project_test\major_industry_circos_draft1\screenshots"

Path(output_dir).mkdir(exist_ok=True)

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

print("[INFO] Starting Playwright browser...")

with sync_playwright() as p:
    print("[INFO] Launching Chromium browser...")
    browser = p.chromium.launch(headless=True)

    print("[INFO] Creating new page...")
    page = browser.new_page(viewport={"width": 1200, "height": 1400})

    file_url = f"file:///{html_file}".replace("\\", "/")
    print(f"[INFO] Loading HTML file...")
    page.goto(file_url, wait_until="networkidle")
    print("[INFO] Page loaded, waiting for chart to render...")
    page.wait_for_timeout(3000)

    for idx, cluster_name in enumerate(clusters):
        print(f"[{idx + 1}/8] Capturing {cluster_name}...")

        try:
            # Click the tab
            tabs = page.locator(".tab")
            if tabs.count() > idx:
                tabs.nth(idx).click()
                page.wait_for_timeout(2000)

            # Take screenshot
            output_file = os.path.join(output_dir, f"{cluster_name}.png")
            page.screenshot(path=output_file, full_page=False)

            file_size = os.path.getsize(output_file) / 1024
            print(f"  [OK] Saved {cluster_name}.png ({file_size:.1f} KB)")

        except Exception as e:
            print(f"  [ERROR] Failed to capture {cluster_name}: {e}")

    browser.close()
    print("[SUCCESS] Screenshot generation completed!")
    print(f"[INFO] Images saved to: {output_dir}")
