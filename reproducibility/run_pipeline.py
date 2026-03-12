"""
Pipeline runner — runs all four stages in order.

Usage:
    python -m reproducibility.run_pipeline          # uses settings.py
    python -m reproducibility.run_pipeline --mock   # force mock data
    python -m reproducibility.run_pipeline --stage 2  # run from stage 2 onward

Or just:  python run.py   (which calls this automatically)
"""

import sys
import time
import argparse
from pathlib import Path

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main():
    parser = argparse.ArgumentParser(description="Run the UST Career Pathways pipeline")
    parser.add_argument("--mock", action="store_true", help="Force mock data (ignore INPUT_FILE)")
    parser.add_argument("--stage", type=int, default=1, choices=[1, 2, 3, 4],
                        help="Start from this stage (default: 1)")
    args = parser.parse_args()

    # If --mock, temporarily override settings
    if args.mock:
        import settings
        settings.INPUT_FILE = None
        settings.RAW_DATA_FILE = None
        settings.USE_MOCK = True

    from settings import USE_MOCK, RAW_DATA_FILE, MOCK_DATA_DIR

    print("=" * 60)
    print("  UST Career Pathways — Reproducibility Pipeline")
    print("=" * 60)

    if USE_MOCK:
        print("\n📋 DATA SOURCE: Mock data (built-in)")
        print("   To use your own file → open settings.py, set INPUT_FILE\n")

        # Generate mock CSV so stage 01 can read it
        mock_csv = MOCK_DATA_DIR / "mock_dataset.csv"
        if not mock_csv.exists():
            print("[mock] Generating mock dataset …")
            from dashboard.mock_data.generate_mock import generate_mock_dataset, write_csv
            rows = generate_mock_dataset()
            write_csv(rows, mock_csv)
            print(f"[mock] ✅ {len(rows):,} rows → {mock_csv.name}")
        else:
            print(f"[mock] Using existing {mock_csv.name}")

        # Point the pipeline at the mock CSV
        import settings
        settings.RAW_DATA_FILE = mock_csv
    else:
        print(f"\n📂 DATA SOURCE: {RAW_DATA_FILE}")
        if not RAW_DATA_FILE.exists():
            print(f"\n❌ File not found: {RAW_DATA_FILE}")
            print("   Check INPUT_FILE in settings.py and try again.")
            sys.exit(1)

    # ── Run stages ───────────────────────────────────────────────────────
    t0 = time.time()

    from reproducibility.stages.stage_01_clean import clean
    from reproducibility.stages.stage_02_classify import classify
    from reproducibility.stages.stage_03_analyze import analyze
    from reproducibility.stages.stage_04_export import export

    stages = [
        (1, "Clean",    clean),
        (2, "Classify", classify),
        (3, "Analyze",  analyze),
        (4, "Export",   export),
    ]

    for num, name, fn in stages:
        if num < args.stage:
            print(f"\n── Stage {num}: {name} (skipped) ──")
            continue
        print(f"\n── Stage {num}: {name} ──")
        fn()

    elapsed = time.time() - t0
    print(f"\n{'=' * 60}")
    print(f"  ✅ Pipeline complete in {elapsed:.1f}s")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
