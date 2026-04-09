# Hedonic Price Decomposition with Promotional Erosion — Evidence from Vietnamese Online Grocery

## Research Question

*"What product attributes generate price premiums in Vietnamese online grocery, and to what extent do promotional pricing strategies erode those premiums?"*

Using 88 days of web-scraped dual-price data from Vietnam's largest online grocery platform, I decompose food price premiums into attribute components and show that promotional pricing partially — but not fully — erodes brand and import premiums at checkout, with erosion patterns that vary systematically by product category.

---

## Chapter Outline

**Chapter 1 — Introduction**
- 1.1 Motivation for Research
- 1.2 Research Subject and Scope
- 1.3 Research Objectives
- 1.4 Overview of Research Methods
- 1.5 Contribution
- 1.6 Thesis Structure

**Chapter 2 — Literature Review**
- 2.1 Hedonic pricing theory (Lancaster 1966, Rosen 1974, Ekeland et al. 2001)
- 2.2 Hedonic methods in food markets (Costanigro & McCluskey 2011, Nelson 1970, Darby & Karni 1973)
- 2.3 Brand equity and price premiums (Keller 1993, Aaker 1991, Kapferer 2008)
- 2.4 Online retail pricing (Cavallo 2017, Schipmann & Qaim 2011)
- 2.5 Vietnamese context and research gap

**Chapter 3 — Methodology**
- 3.1 Hedonic price model selection and justification (vs. alternatives)
- 3.2 Functional form and estimation strategy (log-linear OLS, subcategory FE, cluster-robust SE)
- 3.3 Dual-price design: marked_price vs. final_price
- 3.4 Brand positioning typology and dummy hierarchy (Keller × Aaker)
- 3.5 Price index methodology (Jevons index)

**Chapter 4 — Empirical Application**
- 4.1 Data source, collection, and single-retailer design
- 4.2 Data limitations and coverage
- 4.3 Variable definitions and descriptive statistics
- 4.4 Pooled hedonic regression results — marked vs. final side-by-side
- 4.5 Per-category heterogeneity
- 4.6 Promotional erosion analysis — coefficient comparison + forest plot
- 4.7 Diagnostics and robustness (VIF, Breusch-Pagan, Cook's distance, 3-month snapshot stability)

**Chapter 5 — Conclusions and Recommendations**
- 5.1 Discussion (why some premiums survive checkout; the WinEco effect)
- 5.2 Tết context (contextualizing the data window, not a formal event study)
- 5.3 Limitations (single-retailer, NLP proxy quality, dynamic catalog, no transaction volumes)
- 5.4 Conclusions
- 5.5 Recommendations (consumers, retailers, future research)

**Appendices**
- A: NLP feature dictionary and keyword lists
- B: Full per-category regression tables
- C: Diagnostics (VIF table, residual plots, QQ plots)
- D: Brand gap temporal dynamics (stability check)

---

## Theoretical Framework

- **Hedonic pricing** (Rosen 1974): goods are bundles of attributes; market prices reveal implicit values for each attribute
- **Brand equity** (Aaker 1991, Kapferer 2012): brand identity creates a sustainable price premium above physical product characteristics
- **Price discrimination via versioning** (Varian 1997): same core product in premium/economy variants
- **Online price measurement** (Cavallo 2016, 2017): web-scraped prices as real-time economic indicators

---

## Data & Methods

### Data Collection
Daily web-scraped prices from Winmart's online platform across 10 food categories, spanning December 18, 2025 to March 2026 (~88 days, ~2,280 products). Each observation records both a marked price (sticker/original) and a final price (checkout/discounted).

### Data Limitations
- **Confectionary cold-start:** Data collection began February 2, 2026 (46 days after other categories). Excluded from temporal analyses spanning the full window; cross-sectional estimates remain valid with `days_observed` control.
- **Instant_food Tet gap:** 18-day gap (Jan 31 – Feb 18) spanning the Tet holiday. No claims about Tet-period pricing effects are made for this category.
- **No formal Tet event study** is included — the two most Tet-sensitive categories (Confectionary, Instant_food) have data gaps during the relevant window.

### Brand Positioning Typology

Products are classified into four quadrants based on brand recognition (keyword matching against ~30 nationally distributed brands) and price tier (above/below subcategory median). The classification is based on Aaker (1991) brand identity model:

| Quadrant | is_branded | is_premium | is_high_recognition | n |
|---|---|---|---|---|
| Generic | 0 | 0 | 0 | 564 |
| Local & Value | 1 | 0 | 0 | 563 |
| Household Giant | 1 | 0 | 1 | 308 |
| Niche Professional | 1 | 1 | 0 | 144 |
| Prestige Leader | 1 | 1 | 1 | — |

Brand dummies are hierarchically encoded — coefficients read as incremental effects.

### Hedonic Specification

```
ln(P/unit) = α + β₁·is_branded + β₂·is_premium + β₃·is_high_recognition
           + β₄·is_import + β₅·is_house_brand
           + β₆·ln(pack_size) + β₇·pack_count
           + β₈·has_health_claim + β₉·has_freshness_claim
           + β₁₀·name_length + γ·subcategory_FE + ε
```

- **Dependent variable:** ln(price per 100g/100ml) after pack size normalization
- **Dual-price design:** Same specification run on marked_price (Spec A) and final_price (Spec B). Coefficient shrinkage from A → B indicates promotional erosion of that attribute's premium.
- **Standard errors:** Cluster-robust by subcategory (Breusch-Pagan rejects homoskedasticity, p < 0.01)
- **Sample filter:** Products with fewer than 7 observed days excluded (87 products, 3.8%)

---

## Key Findings

### Pooled Regression Coefficients

| Variable | β (marked price) | β (final price) | Erosion |
|---|---|---|---|
| is_branded | +0.017 (n.s.) | +0.006 (n.s.) | 65.6% |
| is_premium | +0.429*** | +0.437*** | −1.9% (stable) |
| is_high_recognition | −0.251*** | −0.262*** | 4.3% |

The brand-name signal alone does not generate a statistically significant premium. Price premiums are driven by price-tier positioning, with premium-tier products commanding a 43.7% markup over generic equivalents. High-recognition brands (Household Giants) are actually cheaper conditional on being branded, possibly reflecting economies of scale or heavier promotional activity.

Promotional pricing erodes brand-name premiums (65.6% erosion) but not price-tier premiums (−1.9%), with systematic variation across categories.

### Diagnostics Completed
- VIF: all < 2.0
- Breusch-Pagan test: heteroskedasticity confirmed → justifies cluster-robust SE
- Partial F-tests for variable blocks
- Cook's distance influence diagnostics
- 3-snapshot robustness check (Dec/Jan/Feb)

---

## Single-Retailer Framing

### Methods Paragraph (§4.1)

> "This study employs a single-retailer research design, drawing all price observations from Winmart's online platform. This design choice is deliberate: by restricting data to one retailer, all products face the same platform-level pricing strategy, promotional calendar, and supply chain logistics. This controls for retailer-level confounds that would complicate a multi-retailer hedonic analysis, where observed price differences might reflect retailer positioning rather than product attributes."

### Limitations Paragraph (§5.3)

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


## Existing Output

### Tables (12 CSV files)
Descriptive statistics, pooled and per-category regression results, VIF diagnostics, coefficient comparison/erosion analysis, brand distribution and profiles, premium heatmap, and forest plot data.

### Figures (16 PNG files)
Price distributions by brand tier, regression coefficient forest plot, core erosion visualization (marked vs. final), category-brand quadrant heatmap, promotion penetration scatter, category heterogeneity, and brand gap dynamics (Appendix D).
