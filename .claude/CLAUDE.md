# Online Food Price — Project Context

## What This Repo Is

A web scraping + price indexing pipeline that tracks daily food prices from a Vietnamese online grocery platform (Winmart). Data spans **Dec 18, 2025 – present** with daily crawls across 10 food categories and ~170+ products.

---

## Pipeline Overview

```
00. auto_crawl.py       → triggers 15 scraping robots via HTTP PUT (localhost:8080, JWT auth)
01. Getting data.py     → downloads raw JSON from API server, saves as run_YYYY-MM-DD_RunID.json
02. clean_data.py       → deduplicates, keeps latest run per date
03. to_csv.py           → converts JSON → standardized CSV (product_name, unit, final_price, marked_price, url)
04. mass_categorize_index.py → runs all categorize.py + subcat_index.py in parallel
04.1. mass_MoM_index.py → MoM changes per subcategory, excludes staples
05. food_index.py       → aggregates Jevons indices into overall/staples/other_food
06. visualize.ipynb     → CPI nowcasting dashboard (4 panels)
06.1. vizualize daily price.ipynb → daily price breakdown, MTD CPI estimates
```

---

## Data Structure

### Category Folders (10 total)
Each has: `JSON/`, `CSV/`, `cat_lookup_table.csv`, `categorize.py`, `subcat_index.py`, `jevons_price_index.csv`

| Folder | Category (Vietnamese) | Subcategories |
|---|---|---|
| Dairy | Sữa | Sữa Tươi, Sữa Hạt-Đậu, Sữa Bột, Bơ-Phô Mai, Sữa Đặc, Sữa Chua |
| Veg_Fruit | Rau-Trái | Rau Lá, Củ Quả, Trái cây tươi |
| Dry_Food | Thực phẩm khô | Gạo-Nông Sản Khô, Ngũ Cốc-Yến Mạch, Bột, Đóng Hộp, Thực Phẩm Chay |
| Instant_food | Mì/Ăn liền | Mì, Miến-Hủ Tíu, Cháo, Phở-Bún |
| Processed_food | Thực phẩm chế biến | Bánh mì, Xúc xích-Thịt Nguội, Bánh bao, Kim chi, Khác |
| Frozen | Đông lạnh | Hải Sản, Thịt, Chả Giò, Cá-Bò Viên |
| Egg_and_soy | Trứng-Đậu | Trứng, Đậu hũ |
| Confectionary | Bánh Kẹo | Bánh Xốp-Quy, Kẹo-Chocolate, Bánh Snack, Hạt Sấy |
| Spice | Gia vị | (multiple) |
| Baby_product | Chăm sóc bé | Sữa Bột-Dinh Dưỡng, Tã-Bỉm, Sữa Tắm-Gội |

### CSV Schema (per product per day)
```
product_name, unit, final_price, marked_price, product_url, scrape_timestamp, run_id
```
- `final_price` = checkout price (sale/discounted)
- `marked_price` = sticker price (original)
- Price in VND (e.g., 26100 = 26,100 VND)

### Key Derived Files (root level)
- `overall_daily_average_index.csv` — columns: date, overall_average_index, staples_average_index, other_food_average_index (base 1.0 = Dec 18, 2025)
- `other_food_mom_change.csv` — 35 subcategory MoM Jevons indices
- `subcategory_kmeans_groups.csv` — K-means cluster assignments (3 clusters) by price movement pattern
- `official_cpi.json` — official GSO CPI data for comparison

### Jevons Price Index (per category)
- Base date: Dec 18, 2025 (= 1.0)
- Chain-linked geometric mean of daily price relatives per subcategory
- Tracked daily

---

## Price Index Methodology

**Jevons Index** = chain-linked geometric mean where each day's index = previous day's index × geometric mean of matched-product price relatives (P_t / P_{t-1}). Base date Dec 18, 2025 = 1.0. Products not present on consecutive days are excluded from that day's link.

**Aggregation:**
- Staples = Gạo-Nông Sản Khô + Ngũ Cốc-Yến Mạch (from Dry_Food)
- Other Food = all subcategories excluding staples + Baby_product (only Sữa Bột-Dinh Dưỡng)
- Overall = geometric mean of Staples + Other Food

**CPI Nowcasting:** compare online Jevons MoM change vs. official GSO CPI MoM change

---

## Known Data Characteristics

- ~85 CSV files per category (Dec 2025 – Mar 2026), ~88 days
- Product catalog is **dynamic**: new products added, some removed across dates
- Promotion penetration varies dramatically by category:
  - Dairy: **92.7%** of products on promotion (marked_price > final_price)
  - Processed_food: 22.5%
  - Veg_Fruit: **11.6%**
