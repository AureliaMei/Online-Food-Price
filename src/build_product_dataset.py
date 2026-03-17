"""
build_product_dataset.py — Aggregate daily CSVs into a product-level dataset.

For each unique product (product_name × unit), computes:
  - avg_final_price, avg_marked_price across all observation days
  - days_observed
  - promo_rate  (fraction of days where marked_price > final_price)
  - avg_discount_depth  (mean % discount on promoted days only)

Output: output/product_dataset.csv
"""

import pandas as pd
from pathlib import Path
from src.utils import PROJECT_ROOT

CATEGORIES = [
    "Dairy", "Baby_product", "Veg_Fruit", "Confectionary",
    "Dry_Food", "Egg_and_soy", "Frozen", "Instant_food",
    "Processed_food", "Spice",
]

# Only the columns we need — handles Spice which has extra columns (deal, gift_price)
NEEDED_COLS = {'product_name', 'unit', 'final_price', 'marked_price'}


def load_category(folder_name: str) -> pd.DataFrame:
    """Stack all daily CSVs for one category and attach subcategory labels."""
    folder = PROJECT_ROOT / 'data' / folder_name
    csv_folder = folder / 'CSV'
    lookup_file = folder / 'cat_lookup_table.csv'

    files = sorted(csv_folder.glob('*.csv'))
    if not files:
        print(f"  No CSV files in {csv_folder}")
        return pd.DataFrame()

    frames = []
    for f in files:
        try:
            df = pd.read_csv(f, usecols=lambda c: c in NEEDED_COLS)
            frames.append(df)
        except Exception as e:
            print(f"  Warning skipping {f.name}: {e}")

    if not frames:
        return pd.DataFrame()

    daily = pd.concat(frames, ignore_index=True)
    daily['final_price'] = pd.to_numeric(daily['final_price'], errors='coerce')
    daily['marked_price'] = pd.to_numeric(daily['marked_price'], errors='coerce')
    # Drop rows where final_price is missing or zero
    daily = daily[daily['final_price'] > 0].copy()

    # Attach subcategory labels
    if lookup_file.exists():
        lookup = pd.read_csv(
            lookup_file,
            usecols=['product_name', 'subcategory', 'parent_category'],
        )
        # Some categories (e.g. Processed_food) have duplicate product_name rows
        lookup = lookup.drop_duplicates(subset=['product_name'], keep='last')
        daily = daily.merge(lookup, on='product_name', how='left')
    else:
        # Spice: no lookup table — single category
        daily['subcategory'] = 'Gia Vị'
        daily['parent_category'] = 'Gia Vị'

    return daily


def aggregate_products(daily: pd.DataFrame) -> pd.DataFrame:
    """Compute per-product summary statistics from stacked daily data."""
    daily = daily.copy()

    # Promotion flag: marked_price is set (>0) and higher than final_price
    has_marked = daily['marked_price'] > 0
    is_promo = has_marked & (daily['marked_price'] > daily['final_price'])
    daily['is_promo'] = is_promo.astype(float)

    # Discount depth only for promoted rows
    daily['discount_depth'] = float('nan')
    daily.loc[is_promo, 'discount_depth'] = (
        (daily.loc[is_promo, 'marked_price'] - daily.loc[is_promo, 'final_price'])
        / daily.loc[is_promo, 'marked_price']
    )

    # On non-promo days the checkout price IS the sticker price.
    # Fill missing/zero marked_price with final_price so avg_marked_price
    # is always ≥ avg_final_price and covers all observed days.
    daily['marked_price_eff'] = daily['marked_price'].where(
        daily['marked_price'] > 0, daily['final_price']
    )

    grp = daily.groupby(
        ['product_name', 'unit', 'subcategory', 'parent_category'],
        dropna=False,
    )
    agg = grp.agg(
        avg_final_price=('final_price', 'mean'),
        avg_marked_price=('marked_price_eff', 'mean'),
        days_observed=('final_price', 'count'),
        promo_rate=('is_promo', 'mean'),
        avg_discount_depth=('discount_depth', 'mean'),
    ).reset_index()

    return agg


def main() -> None:
    all_frames = []
    for cat in CATEGORIES:
        print(f"Loading {cat}...")
        daily = load_category(cat)
        if daily.empty:
            print(f"  Skipped (no data)")
            continue
        agg = aggregate_products(daily)
        all_frames.append(agg)
        print(f"  {len(agg)} products, promo_rate={agg['promo_rate'].mean():.3f}")

    if not all_frames:
        print("No data found.")
        return

    dataset = pd.concat(all_frames, ignore_index=True)

    out_path = PROJECT_ROOT / 'output' / 'product_dataset.csv'
    dataset.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"\nSaved {len(dataset)} products → {out_path}")

    summary = (
        dataset.groupby('parent_category')
        [['avg_final_price', 'promo_rate', 'avg_discount_depth']]
        .mean()
        .round(3)
    )
    print("\nSummary by category:")
    print(summary.to_string())


if __name__ == '__main__':
    main()
