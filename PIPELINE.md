# Pipeline Overview

## Data Collection (Steps 00-03)

| Step | File | Description |
|------|------|-------------|
| 00 | `00. auto_crawl.py` | Trigger 15 scraping robots via HTTP PUT |
| 01 | `01. Getting data.py` | Download raw JSON from API server |
| 02 | `02. clean_data.py` | Deduplicate, keep latest run per date |
| 03 | `03. to_csv.py` | Convert JSON to standardized CSV |

## Price Index Pipeline (Steps 04-07)

| Step | File | Description |
|------|------|-------------|
| 04 | `04. mass_categorize_index.py` | Categorize products + compute Jevons indices |
| 04.1 | `04.1. mass_MoM_index.py` | MoM changes per subcategory |
| 05 | `05. food_index.py` | Aggregate to overall/staples/other_food indices |
| 06 | `notebooks/06. visualize.ipynb` | CPI nowcasting dashboard (4 panels) |
| 06.1 | `notebooks/06.1. vizualize daily price.ipynb` | Daily price breakdown, MTD CPI estimates |
| 07 | `notebooks/07. marked_price_index.ipynb` | Replicate pipeline using marked_price |

## Thesis Analysis Pipeline (Steps 08-10)

**Prerequisites:** Run the two library modules first to build the product-level dataset and extract NLP features.

| Step | File | Description |
|------|------|-------------|
| pre | `src/build_product_dataset.py` | Aggregate daily CSVs into product-level dataset (`output/product_dataset.csv`) |
| pre | `src/nlp_features.py` | Extract NLP features from product names (`output/product_features.csv`) |
| 08 | `notebooks/08. hedonic_regression.ipynb` | Hedonic pricing OLS regressions + thesis tables |
| 09 | `notebooks/09. visualize_hedonic.ipynb` | 5 publication-ready thesis figures |
| 10 | `notebooks/10. brand_price_dynamics.ipynb` | Brand vs. generic price gap dynamics over time |

## How to Re-run the Thesis Pipeline

```bash
# Step pre: Build product dataset + NLP features
python -m src.build_product_dataset
python -m src.nlp_features

# Steps 08-10: Run notebooks in order
jupyter nbconvert --to notebook --execute "notebooks/08. hedonic_regression.ipynb" --inplace
jupyter nbconvert --to notebook --execute "notebooks/09. visualize_hedonic.ipynb" --inplace
jupyter nbconvert --to notebook --execute "notebooks/10. brand_price_dynamics.ipynb" --inplace
```

## Key Output Files

| File | Produced by | Content |
|------|-------------|---------|
| `output/product_dataset.csv` | `src/build_product_dataset.py` | 2,274 products with prices, promo stats, brand names |
| `output/product_features.csv` | `src/nlp_features.py` | Product features for hedonic regression |
| `output/thesis_table_brand_profiles.csv` | `src/build_product_dataset.py` | Brand-level aggregated stats |
| `output/thesis_table1_descriptive.csv` | Step 08 | Category-level descriptive stats |
| `output/thesis_table2_pooled_regression.csv` | Step 08 | Pooled OLS coefficients |
| `output/thesis_table3_category_regression.csv` | Step 08 | Per-category OLS estimates |
| `output/thesis_fig*.png` | Step 09 | 5 thesis figures |
| `output/brand_gap_daily.csv` | Step 10 | Daily branded-generic gap per category |
| `output/brand_gap_summary.csv` | Step 10 | Gap summary with Tet comparison |

## Library Modules (src/)

| Module | Role |
|--------|------|
| `src/utils.py` | Shared utilities: `PROJECT_ROOT`, `extract_date()`, `load_labels()` |
| `src/build_product_dataset.py` | Product-level aggregation from daily CSVs |
| `src/nlp_features.py` | NLP feature extraction (brand, origin, health claims, pack size) |
| `src/categorize_core.py` | Product categorization engine |
| `src/index_core.py` | Jevons price index computation |
