import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.categorize_core import run_categorization
from config.category_maps import CATEGORY_REGISTRY

if __name__ == "__main__":
    run_categorization(CATEGORY_REGISTRY["Frozen"])
