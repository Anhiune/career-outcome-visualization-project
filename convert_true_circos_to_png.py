import subprocess
import sys
import os
from pathlib import Path

def install_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Installing playwright...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright", "-q"])
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])

def create_screenshots():
    from playwright.sync_api import sync_playwright

    html_dir = r"C:\Users\hoang\Documents\project_test\circos_final\html"
    output_dir = r"C:\Users\hoang\Documents\project_test\circos_final\png"

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    html_files = sorted([f for f in os.listdir(html_dir) if f.endswith('.html')])

    print("\n" + "="*60)
    print("CONVERTING TRUE CIRCOS TO PNG")
    print("="*60 + "\n")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1000, "height": 1100})

        for idx, html_file in enumerate(html_files, 1):
            html_path = os.path.join(html_dir, html_file)
            file_url = f"file:///{html_path}".replace("\\", "/")

            print(f"{idx}/{len(html_files)}: {html_file}")

            try:
                page.goto(file_url, wait_until="networkidle")
                page.wait_for_timeout(5000)

                output_file = os.path.join(output_dir, html_file.replace('.html', '.png'))
                page.screenshot(path=output_file, full_page=True)

                print(f"  [SAVED] {os.path.basename(output_file)}")

            except Exception as e:
                print(f"  [ERROR] {e}")

        browser.close()

    print(f"\n[OK] Generated {len(html_files)} PNG screenshots\n")

if __name__ == "__main__":
    try:
        install_playwright()
        create_screenshots()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
