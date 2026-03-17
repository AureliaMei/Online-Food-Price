"""
nlp_features.py — Extract structured features from Vietnamese product names.

Designed for hedonic pricing analysis: given a product_dataset.csv with
product_name and unit columns, extract brand, origin, health, size, and
packaging features for use as regressors.

Main entry point:
    extract_features(df) → df with new feature columns added in-place
"""

import re
import unicodedata
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Text normalization (mirrors config/category_maps.py convention)
# ---------------------------------------------------------------------------

def _norm(text: str) -> str:
    """NFC normalize + lowercase + strip."""
    return unicodedata.normalize('NFC', str(text)).lower().strip()


def _padded(text: str) -> str:
    """Padded version for word-boundary matching."""
    return ' ' + _norm(text) + ' '


# ---------------------------------------------------------------------------
# Brand list (~40 known brands on Winmart)
# ---------------------------------------------------------------------------

BRAND_KEYWORDS = [
    # Dairy / beverages
    'th true milk', 'th truemilk', 'vinamilk', 'milo', 'ovaltine',
    'nutimilk', 'meadow fresh', 'devondale', 'anchor', 'zott', 'hoff',
    'yakult', 'betagen', 'probi', 'yomost', 'fami', 'ba vì', 'ba vi',
    'celano', 'degrees', 'sahmyook', 'nutifood', 'kun ', 'susu ',
    # Baby / formula
    'similac', 'ensure', 'pediasure', 'glucerna', 'nan ', 'optimum',
    'colosbaby', 'famna', 'nuvi ', 'grow ',
    # Instant food
    'hảo hảo', 'hao hao', 'omachi', 'kokomi', 'vifon', 'acecook',
    'indomie', 'koreno', 'meizan',
    # Confectionary / snack
    'pringles', "lay's", 'oreo', 'danisa', 'cosy ', 'chocopie',
    'kellogg', 'calbee', 'nestlé', 'nestle',
    # Spice / condiment
    'chinsu', 'knorr', 'maggi', 'masan', 'nam dương', 'nam duong',
    # General
    'abbott', 'unilever',
]

# House brand: exact substring match
HOUSE_BRAND_KEYWORDS = ['wineco', 'win eco']

# ---------------------------------------------------------------------------
# Import / origin keywords
# Single-word country names are padded with spaces to require word boundaries.
# Multi-word / brand keywords use plain substring matching.
# ---------------------------------------------------------------------------

IMPORT_ORIGINS = {
    'Mỹ':        [' mỹ ', 'usa', 'american'],
    'Úc':        [' úc ', 'australia', 'australian', 'meadow fresh', 'devondale', 'anchor'],
    'Nhật':      [' nhật ', 'japan', 'japanese'],
    'Pháp':      [' pháp ', 'france', 'french'],
    'Thái':      [' thái ', 'thailand', 'thai'],
    'Hàn':       [' hàn ', 'korea', 'korean'],
    'Đức':       [' đức ', 'germany', 'german'],
    'Ý':         [' ý ', 'italy', 'italian'],
    'Nhập khẩu': ['nhập khẩu', 'imported'],
}

# Known Vietnamese domestic brands. If a product name contains any of these,
# country words in the name are flavor/variety descriptors — not import claims.
DOMESTIC_BRAND_NAMES = {
    'chinsu', 'chin su', 'masan', 'nam dương', 'nam duong',
    'hảo hảo', 'hao hao', 'omachi', 'kokomi', 'vifon',
    'acecook', 'koreno', 'nutifood', 'ba vì', 'ba vi',
    'yomost', 'fami', 'meizan',
    'đức việt',   # Vietnamese sausage brand (uses "Đức"/"Mỹ" as style names)
}

# Compound Vietnamese words/phrases that contain a country keyword as a
# substring but have a different meaning. If any of these appear in the name,
# skip the corresponding country classification.
IMPORT_FP_PHRASES: dict[str, list[str]] = {
    'Mỹ':  ['mỹ nhân', 'mỹ phẩm', 'mỹ vị'],          # beautiful/graceful
    'Nhật': ['giống nhật', 'kiểu nhật'],               # Japanese-variety crops grown locally
    'Hàn':  ['giống hàn', 'kiểu hàn'],
    'Đức':  ['giống đức', 'kiểu đức'],
}

# ---------------------------------------------------------------------------
# Health / freshness claim keywords
# ---------------------------------------------------------------------------

HEALTH_KEYWORDS = [
    'canxi', 'calcium', 'probiotic', 'dha', 'organic', 'ít đường',
    'ít béo', 'tách béo', 'không đường', 'dinh dưỡng', 'tăng cường',
    'vitamin', 'omega', 'collagen', 'fiber', 'chất xơ', 'ít calo',
    'low fat', 'sugar free', 'ăn kiêng',
]

