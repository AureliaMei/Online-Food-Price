# Thesis Brainstorm: Promotional Pricing in Vietnamese Online Grocery Markets

## Proposed Title

**"Promotional Pricing in Vietnamese Online Grocery Retail: Prevalence, Depth, and Temporal Dynamics"**

---

## Core Insight

Both `final_price` (checkout price) and `marked_price` (sticker price) are crawled per product per day. The gap between them is the discount. Key real numbers:

| Category | % Products on Promotion | Mean Discount (when promoted) |
|---|---|---|
| Dairy | **92.7%** | 11.7% |
| Processed_food | 22.5% | 16.8% |
| Veg_Fruit | **11.6%** | 18.4% |

Packaged/branded goods are heavily discounted; fresh produce rarely has marked prices at all. This is the core business phenomenon.

---

## Research Questions

1. How does promotion prevalence and discount depth differ across food categories?
2. What product and category characteristics predict whether a product is on promotion, and how deeply it is discounted?
3. Is there a Tet holiday effect on promotional pricing behavior?

---

## Theoretical Framework

- **Reference Price Theory** (Thaler 1985; Kalyanaram & Winer 1995): Retailers set artificially high marked prices so discounts appear attractive → predicts higher promotion in branded/packaged goods
- **Hi-Lo vs. EDLP Strategy** (Hoch et al. 1994): Hi-Lo (frequent promotions) for packaged goods; EDLP (stable low prices) for fresh produce → directly maps to Dairy vs. Veg_Fruit finding
- **Promotional pricing in emerging markets**: Limited Vietnam-specific literature using web-scraped data → novelty contribution

---

## Hypotheses

| # | Hypothesis |
|---|---|
| H1 | Promotion prevalence differs significantly across food categories |
| H2 | Conditional discount depth differs significantly across categories |
| H3 | Packaged/branded categories have higher promotion rates than fresh produce |
| H4 | Higher absolute price level predicts deeper discounts |
| H5 | Promotion rates increase significantly in the pre-Tet period (Tet 2026 = Jan 29) |

---

## Data

### Primary — Cross-Sectional Snapshot (zero additional collection needed)
- One daily CSV per category (e.g., Mar 15, 2026)
- N ≈ 170–300 products
- Key variables:
  - `is_promoted` = 1 if marked_price > final_price, else 0
  - `discount_rate` = (marked_price − final_price) / marked_price [= 0 if not promoted]
  - `category`, `subcategory` (from cat_lookup_table.csv join)
  - `log_price` = log(marked_price)
  - `unit_type` (hộp, gói, kg, chai, etc.)
  - `is_packaged` = 1 for all except Veg_Fruit and Egg_and_soy

### Secondary — Panel (already available, 88 days)
- Dec 18, 2025 – Mar 15, 2026
- Unit of analysis: subcategory-level daily average discount_rate (avoids dynamic product catalog problem)
- Tet 2026 (Jan 29) inside window → natural experiment for H5

### Data Challenges
- Dynamic product catalog: different products appear on different days → use subcategory aggregates for panel
- Missing marked_price: treat as not promoted (conservative, noted as limitation)
- Unit heterogeneity: control via unit_type dummies, do NOT normalize across categories

---

## Methodology

### Step 1 — Descriptive Statistics (Chapter 3.1)

Per category compute:
- N products, % promoted, unconditional mean discount_rate, conditional mean/median discount_rate, coefficient of variation

Visualizations:
- Grouped bar chart: % promoted by category
- Box plots: discount_rate by category (all products; then promoted-only)

---

### Step 2 — Hypothesis Testing: Cross-Sectional (Chapter 3.2)

**H1 — Promotion prevalence:**
- Chi-square test: is `is_promoted` independent of `category`?
- Post-hoc: pairwise z-tests for proportions, Bonferroni correction

**H2 — Conditional discount depth:**
- Normality check: Shapiro-Wilk on discount_rate among promoted products
- If normal: Welch's ANOVA + Tukey HSD post-hoc
- If non-normal (expected): Kruskal-Wallis + Dunn's test with Bonferroni correction

**H3 — Packaged vs. fresh:**
- `is_packaged`: 1 for Dairy/Processed/Dry/Instant/Frozen/Confectionary/Spice/Baby; 0 for Veg_Fruit/Egg_and_soy
- Mann-Whitney U test on `is_promoted` and on conditional `discount_rate`

---

