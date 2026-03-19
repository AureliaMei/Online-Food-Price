"""
build_product_dataset.py — Aggregate daily CSVs into a product-level dataset.

For each unique product (product_name × unit), computes:
  - avg_final_price, avg_marked_price across all observation days
  - days_observed
  - promo_rate  (fraction of days where marked_price > final_price)
  - avg_discount_depth  (mean % discount on promoted days only)
  - price_volatility  (CV of daily final_price)
  - n_price_changes   (count of distinct final_price values)
  - max_daily_jump_pct  (largest day-over-day % change)
  - promo_streak_max  (longest consecutive promo days)
  - promo_streak_avg  (average consecutive promo streak length)
  - ever_promoted     (binary: was the product ever on promotion?)
  - always_promoted   (binary: promoted on every observed day?)
  - marked_price_changes  (count of distinct marked_price values)
  - marked_price_increased  (binary: did marked price ever go up?)
  - brand_name  (matched brand from BRAND_KEYWORDS, or empty)

Output: output/product_dataset.csv
"""

import unicodedata
import numpy as np
import pandas as pd
from pathlib import Path
from src.utils import PROJECT_ROOT, extract_date

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
            df['date'] = extract_date(f.name)
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


def _max_daily_jump(prices: pd.Series) -> float:
    """Largest absolute % change between consecutive observations."""
    if len(prices) < 2:
        return 0.0
    pct = prices.pct_change().abs()
    return pct.max() if not pct.empty else 0.0


def _streak_stats(promo_flags: pd.Series) -> tuple[int, float]:
    """Return (max_streak, avg_streak) of consecutive 1s in promo_flags."""
    streaks = []
    current = 0
    for v in promo_flags:
        if v == 1:
            current += 1
        else:
            if current > 0:
                streaks.append(current)
            current = 0
    if current > 0:
        streaks.append(current)
    if not streaks:
        return 0, 0.0
    return max(streaks), float(np.mean(streaks))


def aggregate_products(daily: pd.DataFrame) -> pd.DataFrame:
    """Compute per-product summary statistics from stacked daily data."""
    daily = daily.copy()

    # Sort by date for streak / jump calculations
    daily = daily.sort_values(['product_name', 'date']).reset_index(drop=True)

    # Promotion flag: marked_price is set (>0) and higher than final_price
    has_marked = daily['marked_price'] > 0
    is_promo = has_marked & (daily['marked_price'] > daily['final_price'])
    daily['is_promo'] = is_promo.astype(int)

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

    # --- Core aggregations ---
    agg = grp.agg(
        avg_final_price=('final_price', 'mean'),
        avg_marked_price=('marked_price_eff', 'mean'),
        days_observed=('final_price', 'count'),
        promo_rate=('is_promo', 'mean'),
        avg_discount_depth=('discount_depth', 'mean'),
        # B1: Price anomaly detection
        price_volatility=('final_price', lambda x: x.std() / x.mean() if x.mean() > 0 else 0.0),
        n_price_changes=('final_price', 'nunique'),
        max_daily_jump_pct=('final_price', _max_daily_jump),
        # B3: Promotion patterns
        ever_promoted=('is_promo', 'max'),
        always_promoted=('is_promo', 'min'),
        # B4: Marked price stability
        marked_price_changes=('marked_price_eff', 'nunique'),
    ).reset_index()

    # B3: Promotion streak stats
    streak_rows = []
    for keys, sub_df in grp:
        smax, savg = _streak_stats(sub_df['is_promo'].values)
        marked_inc = int((sub_df['marked_price_eff'].diff() > 0).any()) if len(sub_df) > 1 else 0
        streak_rows.append({
            'product_name': keys[0],
            'unit': keys[1],
            'subcategory': keys[2],
            'parent_category': keys[3],
            'promo_streak_max': smax,
            'promo_streak_avg': savg,
            'marked_price_increased': marked_inc,
        })
    streak_df = pd.DataFrame(streak_rows)
    agg = agg.merge(
        streak_df,
        on=['product_name', 'unit', 'subcategory', 'parent_category'],
        how='left',
    )

    return agg


# ---------------------------------------------------------------------------
# B2: Brand name extraction
# ---------------------------------------------------------------------------