FRESHNESS_KEYWORDS = [
    'tươi', 'sạch', 'nguyên chất', 'tự nhiên', 'nguyên kem',
    'thuần khiết', 'không chất bảo quản', 'hữu cơ',
]

# ---------------------------------------------------------------------------
# NFC-normalize all keyword lists at module load to prevent Unicode-form
# mismatches between source-file literals and NFC-normalized product names.
# ---------------------------------------------------------------------------

def _nkw(kw: str) -> str:
    return unicodedata.normalize('NFC', kw)

BRAND_KEYWORDS       = [_nkw(k) for k in BRAND_KEYWORDS]
HOUSE_BRAND_KEYWORDS = [_nkw(k) for k in HOUSE_BRAND_KEYWORDS]
DOMESTIC_BRAND_NAMES = {_nkw(k) for k in DOMESTIC_BRAND_NAMES}
HEALTH_KEYWORDS      = [_nkw(k) for k in HEALTH_KEYWORDS]
FRESHNESS_KEYWORDS   = [_nkw(k) for k in FRESHNESS_KEYWORDS]
IMPORT_ORIGINS       = {c: [_nkw(k) for k in kws] for c, kws in IMPORT_ORIGINS.items()}
IMPORT_FP_PHRASES    = {c: [_nkw(p) for p in ps]  for c, ps  in IMPORT_FP_PHRASES.items()}

# ---------------------------------------------------------------------------
# Size extraction from product_name
# ---------------------------------------------------------------------------

# Pattern: number (optionally decimal) followed by a volume/weight unit
# Handles: 200ml, 1L, 1.5l, 500g, 1kg, 250gr, 200ML
_SIZE_RE = re.compile(
    r'(\d+(?:[.,]\d+)?)\s*(ml|lít\b|lit\b|l\b|g\b|kg\b|gr\b)',
    re.IGNORECASE,
)

# Unit conversion to canonical base (ml or g)
_VOL_UNITS  = {'ml', 'l'}
_WGHT_UNITS = {'g', 'kg', 'gr'}

def _to_base(value: float, unit: str) -> tuple[float, str]:
    """Convert to ml or g. Returns (base_value, 'ml'|'g')."""
    u = unit.lower()
    if u in ('l', 'lít', 'lit'):
        return value * 1000, 'ml'
    if u == 'kg':
        return value * 1000, 'g'
    if u in ('g', 'gr'):
        return value, 'g'
    return value, 'ml'  # ml


def _extract_size(name: str) -> tuple[float | None, str | None]:
    """
    Extract the primary size from a product name.

    Strategy: find all size mentions, prefer the one that appears LAST
    (individual container size tends to be at the end, e.g. '6 hộp x 200ml').
    Returns (size_in_base_unit, unit_type) where unit_type is 'ml' or 'g'.
    """
    matches = _SIZE_RE.findall(name)
    if not matches:
        return None, None
    # Take the last match
    val_str, unit = matches[-1]
    val = float(val_str.replace(',', '.'))
    base_val, base_unit = _to_base(val, unit)
    return base_val, base_unit


# ---------------------------------------------------------------------------
# Pack count extraction
# ---------------------------------------------------------------------------

# Try unit field first: "Gói 6", "Lốc 4", "Thùng 48"
_UNIT_PACK_RE = re.compile(r'(?:gói|lốc|hộp|túi|set|combo|thùng)\s*(\d+)', re.IGNORECASE)

# "10g*10gói" — size_unit * count (count must be followed by a container word)
# "78g x15C", "20g*130" are excluded because count is not followed by a container word.
_MULTIPLY_RE = re.compile(
    r'\d+(?:[.,]\d+)?\s*(?:ml|lít\b|lit\b|l\b|g\b|kg\b|gr\b)\s*[*×x]\s*(\d+)'
    r'(?=\s*(?:gói|hộp|chai|túi|lon|lọ|cái|viên|miếng|thùng|lốc)\b)',
    re.IGNORECASE,
)

# product_name count patterns: "Thùng 48", "6 hộp x", "10 viên x"
# Note: "lốc N" is handled with higher priority in step 0 of _extract_pack_count
_NAME_COUNT_RE = re.compile(
    r'(?:combo|set|thùng)\s*(\d+)'
    r'|(\d+)\s*(?:hộp|chai|gói|túi|cái|lon|viên)\s*x',
    re.IGNORECASE,
)


