import json
import pandas as pd
from pathlib import Path

def get_timestamp(json_path: Path):
    """Reads the JSON to extract the exact startedAt timestamp for sorting."""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Use pandas to easily parse the datetime string
            return pd.to_datetime(data.get('startedAt', ''))
    except Exception:
        # Fallback to max time so broken files are treated as "latest" and deleted
        return pd.Timestamp.max

def clean_same_day_runs():
    root_dir = Path('.')
    print(f"🚀 Scanning for same-day runs in: {root_dir.absolute()}\n")

    for category_dir in root_dir.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith('.') or category_dir.name in ['venv', '__pycache__']:
            continue
            
        json_dir = category_dir / 'JSON'
        csv_dir = category_dir / 'CSV'
        jevons_path = category_dir / 'jevons_price_index.csv'
        
        if not json_dir.exists():
            continue
            
        print(f"📂 Checking {category_dir.name}...")
        runs_by_date = {}
        
        # 1. Group all JSONs by the date in their filename
        for json_file in json_dir.glob("run_*.json"):
            parts = json_file.stem.split('_')
            # Expected format: run_YYYY-MM-DD_runID
            if len(parts) >= 3:
                date_str = parts[1] 
                run_id = parts[2]
                
                if date_str not in runs_by_date:
                    runs_by_date[date_str] = []
                
                runs_by_date[date_str].append({
                    'json_path': json_file,
                    'run_id': run_id,
                    'timestamp': get_timestamp(json_file)
                })
        
        # 2. Identify and Delete the Later Runs
        for date_str, runs in runs_by_date.items():
            if len(runs) > 1:
                # Sort runs chronologically (oldest/first run at index 0)
                runs.sort(key=lambda x: x['timestamp'])
                
                # Keep the first run, target the rest for deletion
                runs_to_delete = runs[1:]
                
                for run in runs_to_delete:
                    # A. Delete the JSON
                    try:
                        run['json_path'].unlink()
                        print(f"  🗑️ Deleted later JSON: {run['json_path'].name}")
                    except Exception as e:
                        print(f"  ⚠️ Could not delete JSON: {e}")
                        
                    # B. Delete the corresponding CSV
                    if csv_dir.exists():
                        # Find any CSV containing this specific run_id
                        for csv_file in csv_dir.glob(f"*{run['run_id']}*.csv"):
                            try:
                                csv_file.unlink()
                                print(f"  🗑️ Deleted linked CSV: {csv_file.name}")
                            except Exception:
                                pass
        
        # 3. Clean up the Jevons file
        if jevons_path.exists():
            try:
                df = pd.read_csv(jevons_path)
                if 'date' in df.columns:
                    original_len = len(df)
                    
                    # Drops any rows with duplicate dates, keeping only the first one
                    df.drop_duplicates(subset=['date'], keep='first', inplace=True)
                    new_len = len(df)
                    
                    if original_len != new_len:
                        df.to_csv(jevons_path, index=False)
                        print(f"  🧹 Removed {original_len - new_len} extra same-day rows from {jevons_path.name}")
            except pd.errors.EmptyDataError:
                pass

    print("\n✅ Cleanup finished.")

if __name__ == "__main__":
    clean_same_day_runs()