"""
05.1. build_features.py — Feature engineering pipeline orchestrator.

Runs sequentially:
  1. src/build_product_dataset.py  → output/product_dataset.csv
  2. src/nlp_features.py           → output/product_features.csv

Run from project root:
    python "05.1. build_features.py"
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

STEPS = [
    ("src.build_product_dataset", "Build product-level dataset"),
    ("src.nlp_features",          "Extract NLP features"),
]


def run_step(module: str, label: str) -> int:
    print(f"\n{'='*60}")
    print(f"⏳  {label}")
    print(f"    python -m {module}")
    print("=" * 60)
    result = subprocess.run(
        [sys.executable, "-m", module],
        check=False,
        cwd=str(ROOT),
    )
    if result.returncode == 0:
        print(f"✅  Done: {module}")
    else:
        print(f"❌  Failed (exit {result.returncode}): {module}")
    return result.returncode


def main() -> int:
    print("\n" + "=" * 60)
    print("🚀  FEATURE ENGINEERING PIPELINE  (05.1)")
    print("=" * 60)

    failures = 0
    for module, label in STEPS:
        rc = run_step(module, label)
        if rc != 0:
            failures += 1
            print(f"\n⛔  Stopping — fix errors in {module} before continuing.")
            break   # dataset must succeed before NLP features can run

    print(f"\n{'='*60}")
    n = len(STEPS)
    passed = n - failures
    print(f"📊  {passed}/{n} steps passed  |  {failures} failed")
    print("=" * 60)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