def _extract_pack_count(name: str, unit_field: str) -> int:
    """Extract number of individual units in one package. Returns 1 if unclear."""
    name_norm = _norm(name)

    # 0. "Lốc N" in product name — highest priority: explicit consumer pack label
    m = re.search(r'lốc\s*(\d+)', name_norm, re.IGNORECASE)
    if m:
        return int(m.group(1))

    # 1. Multiplication pattern: "10g*10gói" → count=10 (count must precede container word)
    m = _MULTIPLY_RE.search(name_norm)
    if m:
        return int(m.group(1))

    # 2. Unit field: "Gói 6", "Thùng 48"
    m = _UNIT_PACK_RE.search(_norm(unit_field))
    if m:
        return int(m.group(1))

    # 3. Product_name: "Thùng 48 gói...", "6 hộp x", "10 viên x"
    m = _NAME_COUNT_RE.search(name_norm)
    if m:
        val = m.group(1) or m.group(2)
        if val:
            return int(val)

    return 1


# ---------------------------------------------------------------------------
# Unit type classification (from unit field)
# ---------------------------------------------------------------------------

_WEIGHT_UNITS = {'g', 'kg', 'gr', 'gram'}
_VOLUME_UNITS = {'ml', 'l', 'lít', 'lit'}
_COUNT_UNITS  = {'cái', 'hộp', 'quả', 'trái', 'miếng', 'viên', 'lọ', 'lon', 'chai', 'túi', 'gói'}

def _classify_unit_type(unit_field: str) -> str:
    """Classify the unit field into weight / volume / count / bundle / unknown."""
    u = _norm(unit_field).strip()
    # Check if unit field itself is a weight/volume value (e.g. "500g", "1L")
    m = _SIZE_RE.match(u)
    if m:
        base_unit = m.group(2).lower()
        if base_unit in _VOL_UNITS:
            return 'volume'
        if base_unit in _WGHT_UNITS:
            return 'weight'

    # Remove digits (pack count like "Gói 6" → "Gói")
    base = re.sub(r'\d+', '', u).strip()
    tokens = set(base.split())

    if tokens & _WEIGHT_UNITS:
        return 'weight'
    if tokens & _VOLUME_UNITS:
        return 'volume'
    if tokens & {'lốc', 'combo', 'set', 'bộ', 'vỉ'}:
        return 'bundle'
    if tokens & _COUNT_UNITS:
        return 'count'
    return 'unknown'


