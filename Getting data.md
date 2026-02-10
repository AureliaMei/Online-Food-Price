# 🤖 Data Synchronization Script

## Overview

This script is an **incremental backup tool**. It connects to your local Maxun API, retrieves historical run data for multiple scraping robots, and saves the results as individual JSON files on your hard drive.

It is designed to be run repeatedly. On the first run, it downloads everything. On subsequent runs, it only downloads new data that hasn't been saved yet.

## Key Features

* **📂 Automated Organization:** Creates a dedicated folder for each robot category (e.g., `Electronics/JSON/`, `Veg_Fruit/JSON/`).
* **⚡ Incremental Sync:** Before downloading, it scans your local folders to see what you already have. It skips files that exist, saving time and bandwidth.
* **🗓️ Smart Filenaming:** Converts API timestamps (e.g., `1/30/2026...`) into sortable filenames (e.g., `run_2026-01-30_...`).
* **🛡️ Error Handling:** If one robot fails (e.g., API timeout), the script logs the error and moves to the next robot without crashing.

---

## How It Works (Step-by-Step)

### 1. Configuration

The script starts by defining the connection details and the list of robots to track.

* **`BASE_URL`**: Points to your local Maxun instance (`localhost:8080`).
* **`ROBOTS` Dictionary**: Maps friendly names (e.g., "Dry_Food") to their specific Maxun UUIDs.

### 2. The Logic: `sync_robot_data()`

This function is called once for every robot in the list. It performs the following steps:

#### Step A: Directory Setup

It uses Python's `pathlib` to ensure the destination folder exists.

```python
# Creates ./Electronics/JSON if it doesn't exist
save_dir = Path(f"./{name}/JSON")
save_dir.mkdir(parents=True, exist_ok=True)

```

#### Step B: Local Inventory (The "Memory")

Before asking the server for data, the script looks at what you already have. It scans the `JSON` folder and extracts the **Run IDs** from the filenames.

* *Why?* This creates a "Ignore List" so we don't re-download the same data twice.

#### Step C: Fetching from Server

It requests the run history from Maxun.

* **`limit=5000`**: Ensures we get the entire history, not just the last 10 runs.
* **`sort=startedAt:desc`**: Requests the newest runs first, though the script processes all of them to be safe.

#### Step D: The Sync Loop

The script iterates through every run returned by the server:

1. **Check Status:** It ignores runs that failed or were stopped (only saves `status == 'success'`).
2. **Check Existence:** It asks: *"Is this Run ID in my Local Inventory?"*
* **Yes:** Skip it.
* **No:** Download it.


3. **Save File:** It dumps the run data into a JSON file.

---

## Output Structure

After running the script, your project folder will look like this:

```text
Project_Root/
│
├── sync_script.py
│
├── Electronics/
│   └── JSON/
│       ├── run_2026-01-30_2b41463d.json
│       ├── run_2026-02-01_8f99e561.json
│       └── ...
│
├── Veg_Fruit/
│   └── JSON/
│       ├── run_2025-12-25_424e50fb.json
│       └── ...
│
└── ... (other categories)

```

## Usage

Simply run the script from your terminal:

```bash
python sync_script.py

```

**Console Output Example:**

```text
🚀 Starting Sync Job...
🔍 Electronics: Found 12 local runs. Checking server...
  ✨ Up to date (Server has 12 runs).
🔍 Veg_Fruit: Found 5 local runs. Checking server...
  📥 DOWNLOADED 2 NEW runs.
✅ All jobs finished.

```