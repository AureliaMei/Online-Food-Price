# Thesis: What Makes Vietnamese Groceries Expensive? Decomposing Food Price Premiums via Hedonic Pricing

## Context

The dataset contains 1,000+ unique products across 10 food categories scraped daily from Winmart over ~88 days. Product names are information-dense Vietnamese text containing brand names, pack sizes, origin signals, health claims, and quality modifiers. The core question: within any food category, some products cost far more than others. How much of that price gap is explained by what the product is (brand, origin, health claims, size) vs. being unexplained? This is a hedonic pricing decomposition of food price premiums in a Vietnamese online grocery context.

## Research Questions

**Primary:** What product characteristics (brand, import origin, health claims, pack size) generate price premiums within Vietnamese online food categories?

**Secondary:** Do the same attributes that generate sticker price premiums (marked_price) also generate premiums in what consumers actually pay (final_price)? Or do promotions erode premiums at checkout?

## Methodology

### Time Treatment: Cross-Sectional
Average final_price and marked_price per product across all available days. No time series required.

### Step 1 — Build Product-Level Dataset
Source files:

- `data/[CATEGORY]/cat_lookup_table.csv` — unique product list (~1,000+ products across 10 categories)
- `data/[CATEGORY]/CSV/*.csv` — daily prices to average per product

Output table — one row per product:

```
product_name, subcategory, category, avg_final_price, avg_marked_price,
days_observed, promo_rate, avg_discount_depth
```

### Step 2 — NLP Feature Extraction Pipeline
Features extracted from product_name and unit columns using regex + keyword dictionaries.

| Feature | Method | Captures |
|---|---|---|
| is_branded | Known brand list (~30 brands) | Brand premium |
| brand_origin | Origin keywords (Mỹ, Úc, Nhật, nhập khẩu…) | Import premium |
| is_house_brand | Exact match (WinEco) | Retailer private label discount |
| ln_pack_size | Regex on unit + name (ml/g/kg/L) | Returns to scale |
| pack_count | Regex on "Lốc X", "Gói X" | Bulk bundling premium |
| has_health_claim | Keyword list (canxi, probiotic, DHA, organic, ít đường) | Health premium |
| has_freshness_claim | Keyword list (tươi, sạch, nguyên chất) | Freshness premium |
| name_length | Token count | Information richness proxy |
| unit_type | weight / volume / count / bundle | Comparability control |

### Step 3 — Hedonic Regression
Dependent variable: ln(price_per_standardized_unit) — price per 100g/100ml after pack size normalization

Specification:

```
ln(P/unit) = α + β₁·is_branded + β₂·is_import + β₃·is_house_brand
           + β₄·ln(pack_size) + β₅·pack_count
           + β₆·has_health_claim + β₇·has_freshness_claim
           + β₈·name_length + γ·subcategory_FE + ε
```

The β coefficients are the implicit prices (premiums) for each attribute.

Run twice:
- DV = ln(marked_price/unit) — sticker price premiums
- DV = ln(final_price/unit) — actual paid price premiums

If β₁ (brand premium) shrinks in specification 2, promotions are partially equalizing consumer prices.

Cross-category analysis:
- Run specification per category group (or with attribute × category interactions)
- Compare premium magnitude: Dairy vs. Veg_Fruit vs. Dry_Food vs. Processed_food
- Expected gradient: import/brand premiums largest in Dairy, near-zero in Veg_Fruit

### Step 4 — Decomposition Summary
For each subcategory, report:
- Total price variation (std dev of ln price)
- Explained by: brand, origin, health claims, pack size (from R²)
- Unexplained (residual) — potential market power signal

## Theoretical Framework

- **Hedonic pricing** (Rosen 1974): goods are bundles of attributes; market prices reveal implicit values for each attribute
- **Brand equity** (Keller 1993): brand identity creates a sustainable price premium above physical product characteristics
- **Price discrimination via versioning** (Varian 1997): same core product in premium/economy variants
- **Promotional pricing paradox:** categories with highest promotion penetration (Dairy 92.7%) also have highest branded price premiums — are promotions the mechanism that keeps premium products competitive?

## Expected Findings

| Attribute | Expected Premium | Strongest in |
|---|---|---|
| Branded vs. generic | +20–40% | Dairy, Processed_food |
| Imported vs. domestic | +15–30% | Dairy |
| House brand (WinEco) | −5–15% | Veg_Fruit |
| Health claim | +10–20% | Dairy, Baby_product |
| Freshness claim | +5–15% | Veg_Fruit, Frozen |
| Larger pack size | −X% per unit | Packaged goods |

Brand premium in marked_price > brand premium in final_price → promotions partially close the gap.

## Thesis Structure

1. Introduction — food inflation in Vietnam; how much of grocery spending is a "premium tax"?
2. Literature Review — hedonic pricing, brand equity, online retail pricing, Vietnamese consumer market
3. Data & Methods — scraping pipeline, NLP feature engineering, regression specification
4. Results
   - Descriptive: price distributions by brand/origin/health claim tier
   - Main regression table (pooled and by category)
   - Marked price vs. final price premium comparison
   - Robustness checks
5. Discussion — consumer welfare, retailer strategy, implications for food affordability
6. Conclusion

## Critical Files

| File | Role |
|---|---|
| `data/[CATEGORY]/cat_lookup_table.csv` | Master product list (10 files) |
| `data/[CATEGORY]/CSV/*.csv` | Daily prices to average |
| `output/subcategory_kmeans_groups.csv` | Validate subcategory clusters |
| `.claude/thesis_brainstorm.md` | UPDATE this file to reflect new thesis direction |

## Rigor Levers

