# Thesis: Hedonic Price Decomposition with Promotional Erosion — Evidence from Vietnamese Online Grocery

## Research Question

**Single RQ:** *"What product attributes generate price premiums in Vietnamese online grocery, and to what extent do promotional pricing strategies erode those premiums?"*

**One-sentence pitch:** Using 88 days of web-scraped dual-price data from Vietnam's largest online grocery platform, I decompose food price premiums into attribute components and show that promotional pricing partially — but not fully — erodes brand and import premiums at checkout, with erosion patterns that vary systematically by product category.

---

## Chapter Outline

```
Chapter 1  Introduction
  1.1  Research subject and scope
       - Food price premiums in Vietnamese online grocery retail
       - Scope: 10 food categories, ~2,280 products, 88 days of web-scraped data from Winmart
  1.2  Research objectives
       - Identify which product attributes generate price premiums
       - Quantify how promotional pricing erodes those premiums at checkout
  1.3  Overview of research methods
       - Web scraping + NLP feature extraction → dual-price hedonic regression (marked vs final)
       - Single-retailer design rationale (preview of §3.1)
  1.4  Contribution to the topic
       - Contribution statement (use qualified claim from thesis_todo_lit_search.md)
       - First dual-price hedonic analysis of Vietnamese online grocery

Chapter 2  Literature Review
  - Hedonic pricing theory (Rosen 1974, Lancaster 1966)
  - Brand equity and positioning (Aaker 1991, Kapferer 2012)
  - Online retail pricing and promotional strategy (Varian 1997, Cavallo 2016)
  - Vietnamese consumer market — gap identification

Chapter 3  Data & Methods
  3.1  Data collection (Winmart scraping, 10 categories, 88 days, ~2,280 products)
  3.2  Data limitations and coverage (Confectionary cold-start, Instant_food gap)
  3.3  NLP feature extraction (9 features from product names)
  3.4  Brand positioning typology and dummy hierarchy
  3.5  Hedonic specification (pooled OLS + subcategory FE + cluster-robust SE)
  3.6  Dual-price design: marked_price vs. final_price

Chapter 4  Results and Discussion
  4.1  Descriptive statistics (Table 1, incl. promotion penetration by category)
  4.2  Pooled hedonic regression (Table 2) — marked vs. final side-by-side
  4.3  Per-category heterogeneity (Table 3) — why premiums differ across categories
  4.4  Promotional erosion analysis — THE key finding (coefficient comparison + forest plot)
  4.5  Diagnostics and robustness
       - VIF (all < 2.0), Breusch-Pagan, partial F-tests
       - Cook's distance influence diagnostics
       - 3-month snapshot stability (Dec/Jan/Feb)
  4.6  Discussion
       - Why some premiums survive checkout (import, health claims) and others don't
       - The WinEco effect: house brand discount amplified by promotions (431% erosion)
       - Tet context (1–2 paragraphs — not an event study, but contextualizing the data window)
  4.7  Limitations
       - Single-retailer (Winmart only)
       - NLP proxy quality (brand list, health claim keywords)
       - Dynamic product catalog
       - No transaction volumes (cannot compute sales-weighted indices)

Chapter 5  Conclusion

Appendix A  NLP feature dictionary and keyword lists
Appendix B  Full per-category regression tables (with dropped-variable footnotes)
Appendix C  Diagnostics (VIF table, residual plots, QQ plots)
Appendix D  Brand gap temporal dynamics (1-page stability check, NO Tet analysis)
```

---

## Theoretical Framework

- **Hedonic pricing** (Rosen 1974): goods are bundles of attributes; market prices reveal implicit values for each attribute
- **Brand equity** (Aaker 1991, Kapferer 2012): brand identity creates a sustainable price premium above physical product characteristics — anchor for the brand positioning typology
- **Price discrimination via versioning** (Varian 1997): same core product in premium/economy variants
- **Online price measurement** (Cavallo 2016, 2017): web-scraped prices as real-time economic indicators

---

## §3.2 — Data Limitations and Coverage

### Confectionary 46-Day Cold-Start

The Confectionary (Bánh Kẹo) price index begins **2026-02-02** with base = 1.0, 46 days after the Dec 18 base date used for all other categories. The Confectionary category page was not included in the initial scraping robot configuration and was added on Feb 2, 2026.