# Import brand keywords from nlp_features (already NFC-normalized there)
from src.nlp_features import BRAND_KEYWORDS as _RAW_BRANDS
from src.brand_quadrants import (
    BRAND_CANONICAL, BRAND_QUADRANTS,
    is_premium as _is_premium, is_high_recognition as _is_high_recognition,
)

# Build a display-name version: use canonical mapping first, else title-case
_BRAND_DISPLAY = {}
for kw in _RAW_BRANDS:
    _BRAND_DISPLAY[kw] = BRAND_CANONICAL.get(kw, kw.strip().title())


def _extract_brand_name(product_name: str) -> str:
    """Return first matching brand keyword from product name, or empty string."""
    name_norm = unicodedata.normalize('NFC', str(product_name)).lower().strip()
    for kw in _RAW_BRANDS:
        if kw in name_norm:
            return _BRAND_DISPLAY[kw]
    return ''


def _build_brand_profiles(dataset: pd.DataFrame) -> pd.DataFrame:
    """Aggregate brand-level stats and save to output."""
    branded = dataset[dataset['brand_name'] != ''].copy()
    if branded.empty:
        return pd.DataFrame()

    profiles = branded.groupby('brand_name').agg(
        n_products=('product_name', 'count'),
        n_categories=('parent_category', 'nunique'),
        categories=('parent_category', lambda x: ', '.join(sorted(str(v) for v in x.unique() if pd.notna(v)))),
        avg_price=('avg_final_price', 'mean'),
        median_price=('avg_final_price', 'median'),
        price_p10=('avg_final_price', lambda x: x.quantile(0.1)),
        price_p90=('avg_final_price', lambda x: x.quantile(0.9)),
        avg_promo_rate=('promo_rate', 'mean'),
        avg_discount_depth=('avg_discount_depth', 'mean'),
        avg_price_volatility=('price_volatility', 'mean'),
    ).reset_index()

    profiles['price_range_p90_p10'] = profiles['price_p90'] - profiles['price_p10']
    # Add quadrant classification
    profiles['brand_quadrant'] = profiles['brand_name'].map(BRAND_QUADRANTS).fillna('')
    profiles = profiles.sort_values('n_products', ascending=False)
    return profiles


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

    # B2: Extract brand names
    dataset['brand_name'] = dataset['product_name'].map(_extract_brand_name)
    n_branded = (dataset['brand_name'] != '').sum()
    print(f"\nBrand extraction: {n_branded}/{len(dataset)} products matched a known brand")

    # B2b: Brand quadrant classification
    dataset['brand_quadrant'] = dataset['brand_name'].map(BRAND_QUADRANTS).fillna('')
    dataset['is_premium'] = dataset['brand_quadrant'].apply(
        lambda q: _is_premium(q) if q else 0
    )
    dataset['is_high_recognition'] = dataset['brand_quadrant'].apply(
        lambda q: _is_high_recognition(q) if q else 0
    )
    n_quadrant = (dataset['brand_quadrant'] != '').sum()
    n_missing = n_branded - n_quadrant
    if n_missing > 0:
        missing = dataset[
            (dataset['brand_name'] != '') & (dataset['brand_quadrant'] == '')
        ]['brand_name'].unique()
        print(f"  WARNING: {n_missing} branded products missing quadrant assignment: {list(missing)}")
    else:
        print(f"  Quadrant assignment: {n_quadrant}/{n_branded} branded products classified")

    out_path = PROJECT_ROOT / 'output' / 'product_dataset.csv'
    dataset.to_csv(out_path, index=False, encoding='utf-8-sig')
    print(f"Saved {len(dataset)} products → {out_path}")

    # B2: Brand profiles table
    profiles = _build_brand_profiles(dataset)
    if not profiles.empty:
        profiles_path = PROJECT_ROOT / 'output' / 'thesis_table_brand_profiles.csv'
        profiles.to_csv(profiles_path, index=False, encoding='utf-8-sig')
        print(f"Saved {len(profiles)} brand profiles → {profiles_path}")

    summary = (
        dataset.groupby('parent_category')
        [['avg_final_price', 'promo_rate', 'avg_discount_depth',
          'price_volatility', 'n_price_changes']]
        .mean()
        .round(3)
    )
    print("\nSummary by category:")
    print(summary.to_string())


if __name__ == '__main__':
    main()
