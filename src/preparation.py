"""
preparation.py — Gold-layer data preparation for hedonic regression and tree models.

Functions
---------
prepare_regression_sample(df)  → (reg_df, reg_df_clean)
prepare_tree_features(df)      → (X, feature_names, y, df_tree)
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer

# Columns required for the hedonic OLS model
_MODEL_COLS = [
    'ln_price_per_unit', 'is_branded', 'is_premium', 'is_high_recognition',
    'is_import', 'is_house_brand',
    'ln_pack_size', 'pack_count', 'has_health_claim', 'has_freshness_claim',
    'name_length', 'subcategory',
]

# Columns needed as base drop for the regression sample
_BASE_DROP_COLS = ['ln_price_per_unit', 'ln_marked_price_per_unit', 'ln_pack_size', 'subcategory']

# Categorical and numeric columns for the tree model
_CAT_COLS = ['parent_category', 'brand_quadrant']
_NUM_COLS = [
    'ln_pack_size', 'pack_count', 'is_import', 'has_health_claim',
    'has_freshness_claim', 'promo_rate', 'avg_discount_depth',
    'price_volatility', 'name_length', 'ever_promoted',
]


def prepare_regression_sample(
    df: pd.DataFrame,
    price_col: str = 'ln_price_per_unit',
    trim: tuple = (0.01, 0.99),
) -> tuple:
    """Return (reg_df, reg_df_clean) ready for smf.ols().

    reg_df       — winsorized sample (use for descriptive stats / broad plots)
    reg_df_clean — additionally drops NA on all model columns and coerces
                   subcategory to str (use for OLS .fit() calls)
    """
    # 1. Drop rows missing any base column or with non-finite price
    reg_df = df.dropna(subset=_BASE_DROP_COLS).copy()
    reg_df = reg_df[np.isfinite(reg_df[price_col])].copy()

    # 2. Winsorize price at trim quantiles
    lo, hi = reg_df[price_col].quantile(list(trim))
    reg_df = reg_df[(reg_df[price_col] >= lo) & (reg_df[price_col] <= hi)].copy()

    # 3. Clean sample for OLS: drop NA on all model columns, coerce subcategory
    reg_df_clean = reg_df.dropna(subset=_MODEL_COLS).copy()
    reg_df_clean['subcategory'] = reg_df_clean['subcategory'].astype(str)

    return reg_df, reg_df_clean


def prepare_tree_features(
    df: pd.DataFrame,
    max_kw_features: int = 60,
    min_kw_df: int = 10,
) -> tuple:
    """Return (X, feature_names, y, df_tree) for PercentileDecisionTree.

    X            — (n, p) float64 feature matrix
    feature_names — list of p feature name strings
    y            — (n,) float64 target (avg_final_price in VND)
    df_tree      — DataFrame subset used (index reset)
    """
    dt = df.copy()

    # 1. Fill missing categoricals and numerics
    dt['brand_quadrant'] = dt['brand_quadrant'].fillna('generic').replace('', 'generic')
    for col in _NUM_COLS:
        dt[col] = pd.to_numeric(dt[col], errors='coerce').fillna(0)

    # 2. Drop rows without a target
    dt = dt.dropna(subset=['avg_final_price']).reset_index(drop=True)

    # 3. One-hot encode categoricals
    ohe = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    X_cat = ohe.fit_transform(dt[_CAT_COLS])
    cat_names = ohe.get_feature_names_out(_CAT_COLS).tolist()

    # 4. Numeric features
    X_num = dt[_NUM_COLS].values
    num_names = list(_NUM_COLS)

    # 5. Keyword features from product name (Vietnamese: space-separated)
    cv = CountVectorizer(
        analyzer='word',
        ngram_range=(1, 2),
        max_features=max_kw_features,
        min_df=min_kw_df,
        binary=True,
        token_pattern=r'[^\s]+',
    )
    X_kw = cv.fit_transform(dt['product_name'].astype(str)).toarray()
    kw_names = ['kw:' + n for n in cv.get_feature_names_out()]

    # 6. Stack all feature blocks
    X = np.hstack([X_cat, X_num, X_kw]).astype(np.float64)
    feature_names = cat_names + num_names + kw_names
    y = dt['avg_final_price'].values.astype(np.float64)

    return X, feature_names, y, dt