**Consequences:**
- The overall Jevons index (`overall_daily_average_index.csv`) is computed as `combined_df.mean(axis=1)` with `skipna=True` in `05. food_index.py`. Before Feb 2, the overall index averages over 9 categories; from Feb 2 onward, over 10. This creates a **silent composition break** in the aggregate series.
- Cross-category time-series charts comparing Confectionary alongside Dec-18-based categories are misleading (different base dates, different observation windows).
- Confectionary is one of the highest-demand Tet categories — the entire pre-Tet surge window is unobserved.

**Mitigation for hedonic regression:** The cross-sectional product dataset averages prices over each product's available days. Confectionary products simply have fewer averaged observations (max ~50 days vs. ~88 for other categories). The `days_observed` variable controls for this, and sparse products (< 7 days) are already filtered.

**Thesis text:** "Confectionary data collection began on February 2, 2026, 46 days after the other nine categories. This category is excluded from temporal analyses spanning the full December–March window. Cross-sectional hedonic estimates for Confectionary are based on a shorter observation window (maximum 50 days) but remain valid as the `days_observed` variable controls for observation length."

### Instant_food 18-Day Tet Gap

Instant_food has a continuous **18-day gap from January 31 to February 18, 2026**, spanning the entire Tet holiday period (Tet = Feb 17). Additionally, 3 of 4 subcategories (Cháo, Miến-Hủ Tíu, Phở-Bún) have no data for the first ~10 days (Dec 18–28), with only Mì reporting from day 1.

**Consequences:**
- Instant noodles are a classic Tet stockpiling category — the missing window is exactly where a price spike would be expected.
- The chain-linked Jevons index bridges the gap by linking Jan 31 directly to Feb 18, but this masks whatever happened during the 18 missing days.

**Mitigation:** Same as Confectionary — the cross-sectional hedonic regression averages over available days and is robust to temporal gaps.

**Thesis text:** "The Instant_food category exhibits an 18-day data gap (January 31 – February 18, 2026) coinciding with the Tet holiday period. No claims about Tet-period pricing effects are made for this category."

### Why No Tet Event Study

Confectionary (missing pre-Tet entirely) and Instant_food (missing Tet week) are the two most Tet-sensitive product categories. Without these, a formal Tet event study would exclude the categories where the effect is strongest, rendering the analysis incomplete. **No formal Tet event study is included.** However, Tet is discussed in §4.6 as contextual background — see below.

---

## §4.6 — Tet Context (Discussion, 1–2 Paragraphs)

The data window (Dec 18, 2025 – Mar 2026) spans Tet Nguyên Đán 2026 (February 17). This is not incidental — Tet is the single largest demand shock in the Vietnamese food calendar, driving stockpiling of staples, gift-giving of packaged goods, and promotional surges by retailers.

**What can be said (for categories with continuous data):** For the 8 categories with uninterrupted data through the Tet window (Dairy, Veg_Fruit, Dry_Food, Frozen, Processed_food, Egg_and_soy, Spice, Baby_product), the brand gap temporal dynamics in Appendix D provide descriptive context. Any visible compression or widening of the branded–generic price gap around mid-February can be noted as suggestive, but should not be interpreted causally.

**What cannot be said:** Confectionary (46-day cold-start, missing pre-Tet) and Instant_food (18-day gap spanning Tet week) are the two most Tet-sensitive categories. Their absence from the Tet window makes any formal event study indefensible.

**Draft text:** "The 88-day observation window encompasses Tet Nguyên Đán 2026 (February 17), Vietnam's most significant consumption event. While a formal Tet event study is precluded by data gaps in two key holiday categories (Confectionary and Instant_food), the temporal stability of brand premiums across this period — observable for the remaining eight categories — suggests that the cross-sectional hedonic estimates are not artifacts of a single seasonal pricing regime."

---

## §3.4 — Brand Positioning Typology and Dummy Hierarchy

### The 4-Quadrant Brand Classification

Products are classified into four quadrants based on:
1. **Brand recognition** — substring matching against a curated keyword list of ~30 nationally distributed brands (e.g., Vinamilk, TH True Milk, Dutch Lady)
2. **Price tier** — whether the product's average price exceeds its subcategory median