# ---------------------------------------------------------------------------
# Main feature extraction
# ---------------------------------------------------------------------------

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add NLP-derived feature columns to df (in-place copy).

    Required input columns: product_name, unit
    Returns df with new columns added.
    """
    df = df.copy()

    names  = df['product_name'].fillna('').astype(str)
    units  = df['unit'].fillna('').astype(str)

    names_norm = names.map(_norm)
    names_pad  = names.map(_padded)

    # ------------------------------------------------------------------
    # is_branded: any known brand keyword found in product_name
    # ------------------------------------------------------------------
    def _check_brands(name_norm: str) -> int:
        for kw in BRAND_KEYWORDS:
            if kw in name_norm:
                return 1
        return 0

    df['is_branded'] = names_norm.map(_check_brands)

    # ------------------------------------------------------------------
    # is_house_brand: WinEco / Win Eco
    # ------------------------------------------------------------------
    def _check_house(name_norm: str) -> int:
        for kw in HOUSE_BRAND_KEYWORDS:
            if kw in name_norm:
                return 1
        return 0

    df['is_house_brand'] = names_norm.map(_check_house)

    # ------------------------------------------------------------------
    # import_origin: categorical (first matching country, or 'domestic')
    # is_import: binary
    # Uses padded name for word-boundary matching of single-word country names.
    # Domestic brand override: if a known domestic brand is present, country
    # words are flavor/variety descriptors, not import claims.
    # ------------------------------------------------------------------
    def _get_origin(args: tuple) -> str:
        name_pad, name_norm = args
        for brand in DOMESTIC_BRAND_NAMES:
            if brand in name_norm:
                return 'domestic'
        for country, kws in IMPORT_ORIGINS.items():
            fp_phrases = IMPORT_FP_PHRASES.get(country, [])
            for kw in kws:
                if kw in name_pad:
                    if any(fp in name_norm for fp in fp_phrases):
                        continue  # false positive phrase present — skip this match
                    return country
        return 'domestic'

    df['import_origin'] = list(map(_get_origin, zip(names_pad, names_norm)))
    df['is_import'] = (df['import_origin'] != 'domestic').astype(int)

    # ------------------------------------------------------------------
    # has_health_claim
    # ------------------------------------------------------------------
    def _has_health(name_norm: str) -> int:
        for kw in HEALTH_KEYWORDS:
            if kw in name_norm:
                return 1
        return 0

    df['has_health_claim'] = names_norm.map(_has_health)

    # ------------------------------------------------------------------
    # has_freshness_claim
    # ------------------------------------------------------------------
    def _has_fresh(name_norm: str) -> int:
        for kw in FRESHNESS_KEYWORDS:
            if kw in name_norm:
                return 1
        return 0

    df['has_freshness_claim'] = names_norm.map(_has_fresh)

    # ------------------------------------------------------------------
    # name_length: token count
    # ------------------------------------------------------------------
    df['name_length'] = names_norm.map(lambda n: len(n.split()))

    # ------------------------------------------------------------------
    # unit_type
    # ------------------------------------------------------------------
    df['unit_type'] = units.map(_classify_unit_type)

    # ------------------------------------------------------------------
    # pack_count
    # ------------------------------------------------------------------
    df['pack_count'] = [
        _extract_pack_count(n, u)
        for n, u in zip(names.tolist(), units.tolist())
    ]

    # ------------------------------------------------------------------
    # uncertain_pack_count: True when unit="Thùng" (no number) and
    # no pack count was found in the product name.
    # These rows have unknown carton quantities → exclude from regressions.
    # ------------------------------------------------------------------
    df['uncertain_pack_count'] = (
        units.map(_norm).str.strip().eq('thùng') &
        (df['pack_count'] == 1) &
        ~names_norm.str.contains(r'thùng\s*\d+', case=False, na=False)
    )

    # ------------------------------------------------------------------
    # size_ml, size_g: individual container size
    # ------------------------------------------------------------------
    sizes = names.map(_extract_size)
    df['_size_val']  = sizes.map(lambda x: x[0])
    df['_size_unit'] = sizes.map(lambda x: x[1])

    df['size_ml'] = np.where(df['_size_unit'] == 'ml', df['_size_val'], np.nan)
    df['size_g']  = np.where(df['_size_unit'] == 'g',  df['_size_val'], np.nan)
    df.drop(columns=['_size_val', '_size_unit'], inplace=True)

    # ------------------------------------------------------------------
    # ln_pack_size: log of individual container size (ml or g, unified)
    # ------------------------------------------------------------------
    # Combine into one size column (prefer ml for beverages, g for solids)
    combined_size = df['size_ml'].fillna(df['size_g'])
    df['ln_pack_size'] = np.log(combined_size.replace(0, np.nan))

    # ------------------------------------------------------------------
    # Price per unit (for regression DV) — requires avg_final_price column
    # ------------------------------------------------------------------
    if 'avg_final_price' in df.columns:
        # Total content = individual_size × pack_count
        total_size = combined_size * df['pack_count']
        df['price_per_100ml'] = np.where(
            df['size_ml'].notna(),
            df['avg_final_price'] / (df['size_ml'] * df['pack_count'] / 100),
            np.nan,
        )
        df['price_per_100g'] = np.where(
            df['size_g'].notna(),
            df['avg_final_price'] / (df['size_g'] * df['pack_count'] / 100),
            np.nan,
        )
        # Unified per-unit price: use whichever is available
        unified = df['price_per_100ml'].fillna(df['price_per_100g'])
        df['ln_price_per_unit'] = np.log(unified.replace(0, np.nan))

        # Same for marked price
        if 'avg_marked_price' in df.columns:
            df['marked_price_per_100ml'] = np.where(
                df['size_ml'].notna(),
                df['avg_marked_price'] / (df['size_ml'] * df['pack_count'] / 100),
                np.nan,
            )
            df['marked_price_per_100g'] = np.where(
                df['size_g'].notna(),
                df['avg_marked_price'] / (df['size_g'] * df['pack_count'] / 100),
                np.nan,
            )
            unified_marked = df['marked_price_per_100ml'].fillna(df['marked_price_per_100g'])
            df['ln_marked_price_per_unit'] = np.log(unified_marked.replace(0, np.nan))

    return df


# ---------------------------------------------------------------------------
# CLI: run on output/product_dataset.csv and save output/product_features.csv
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    from src.utils import PROJECT_ROOT

    in_path = PROJECT_ROOT / 'output' / 'product_dataset.csv'
    out_path = PROJECT_ROOT / 'output' / 'product_features.csv'

    if not in_path.exists():
        print(f"Input not found: {in_path}")
        print("Run src/build_product_dataset.py first.")
    else:
        df = pd.read_csv(in_path)
        print(f"Loaded {len(df)} products.")
        df_feat = extract_features(df)
        df_feat.to_csv(out_path, index=False, encoding='utf-8-sig')
        print(f"Saved {len(df_feat)} rows → {out_path}")

        # Quick sanity checks
        print(f"\nFeature coverage:")
        feat_cols = [
            'is_branded', 'is_import', 'is_house_brand',
            'has_health_claim', 'has_freshness_claim',
            'ln_pack_size', 'ln_price_per_unit',
        ]
        for col in feat_cols:
            if col in df_feat.columns:
                non_null = df_feat[col].notna().sum()
                if df_feat[col].dtype == float:
                    mean_val = df_feat[col].mean()
                    print(f"  {col}: {non_null}/{len(df_feat)} non-null, mean={mean_val:.3f}")
                else:
                    rate = df_feat[col].mean()
                    print(f"  {col}: rate={rate:.3f}")