### Step 3 — Two-Part Regression Model (Chapter 3.3) ← Core Methodology

`discount_rate` has mass at zero (not promoted) + continuous positive part (promoted). A **two-part / hurdle model** is appropriate — it separates the decision to promote from the depth of promotion.

**Why not plain Tobit?**
Tobit assumes one latent process drives both the 0/non-0 decision AND the magnitude. Two-Part allows different factors to drive *participation* vs. *depth* — more realistic (category strategy decisions are separate from depth decisions) and more interpretable for a business audience.

#### Part 1 — Extensive Margin: P(is_promoted)
- Model: **Probit regression**
- Y: `is_promoted` (0/1)
- X: category dummies (ref = Veg_Fruit), `log_price`, unit_type dummies
- Report: Average Marginal Effects (AMEs) → interpret as percentage-point change in P(promotion)
- Checks: VIF for multicollinearity, McFadden R²

#### Part 2 — Intensive Margin: discount_rate | is_promoted = 1
- Sample: promoted products only
- Model: **OLS with HC3 heteroskedasticity-robust standard errors**
  - If Breusch-Pagan significant and skewed residuals: consider Tobit as robustness check
- Y: `discount_rate` (continuous, 0.028–0.441 in data)
- X: same as Part 1
- Report: OLS coefficients → percentage-point change in discount depth
- Checks: residual plots, Breusch-Pagan, leverage/Cook's D for outliers

**H4 tested by:** sign and significance of `log_price` in Part 2

---

### Step 4 — Tet Event Study (Chapter 3.4)

Tet 2026 = January 29. Clean pre/during/post window inside data range.

**Variable construction (subcategory-day panel):**
- `days_from_tet`: signed integer, 0 = Jan 29
- `tet_period`: dummy = 1 for Jan 15 – Feb 5 ([-14, +7] window)

**Analysis:**
1. Line chart: daily average discount_rate with Tet date as vertical line, by category group
2. Simple mean comparison: pre-Tet (Jan 15–28) vs. baseline (Dec 18 – Jan 14) → t-test or Mann-Whitney
3. Panel regression:
   - Y: daily subcategory discount_rate
   - X: `tet_period`, subcategory fixed effects, day_of_week fixed effects
   - Coefficient on `tet_period` = Tet effect net of subcategory characteristics and weekday patterns

**H5 tested by:** sign and significance of `tet_period`

---

### Step 5 — Robustness Checks (Chapter 3.5)

1. Re-run Parts 1 & 2 on 3 separate snapshot dates (Jan, Feb, Mar) — check coefficient stability
2. Exclude discount_rate > 60% as likely data errors — re-run
3. Alternative packaged/fresh grouping: staples (Veg_Fruit, Egg_and_soy, Dry_Food) vs. non-staples

---

## Optional Extension — Nutrition-Cost Efficiency (~1 week data collection)

If nutritional data (kcal, protein per 100g) collected from product pages or a nutritional database:
- Compute price_per_100kcal and price_per_gram_protein by subcategory
- Research question: Are healthier products discounted less? Does discounting improve nutrition-cost efficiency?
- Model: OLS — Y: price_per_100kcal, X: discount_rate + category dummies

---

## Thesis Structure

1. **Introduction** — research gap (no web-scraped promotional pricing study in Vietnam), objectives, data overview
2. **Literature Review** — Reference Price Theory, Hi-Lo vs. EDLP, promotional pricing in emerging markets
3. **Methodology** — data pipeline, variable construction, models (Steps 1–5)
4. **Results** — descriptive → hypothesis tests → two-part model → Tet event study
5. **Discussion** — interpret, link to theory, business/consumer implications
6. **Conclusion** — limitations (single platform, dynamic catalog), future research

---

## Tools

- Python: `pandas`, `scipy`, `statsmodels` (Probit, OLS, Tobit), `matplotlib`/`seaborn`
- One Jupyter notebook per chapter/analysis section
- All data already in repo — no additional crawling needed for core thesis

---

## Key Files to Use

| File | Role |
|---|---|
| `{Category}/CSV/run_YYYY-MM-DD_*.csv` | final_price + marked_price per product |
| `{Category}/cat_lookup_table.csv` | product → subcategory → category |
| `{Category}/jevons_price_index.csv` | Temporal subcategory panel |
| `overall_daily_average_index.csv` | Context / comparison |
| `official_cpi.json` | Optional CPI benchmark |