| Quadrant | is_branded | is_premium | is_high_recognition | n |
|---|---|---|---|---|
| Generic (no brand) | 0 | 0 | 0 | 564 |
| Local & Value | 1 | 0 | 0 | 563 |
| Household Giant | 1 | 0 | 1 | 308 |
| Niche Professional | 1 | 1 | 0 | 144 |
| Prestige Leader | 1 | 1 | 1 | — |

### Hierarchical Dummy Encoding

The three brand dummies are **hierarchical**, not independent:
- `is_premium = 1` **implies** `is_branded = 1`
- `is_high_recognition = 1` **implies** `is_branded = 1`

This means the coefficients must be read as **incremental** effects:

| Premium over Generic | Coefficient formula |
|---|---|
| Local & Value vs. Generic | β(is_branded) |
| Niche Professional vs. Generic | β(is_branded) + β(is_premium) |
| Household Giant vs. Generic | β(is_branded) + β(is_high_recognition) |
| Prestige Leader vs. Generic | β(is_branded) + β(is_premium) + β(is_high_recognition) |

### Actual Coefficients (from pooled regression)

| Variable | β (marked) | β (final) | Erosion |
|---|---|---|---|
| is_branded | +0.017 (n.s.) | +0.006 (n.s.) | 65.6% |
| is_premium | +0.429*** | +0.437*** | −1.9% (stable) |
| is_high_recognition | −0.251*** | −0.262*** | 4.3% |

**Key interpretation:** The brand name alone (`is_branded`) carries essentially zero premium — the coefficient is not statistically significant. The premium comes entirely from the **price-tier positioning** (`is_premium`). High-recognition brands (Household Giants) are actually *cheaper* conditional on being branded, possibly reflecting economies of scale or heavier promotional activity.

**Do NOT say:** "There is a brand premium of X%."
**DO say:** "The brand-name signal alone does not generate a statistically significant premium. Price premiums are driven by the price-tier positioning of the brand, with premium-tier products commanding a 43.7% markup over generic equivalents."

### Footnote Template for Regression Tables

> "Brand dummies are hierarchically encoded. `is_branded` captures the Local & Value vs. Generic contrast only. The total premium for a Prestige Leader product equals β₁ + β₂ + β₃. See Section 3.4 for the full interpretation guide."

---

## Single-Retailer Framing

### Methods Paragraph (§3.1 or §3.7)

> "This study employs a single-retailer research design, drawing all price observations from Winmart's online platform. This design choice is deliberate: by restricting data to one retailer, all products face the same platform-level pricing strategy, promotional calendar, and supply chain logistics. This controls for retailer-level confounds that would complicate a multi-retailer hedonic analysis, where observed price differences might reflect retailer positioning rather than product attributes."

### Limitations Paragraph (§4.7)

> "A key limitation is that findings are specific to Winmart's online channel and cannot be generalized to the Vietnamese food retail sector as a whole. Winmart occupies a mid-market position in Vietnam's modern trade segment; premium retailers (e.g., Annam Gourmet) or traditional wet markets would likely exhibit different premium structures. The product assortment over-represents branded and packaged goods relative to traditional trade channels. Future work should extend this analysis to multiple retail formats to test whether the attribute premiums identified here are retailer-specific or reflect broader market-level valuations."

**Important:** These are two separate paragraphs in different sections. Do NOT combine them — it reads as defensive rationalization.

---

## Hedonic Regression Specification

### Dependent Variable
`ln(price_per_standardized_unit)` — log price per 100g/100ml after pack size normalization

### Model
```
ln(P/unit) = α + β₁·is_branded + β₂·is_premium + β₃·is_high_recognition
           + β₄·is_import + β₅·is_house_brand
           + β₆·ln(pack_size) + β₇·pack_count
           + β₈·has_health_claim + β₉·has_freshness_claim
           + β₁₀·name_length + γ·subcategory_FE + ε
```

### Dual-Price Design
Run the same specification twice:
- **Specification A:** DV = ln(marked_price / unit) — sticker price premiums
- **Specification B:** DV = ln(final_price / unit) — checkout price premiums

If a coefficient shrinks from A → B, promotions are eroding that attribute's premium at checkout.

### Standard Errors
Cluster-robust SE by subcategory. Justified by:
- Breusch-Pagan test rejects homoskedasticity (BP χ², p < 0.01)
- Products within the same subcategory share unobserved pricing factors

