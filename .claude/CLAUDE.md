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
- Geometric mean of price ratios per subcategory
- Tracked daily

---

## Price Index Methodology

**Jevons Index** = geometric mean of (P_current / P_base) across products in subcategory

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
See `.claude/thesis_brainstorm.md` for full plan.

**Topic:** Promotional Pricing Patterns in Vietnamese Online Grocery Markets
**Angle:** Cross-sectional + temporal analysis of discount rates using the `marked_price` vs `final_price` gap
**Key finding to investigate:** Why do packaged goods (Dairy ~93%) have far higher promotion rates than fresh produce (Veg_Fruit ~12%)?
**Bonus:** Tet holiday event study — Feb 17, 2026 falls inside the data window

---

## Git Info

- Main branch: `main`
- Active branch: `food-only`
- Recent commits track daily data runs (e.g., "data for 15.3")
