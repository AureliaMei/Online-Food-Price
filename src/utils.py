import re
import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def extract_date(filename: str) -> str:
    """Extract YYYY-MM-DD from a filename. Returns filename unchanged if not found."""
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    return match.group(0) if match else filename


def clean_price(val) -> float:
    """Strip non-digit characters and return float. Returns 0.0 for empty/null values."""
    if not val or pd.isna(val) or val == "":
        return 0.0
    digits = re.sub(r'[^\d]', '', str(val))
    return float(digits) if digits else 0.0


def load_labels(json_path: Path = None) -> dict:
    """Load label definitions from Category list.json. Returns empty dict on failure."""
    if json_path is None:
        json_path = PROJECT_ROOT / 'Category list.json'
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data[0] if isinstance(data, list) and data else {}
    except Exception as e:
        print(f"Warning: Could not load labels from {json_path}: {e}")
        return {}