### Sample Filters
- Sparse product filter: `days_observed >= 7` (removes 87 products, 3.8%)
- Effective N ≈ 2,175 (after KG-sold produce unit normalization recovery)

---

## What Was Cut vs. Kept

| Old Content | Disposition | Rationale |
|---|---|---|
| Hedonic regression (Steps 1-4) | **KEPT**, expanded | Core of thesis |
| Dual-price comparison (marked vs final) | **KEPT**, deepened | Centerpiece finding |
| Per-category heterogeneity | **KEPT** | Shows systematic variation |
| Brand gap dynamics (Part D) | **DEMOTED** → 1-page Appendix D | Temporal stability check only |
| Tet event study | **DEMOTED** → 1–2 paragraphs in §4.6 | No formal study (data gaps), but Tet contextualized in Discussion |
| Decision tree (Part E) | **CUT entirely** | Supplementary, distracts from hedonic story |
| 5-hypothesis promo chapter | **CUT** | Absorbed into §4.1 descriptives + §4.4 erosion |

---

## Existing Output Files

### Tables (12 CSV files)
- `thesis_table1_descriptive.csv` — Table 1: descriptive stats by category
- `thesis_table2_pooled_regression.csv` — Table 2: pooled OLS (marked vs final)
- `thesis_table3_category_regression.csv` — Table 3: per-category regressions
- `thesis_table_vif.csv` — VIF diagnostics (all < 2.0)
- `thesis_table_coefficient_comparison.csv` — Erosion analysis (coefficient comparison)
- `thesis_table_category_heterogeneity.csv` — Standardized coefficients by category
- `thesis_table_brand_distribution.csv` — Brand prevalence across categories
- `thesis_table_brand_erosion.csv` — Per-category brand premium erosion
- `thesis_table_promo_vs_premium.csv` — Promo penetration vs brand premium
- `thesis_table_brand_profiles.csv` — 150+ brands with quadrants
- `thesis_table_premium_heatmap.csv` — Category × brand quadrant cross-tab
- `thesis_table_forest_plot.csv` — Forest plot data

### Figures (16 PNG files)
- `thesis_fig1_brand_price_distribution.png` — Price distributions by brand tier
- `thesis_fig2_forest_plot.png` — Regression coefficient forest plot
- `thesis_fig3_brand_premium_marked_vs_final.png` — **Core finding: erosion visualization**
- `thesis_fig4_premium_heatmap.png` — Category × brand quadrant heatmap
- `thesis_fig5_promo_vs_brand_premium.png` — Promo penetration scatter
- `thesis_fig_coefficient_erosion.png` — Detailed coefficient erosion
- `thesis_fig_category_heterogeneity.png` — Category heterogeneity
- `thesis_figD1–D5` — Brand gap dynamics (Appendix D)
- `thesis_dt_*.png` — Decision tree outputs (NOT used in thesis, kept for reference)

---

## Deferred Tasks (User-Driven)

### 1. Brand Quadrant Theory Grounding
**File:** `.claude/thesis_todo_brand_theory.md`
**Feeds into:** Chapter 2 (literature review) + §3.4 (brand typology)
**Task:** Anchor the 4-quadrant decomposition in Aaker (1991) brand equity model or Kapferer (2012) brand identity prism. Call it "market positioning typology," not "brand equity measure."

### 2. Literature Gap Verification
**File:** `.claude/thesis_todo_lit_search.md`
**Feeds into:** Chapter 1 (contribution statement)
**Task:** Run structured Google Scholar searches to verify the novelty claim. Use qualified template: "To the author's knowledge, this is the first hedonic analysis of brand, import, and health claim premiums using web-scraped daily data from Vietnamese online grocery retail."

---

## Rigor Checklist (What's Already Done)

- [x] VIF check: all < 2.0
- [x] Breusch-Pagan test: heteroskedasticity confirmed → justifies cluster-robust SE
- [x] Partial F-tests for variable blocks
- [x] Cook's distance influence diagnostics
- [x] 3-snapshot robustness (Dec/Jan/Feb)
- [x] Sparse product filter (days_observed >= 7)
- [x] Pre-flight variance check in per-category regressions
- [x] KG-sold produce unit normalization recovered (~100 products)
- [ ] Brand quadrant theory grounding (user task)
- [ ] Literature gap verification (user task)
