"""
run.py — One command to rule them all.

    python run.py           → run pipeline + launch dashboard
    python run.py --mock    → force mock data
    python run.py --no-dash → pipeline only, skip dashboard
    python run.py --dash    → dashboard only (skip pipeline)

Edit settings.py first to point INPUT_FILE at your data.
"""

import sys
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(
        description="UST Career Pathways — run pipeline and/or dashboard",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--mock", action="store_true",
                        help="Use built-in mock data (ignores INPUT_FILE)")
    parser.add_argument("--no-dash", action="store_true",
                        help="Run pipeline only, don't launch dashboard")
    parser.add_argument("--dash", action="store_true",
                        help="Launch dashboard only (skip pipeline)")
    parser.add_argument("--stage", type=int, default=1,
                        help="Start pipeline from this stage (1-4)")
    args = parser.parse_args()

    # ── Pipeline ─────────────────────────────────────────────────────────
    if not args.dash:
        pipeline_cmd = [sys.executable, "-m", "reproducibility.run_pipeline"]
        if args.mock:
            pipeline_cmd.append("--mock")
        if args.stage > 1:
            pipeline_cmd.extend(["--stage", str(args.stage)])

        result = subprocess.run(pipeline_cmd, cwd=str(ROOT))
        if result.returncode != 0:
            print("\n❌ Pipeline failed. Fix the errors above and re-run.")
            sys.exit(1)

        # Validate
        print("\nRunning validation …")
        val_result = subprocess.run(
            [sys.executable, "-m", "reproducibility.validate"],
            cwd=str(ROOT),
        )
        if val_result.returncode != 0:
            print("\n⚠️  Validation had failures. Dashboard may show incomplete data.")

    # ── Dashboard ────────────────────────────────────────────────────────
    if not args.no_dash:
        print("\n🚀 Launching dashboard at  http://localhost:8501\n")
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "dashboard/app.py",
             "--server.headless", "true"],
            cwd=str(ROOT),
        )


if __name__ == "__main__":
    main()
