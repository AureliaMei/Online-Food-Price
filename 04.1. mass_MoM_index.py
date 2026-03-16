import pandas as pd
import numpy as np
from scipy.stats import gmean
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from src.utils import extract_date

# --- CONFIGURATION ---
root_dir = Path(__file__).parent
output_index_file = root_dir / 'other_food_mom_change.csv'

# Subcategories to EXCLUDE (because they belong to Staples)
staples = ['Gạo - Nông Sản Khô', 'Ngũ Cốc - Yến Mạch']

def main():
    print(f"🚀 Scanning all directories in: {root_dir.absolute()} for Other Food...")

    # Dictionary to store all daily dataframes across all categories
    # Format: {'2026-01-28': combined_dataframe_for_that_day}
    historical_dfs = {} 

    # 1. Collect and filter data from ALL category folders
    for category_dir in root_dir.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith('.') or category_dir.name in ['venv', '__pycache__']:
            continue
            
        csv_folder = category_dir / 'CSV'
        lookup_file = category_dir / 'cat_lookup_table.csv'
        
        if not csv_folder.exists() or not lookup_file.exists():
            continue
            
        try:
            lookup = pd.read_csv(lookup_file, usecols=['product_name', 'subcategory'])
        except Exception as e:
            print(f"  ⚠️ Could not read lookup in {category_dir.name}: {e}")
            continue

        for file_path in csv_folder.glob('*.csv'):
            current_date = extract_date(file_path.name)
            
            try:
                df = pd.read_csv(file_path, usecols=['product_name', 'final_price'])
                df = df.merge(lookup, on='product_name', how='left')
                df = df.dropna(subset=['subcategory', 'final_price'])
                
                # Apply Category-Specific Rules
                if category_dir.name == 'Baby_product':
                    # Only keep the target subcategory for baby products
                    df = df[df['subcategory'] == 'Sữa Bột - Sữa Dinh Dưỡng']
                else:
                    # Exclude Staples for everything else
                    df = df[~df['subcategory'].isin(staples)]
                    
                if df.empty:
                    continue
                    
                if current_date not in historical_dfs:
                    historical_dfs[current_date] = []
                historical_dfs[current_date].append(df)
                
            except Exception:
                pass

    if not historical_dfs:
        print("❌ No valid data found after filtering.")
        return

    # Combine the daily lists into single dataframes
    for date_str, df_list in historical_dfs.items():
        historical_dfs[date_str] = pd.concat(df_list, ignore_index=True)

    # 2. Calculate the MoM Jevons Ratio
    print("\n⏳ Calculating Month-over-Month changes...")
    dates = sorted(historical_dfs.keys())
    results = []

    for current_date in dates:
        curr_df = historical_dfs[current_date]
        
        # Determine the exact date one month ago
        past_date_obj = pd.to_datetime(current_date) - pd.DateOffset(months=1)
        past_date_str = past_date_obj.strftime('%Y-%m-%d')
        
        day_results = {'date': current_date}
        
        if past_date_str in historical_dfs:
            past_df = historical_dfs[past_date_str]
            subcategories = curr_df['subcategory'].unique()
            
            for sub in subcategories:
                p_past = past_df[past_df['subcategory'] == sub][['product_name', 'final_price']]
                p_curr = curr_df[curr_df['subcategory'] == sub][['product_name', 'final_price']]
                
                matched = p_past.merge(p_curr, on='product_name', suffixes=('_past', '_curr'))
                matched = matched[(matched['final_price_past'] > 0) & (matched['final_price_curr'] > 0)]

                if not matched.empty:
                    price_relatives = matched['final_price_curr'] / matched['final_price_past']
                    day_results[sub] = gmean(price_relatives)
                else:
                    day_results[sub] = np.nan
        else:
            # If no data exists exactly one month prior, we cannot compute a MoM change
            for sub in curr_df['subcategory'].unique():
                day_results[sub] = np.nan
                
        results.append(day_results)

    # 3. Format and Output
    if results:
        final_df = pd.DataFrame(results)
        
        # Calculate the overall 'Other Food' index (ignoring NaNs automatically)
        sub_cols = [c for c in final_df.columns if c != 'date']
        final_df['other_food_average'] = final_df[sub_cols].mean(axis=1)
        
        # Sort values just to be safe
        final_df.sort_values('date', inplace=True)
        
        final_df.to_csv(output_index_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ All 'Other Food' MoM calculations complete.")
        print(f"   Saved to: {output_index_file}")
        
        print("\nPreview of the aggregated average:")
        print(final_df[['date', 'other_food_average']].tail())
    else:
        print("No results generated.")

if __name__ == "__main__":
    main()