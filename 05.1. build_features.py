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
    (ROOT / "src" / "build_product_dataset.py", "Build product-level dataset"),
    (ROOT / "src" / "nlp_features.py",          "Extract NLP features"),
]


def run_step(script: Path, label: str) -> int:
    print(f"\n{'='*60}")
    print(f"⏳  {label}")
    print(f"    {script.relative_to(ROOT)}")
    print("=" * 60)
    result = subprocess.run(
        [sys.executable, str(script)],
        check=False,
        cwd=str(ROOT),
    )
    if result.returncode == 0:
        print(f"✅  Done: {script.name}")
    else:
        print(f"❌  Failed (exit {result.returncode}): {script.name}")
    return result.returncode


def main() -> int:
    print("\n" + "=" * 60)
    print("🚀  FEATURE ENGINEERING PIPELINE  (05.1)")
    print("=" * 60)

    missing = [s for s, _ in STEPS if not s.exists()]
    if missing:
        for p in missing:
            print(f"⚠️  Script not found: {p}")
        return 1

    failures = 0
    for script, label in STEPS:
        rc = run_step(script, label)
        if rc != 0:
            failures += 1
            print(f"\n⛔  Stopping — fix errors in {script.name} before continuing.")
            break   # dataset must succeed before NLP features can run

    print(f"\n{'='*60}")
    n = len(STEPS)
    passed = n - failures
    print(f"📊  {passed}/{n} steps passed  |  {failures} failed")
    print("=" * 60)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
