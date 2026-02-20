# Online Food Price Tracker

This repository contains an automated pipeline for scraping, processing, and indexing online food prices across multiple product categories.

## Workflow Overview

The data collection and processing pipeline follows a four-stage process:

```
auto_crawl → Getting data → to_csv → mass_categorize_index
```

### Stage 1: `auto_crawl.py` - Trigger Web Scrapers

**Purpose:** Initiate web crawlers to scrape product data from online retailers.

**What it does:**
- Triggers 15 configured web robots via HTTP PUT requests to a local API server (running on port 8080)
- Each robot is mapped to a specific food product category (Electronics, Hygene, Dry_Food, Instant_food, Non-alcohol_beverage, Household_good, Baby_product, Egg_and_soy, Frozen, Spice, Processed_food, Dairy, Confectionary, Detergent, Veg_Fruit)
- Uses JWT authentication token and Cookie headers to authorize requests
- Displays success/failure status for each robot and sends macOS notifications when done
- Robots crawl online food retailers and store raw results on the API server

**Output:** Web crawlers run asynchronously on the backend; results are stored in the API server's database

---

### Stage 2: `Getting data.py` - Sync Crawled Data Locally

**Purpose:** Fetch the raw scraped data from the API server and save it locally as JSON files.

**What it does:**
- Connects to the local API server (`http://localhost:8080/api`) and retrieves robot run results
- For each category:
  - Checks which runs are already saved locally (scanning existing `CategoryName/JSON/` directory)
  - Fetches all successful runs from the API server (filters by `status === "success"`)
  - Downloads only new runs that haven't been saved locally yet
  - Parses API date formats and standardizes them to `YYYY-MM-DD` format
- Saves each run as a JSON file with naming convention: `run_YYYY-MM-DD_RunID.json`
- Provides counts of new downloads and skips redundant data

**Output:** 
- Raw JSON files stored in: `CategoryName/JSON/run_*.json`
- Each JSON file contains the complete product data from one crawler run

---

### Stage 3: `to_csv.py` - Convert and Normalize Data

**Purpose:** Transform raw JSON data into clean, standardized CSV format.

**What it does:**
- Filters JSON files within a configurable date range (default: Feb 8 - Feb 18, 2026)
- Extracts dates from filenames (`run_YYYY-MM-DD_...`) and includes only files in date range
- For each category, applies custom mapping logic (e.g., `map_dairy()`, `map_electronics()`, etc.) to:
  - Extract relevant product fields (product name, unit, prices, URL)
  - Clean price values by removing non-numeric characters and converting to float
  - Normalize two-price logic: determines which is final price vs. marked price based on values
  - Handles missing/null data gracefully (defaults to 0.0 for missing prices)
- Consolidates all products into a single CSV per category
- Standardizes column structure: `product_name`, `unit`, `final_price`, `marked_price`, `product_url`

**Output:**
- Cleaned CSV files stored in: `CategoryName/CSV/run_YYYY-MM-DD_*.csv`
- Ready for analysis with standardized pricing and fields

---

### Stage 4: `mass_categorize_index.py` - Categorize & Build Indexes

**Purpose:** Orchestrate post-processing scripts across all product categories in parallel.

**What it does:**
- Scans all category subdirectories (Baby_product/, Confectionary/, Dairy/, etc.)
- Discovers all `categorize.py` and `subcat_index.py` scripts
- **Phase 1:** Executes all `categorize.py` scripts to:
  - Further classify products into subcategories
  - Generate category lookup tables (`cat_lookup_table.csv`)
  - Store categorized data by category
- **Phase 2:** Executes all `subcat_index.py` scripts to:
  - Build Jevons price indexes for each subcategory
  - Generate `jevons_price_index.csv` tracking price changes over time
- Provides a summary report with success/failure counts for each script
- Handles errors gracefully and continues execution even if individual scripts fail

**Output:**
- Per-category files: `CategoryName/cat_lookup_table.csv` (product-to-subcategory mapping)
- Per-category files: `CategoryName/jevons_price_index.csv` (price index over time)
- JSON and CSV files organized by category and run date

---

## Quick Start

Run the complete pipeline in order:

```bash
python auto_crawl.py          # Trigger web scrapers
python Getting\ data.py        # Fetch and sync data locally
python to_csv.py              # Convert JSON to CSV + clean data
python mass_categorize_index.py # Categorize products & build indexes
```

Or to run individual stages:
- **Fetch fresh data only:** `python Getting\ data.py`
- **Regenerate CSVs from existing JSON:** `python to_csv.py`
- **Rebuild categories and indexes:** `python mass_categorize_index.py`

---

## Configuration

- **Date Range:** Edit `TARGET_START_DATE` and `TARGET_END_DATE` in `to_csv.py`
- **API Server:** Default is `http://localhost:8080` (ensure the local API server is running)
- **Robot IDs & Categories:** See the `ROBOTS` dictionary in `auto_crawl.py` and `Getting data.py`

---

## Directory Structure

Each category folder contains:
- `cat_lookup_table.csv` – Product-to-subcategory mapping
- `categorize.py` – Custom categorization logic for that category
- `jevons_price_index.csv` – Price index tracking
- `subcat_index.py` – Indexing calculation script
- `CSV/` – Cleaned CSV data files (one per run)
- `JSON/` – Raw JSON data files (one per crawler run)