- Cluster-robust SE by subcategory
- VIF check for NLP feature multicollinearity
- Partial F-tests: brand block, health claim block
- Robustness: re-run on 3 separate date snapshots (not just average)
- Sensitivity: narrow brand list (top 15) vs. broad (all capitalized tokens)
- Adjusted R² decomposition per category

## Implementation Steps (post plan approval)

1. Update thesis_brainstorm.md — rewrite to reflect hedonic pricing / food price premium framing
2. Write `src/build_product_dataset.py` — aggregate daily CSVs → product-level dataset
3. Write `src/nlp_features.py` — NLP extraction pipeline
4. Write `notebooks/08. hedonic_regression.ipynb` — regressions + tables
5. Write `notebooks/09. visualize_hedonic.ipynb` — charts for thesis

## Verification

- Branded products should have higher mean prices than generic in each category (sanity check)
- β₁ positive and significant in Dairy, near-zero in Veg_Fruit
- R² higher for brand-heavy categories (Dairy) than commodity categories (Veg_Fruit)
- Coefficients stable across 3 different date snapshots

---

## Part D: Brand Price Gap Dynamics Over Time

### Research Questions

1. Is the branded-generic price gap (in VND and %) stable across the 88-day window, or does it widen/compress over time?
2. Does the gap behave differently across categories (Dairy vs. Veg_Fruit vs. Processed_food)?
3. Is there a visible Tet effect (around Feb 17, 2026) — do brands discount more during the holiday, narrowing the gap?

### Methodology

**Unit of analysis:** date × category (daily panel)

**Gap metric:**
- `gap_abs` = median(branded final_price) − median(generic final_price) in VND
- `gap_pct` = gap_abs / median(generic final_price) × 100
- Computed separately for `final_price` and `marked_price`
- Using median (not mean) for robustness to outlier price jumps

**Brand detection:** same `BRAND_KEYWORDS` substring match as hedonic regression (`is_branded = 1` if any keyword in product name)

**Tet window:** Feb 10 – Feb 24, 2026 (±1 week around Feb 17)

### Expected Findings

| Category | Expected dynamic |
|---|---|
| Dairy | Persistent branded premium; slight narrowing at Tet (high promo_rate = 92.7%) |
| Veg_Fruit | No meaningful gap (few/no branded products) |
| Processed_food | Moderate gap; possible Tet widening (branded gift sets?) |
| Instant_food | Moderate gap; stable (commodity pricing) |
| Confectionary | Largest Tet effect — branded snacks as gift items |

### Output

- `notebooks/10. brand_price_dynamics.ipynb` — 4-panel visualization
- `output/brand_gap_daily.csv` — daily × category timeseries
- `output/brand_gap_summary.csv` — per-category summary with Tet vs. non-Tet comparison

### Connection to Main Thesis

This is a **temporal robustness check** for the cross-sectional hedonic findings:
- If branded premium is stable over time → cross-sectional average is representative
- If branded premium shrinks during Tet → promotional pricing partially equalizes consumer prices (supports the "promotions erode premiums" finding from Fig 3)
- Connects to the Discussion section: consumer welfare implications of promotional pricing

### Thesis Placement

Section 4 (Results) → 4.4 Temporal Dynamics of Brand Premiums
- Short section (~1 page): reference Figure D1 (gap over time) + Table D1 (summary stats)
- Bridge to Discussion: are the premiums found in hedonic regression permanent features or partially eroded by seasonal promotions?

---

## Part E: Decision Tree Price Predictor

### Motivation

The OLS hedonic regression captures *marginal effects* of individual attributes holding others fixed. A decision tree complements this by:
1. Capturing **interaction effects** (e.g., "imported dairy costs X, but imported confectionery costs Y")
2. Giving **intuitive price ranges** ("if a product is Prestige Leader dairy with a health claim, expect 45,000–120,000 VND")
3. Being fully interpretable as explicit if-then rules — no log-transformation interpretation needed

### Model

**Target:** `avg_final_price` (VND checkout price — direct, intuitive)
**Algorithm:** `DecisionTreeRegressor(max_depth=5, min_samples_leaf=15)`
**Evaluation:** 5-fold CV R², MAE, median absolute error

### Features

**Structured (12):** `parent_category` (one-hot), `brand_quadrant` (one-hot), `ln_pack_size`, `pack_count`, `is_import`, `has_health_claim`, `has_freshness_claim`, `promo_rate`, `avg_discount_depth`, `price_volatility`, `name_length`, `ever_promoted`

**Name keywords (up to 60):** `CountVectorizer(ngram_range=(1,2), max_features=60, min_df=10, binary=True)` on `product_name`. Vietnamese is space-separated so standard tokenization works. Captures signals like "cao cấp" (premium), "hữu cơ" (organic), "rang muối" (salted roast), "lốc" (multipack), "nhập khẩu" (imported) that go beyond the structured features.

### Outputs (in notebook 08)

- **DT1:** Tree diagram (max 4 levels displayed), colored green→red by price
- **DT2:** Leaf PI chart — horizontal bars showing 50%/90% prediction intervals per leaf, sorted by median price, colored by majority product category
- **DT3:** Feature importances (color-coded: category/brand/keyword/continuous) + actual vs. predicted scatter (log-log) with 50%/90% PI bands

### Thesis Placement

Appendix or Section 4.5 (Supplementary): "Alternative Approach — Decision Tree Price Predictor"
- Supports the hedonic findings: if the same attributes dominate (brand_quadrant, parent_category, ln_pack_size) the tree importance ranking validates the OLS finding that these are the main price drivers
- Adds keyword-level evidence: "hữu cơ" / "nhập khẩu" / "cao cấp" appearing in feature importances confirms that name signals carry price information beyond structured attributes
- The leaf PI chart is the most intuitive takeaway: a reader can locate their product type and see the expected price range directly
