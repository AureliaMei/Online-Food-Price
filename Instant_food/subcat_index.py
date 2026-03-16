import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.index_core import run_jevons_index

if __name__ == "__main__":
    run_jevons_index(
        "Instant_food",
        dedup_lookup=True,
        handle_new_subcats=True,
        sort_output_columns=True,
    )
