import pandas as pd
from dataclasses import dataclass, field
from typing import Callable
from pathlib import Path
from src.utils import PROJECT_ROOT, load_labels


@dataclass
class CategoryConfig:
    folder_name: str
    sub_map: dict           # {label_code: [keyword, ...]}
    priority_order: list    # ordered label codes to check
    fallback: str           # digit code, "Label N", or verbatim string
    parent_label_code: str  # "Label N" for parent_category column
    normalize_fn: Callable = None    # custom text normalizer; default: str.lower()
    pre_check_fn: Callable = None    # (name_normalized) -> str | None; short-circuit result
    exclusion_map: dict = field(default_factory=dict)  # {label_code: [words that cancel match]}
    junk_keywords: list = field(default_factory=list)  # if any match, row is marked junk
    junk_marker: str = "Bỏ qua (Lỗi Dữ Liệu)"


def _resolve_fallback(fallback: str, labels_dict: dict) -> str:
    if fallback.isdigit():
        return labels_dict.get(f"Label {fallback}", f"Label {fallback}")
    if fallback.startswith("Label "):
        return labels_dict.get(fallback, fallback)
    return fallback  # verbatim string (e.g. "Sữa tươi", "Củ, Quả")


def classify_product(name: str, config: CategoryConfig, labels_dict: dict) -> str:
    """Classify a product name into a subcategory using the category config."""
    norm = config.normalize_fn or (lambda x: str(x).lower())
    name_n = norm(str(name))

    # Junk check — mark and filter later (e.g. Confectionary)
    if config.junk_keywords and any(jk in name_n for jk in [norm(j) for j in config.junk_keywords]):
        return config.junk_marker

    # Optional pre-check for early overrides (e.g. Dairy's "sữa trái cây" rule)
    if config.pre_check_fn:
        result = config.pre_check_fn(name_n)
        if result is not None:
            return result

    # Priority-ordered keyword matching
    for code in config.priority_order:
        keywords = config.sub_map.get(code, [])
        if any(norm(k) in name_n for k in keywords):
            # Exclusion check (e.g. Dry_Food label 47 excludes "bơ")
            if any(ex in name_n for ex in config.exclusion_map.get(code, [])):
                continue
            return labels_dict.get(f"Label {code}", f"Label {code}")

    return _resolve_fallback(config.fallback, labels_dict)


def run_categorization(config: CategoryConfig) -> None:
    """
    Full categorization pipeline for one category.
    Reads CSV/ folder, deduplicates product names, classifies, writes cat_lookup_table.csv.
    """
    folder = PROJECT_ROOT / config.folder_name
    csv_folder = folder / "CSV"
    output_file = folder / "cat_lookup_table.csv"

    labels_dict = load_labels()

    csv_files = list(csv_folder.glob("*.csv"))
    if not csv_files:
        print(f"No CSV files found in {csv_folder}")
        return

    print(f"Reading {len(csv_files)} files for {config.folder_name}...")
    frames = []
    for f in csv_files:
        try:
            frames.append(pd.read_csv(f, encoding='utf-8-sig', usecols=['product_name']))
        except Exception as e:
            print(f"Skipping {f.name}: {e}")

    if not frames:
        print("No data loaded.")
        return

    master_df = pd.concat(frames, ignore_index=True)
    initial_count = len(master_df)
    master_df = master_df.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    print(f"Removed {initial_count - len(master_df)} duplicates.")

    master_df['subcategory'] = master_df['product_name'].apply(
        lambda x: classify_product(x, config, labels_dict)
    )

    # Drop junk rows
    if config.junk_keywords:
        before = len(master_df)
        master_df = master_df[master_df['subcategory'] != config.junk_marker].reset_index(drop=True)
        print(f"Removed {before - len(master_df)} junk rows.")

    master_df['parent_category'] = labels_dict.get(config.parent_label_code, config.parent_label_code)
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Saved {len(master_df)} products to {output_file.name}")