- Discount depth (when promoted): Dairy ~11.7%, Processed_food ~16.8%, Veg_Fruit ~18.4%
- Tet 2026 = February 17, 2026 — falls within data window

---

## Ongoing Work

### Bachelor Thesis Project
See `.claude/thesis_brainstorm.md` for full plan. Primary draft: `Thesis_Draft_Comprehensive.docx`.

**Topic:** Hedonic Price Decomposition with Promotional Erosion — Evidence from Vietnamese Online Grocery
**RQ:** What product attributes generate price premiums in Vietnamese online grocery, and to what extent do promotional pricing strategies erode those premiums?
**Core finding:** Dual-price hedonic regression (marked vs final price) shows promotional pricing erodes brand-name premiums (50.6%) but not price-tier premiums (−1.7%), with systematic variation across categories
**Status:** Analysis complete. Thesis writing phase.

### Thesis Chapter Structure (based on Thesis_Draft_Comprehensive.docx)

```
Chapter 1  Introduction
  1.1  Research subject and scope
  1.2  Research objectives
  1.3  Overview of research methods
  1.4  Contribution

Chapter 2  Literature Review
  2.1  Hedonic Pricing Theory: Goods as Attribute Bundles (Lancaster 1966, Rosen 1974, Ekeland et al. 2004)
  2.2  Hedonic Methods in Food and Agricultural Markets (search/experience/credence attributes, methodological precedents)
  2.3  Brand Equity, Product Differentiation, and Price Premiums (Keller 1993, Aaker 1991, 4-quadrant typology)
  2.4  Online Retail Pricing and Web-Scraped Price Data (Cavallo 2017, Schipmann & Qaim 2011)
  2.5  Vietnamese Food Market Context and Research Gap

Chapter 3  Methodology
  Opening: Model selection justification — why hedonic regression (vs. discrete choice, ML)
  3.2  Functional form and estimation strategy — log-linear OLS, subcategory FE, cluster-robust SE; why not Box-Cox, quantile regression, panel FE
  3.3  Dual-price design — marked vs. final; erosion metric; why not single-price hedonic, DiD
  3.4  Feature extraction and brand positioning typology — NLP pipeline, Keller × Aaker 4-quadrant, hierarchical encoding
  3.5  Price index methodology — Jevons (chain-linked geometric mean); why not Laspeyres/Törnqvist

Chapter 4  Empirical Application
  4.1  Data source, collection, and single-retailer design (Winmart, 15 robots, 10 categories, 88 days, ~2,280 products)
  4.2  Data limitations and coverage (Confectionary cold-start, Instant_food Tết gap, no formal Tết event study, dynamic catalog, no transaction volumes)
  4.3  Variable definitions and descriptive statistics (9 NLP features, Table 1 by category)
  4.4  Pooled hedonic regression results (Table 2: marked vs. final side-by-side; Figure 2: forest plot)
  4.5  Per-category heterogeneity (Table 3; import +100% in Fresh Produce, −61% in Processed Food)
  4.6  Promotional erosion analysis — THE key finding (brand-name 50.6% erosion, price-tier −1.7%, WinEco 476%)
  4.7  Diagnostics and robustness (VIF < 2.0, Breusch-Pagan, Cook's distance, 3-month snapshot stability)

Chapter 5  Conclusions and Recommendations
  5.1  Discussion — why price-tier survives (Varian versioning), why brand-name erodes (traffic-driving), WinEco private-label strategy, import/health claim heterogeneity, Tết context
  5.3  Limitations — single-retailer external validity, NLP proxy quality, dynamic catalog, no transaction volumes, is_premium endogeneity
  5.4  Conclusions — three principal findings + contribution + scope boundary
  5.5  Recommendations — for consumers (price tier > brand), businesses (premium positioning protected, Household Giants are promo targets), public/policymakers (penetration vs. depth, dual-pricing transparency), future research (multi-retailer, transaction data, IV)

Appendices: A (NLP dictionary), B (per-category tables), C (diagnostics), D (brand gap dynamics)
```

### Thesis Drafts
- `Thesis_Draft_Comprehensive.docx` — full draft (Ch 1 prose, Ch 2–5 detailed bullets with figures)
- `Thesis_Draft_Ch3_4_Bullets.docx` — bullet-point summary of Ch 3–4
- `Thesis_Chapter2.docx` — Chapter 2 standalone
- `thesis_outline_ch1_4.docx` — detailed prose outline (Ch 1–4 full paragraphs, Ch 5 bullets)
- `.claude/thesis_brainstorm.md` — canonical chapter plan with methodology alternatives
- `thesis_summary_for_professor.md` — summary with key coefficients

---

## Git Info

- Main branch: `main`
- Active branch: `food-only`
- Recent commits track daily data runs (e.g., "data for 15.3")
