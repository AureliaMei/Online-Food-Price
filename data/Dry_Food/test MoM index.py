import pandas as pd
import numpy as np
import glob
import os
import re
from scipy.stats import gmean

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Dry_Food/CSV'
lookup_file = '/Users/my/Online Food Price/Dry_Food/cat_lookup_table.csv'
# Updated output name to reflect the MoM calculation
output_index_file = '/Users/my/Online Food Price/Dry_Food/mom_price_change.csv' 

def extract_date(filename):
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    return match.group(0) if match else filename

def main():
    if not os.path.exists(lookup_file):
        print(f"❌ Lookup file not found: {lookup_file}")
        return

    try:
        lookup = pd.read_csv(lookup_file, usecols=['product_name', 'subcategory'])
    except Exception as e:
        print(f"❌ Error reading lookup file: {e}")
        return
    
    # Define our exact targets
    target_subs = ['Gạo - Nông Sản Khô', 'Ngũ Cốc - Yến Mạch']
    
    files = sorted(glob.glob(os.path.join(csv_folder, '*.csv')))
    if not files:
        print(f"❌ No CSV files found in {csv_folder}")
        return

    # Dictionary to store all daily dataframes: {'2026-01-28': df, '2026-01-29': df, ...}
    historical_dfs = {} 
    results = []

    for file in files:
        current_date = extract_date(os.path.basename(file))
        print(f"Processing: {current_date}")
        
        try:
            # 1. Load and filter current day data
            curr_df = pd.read_csv(file, usecols=['product_name', 'final_price'])
            curr_df = curr_df.merge(lookup, on='product_name', how='left')
            
            # Keep ONLY our target staples
            curr_df = curr_df[curr_df['subcategory'].isin(target_subs)]
            curr_df = curr_df.dropna(subset=['subcategory', 'final_price'])
            
            # Store it in memory for future months to reference
            historical_dfs[current_date] = curr_df
            
            # 2. Determine the exact date one month ago
            past_date_obj = pd.to_datetime(current_date) - pd.DateOffset(months=1)
            past_date_str = past_date_obj.strftime('%Y-%m-%d')
            
            day_results = {'date': current_date}
            
            # 3. Calculate MoM Jevons ratio
            for sub in target_subs:
                # If we have data from exactly one month ago
                if past_date_str in historical_dfs:
                    past_df = historical_dfs[past_date_str]
                    
                    p_past = past_df[past_df['subcategory'] == sub][['product_name', 'final_price']]
                    p_curr = curr_df[curr_df['subcategory'] == sub][['product_name', 'final_price']]
                    
                    matched = p_past.merge(p_curr, on='product_name', suffixes=('_past', '_curr'))
                    matched = matched[(matched['final_price_past'] > 0) & (matched['final_price_curr'] > 0)]

                    if not matched.empty:
                        price_relatives = matched['final_price_curr'] / matched['final_price_past']
                        # Calculate the MoM ratio (e.g., 1.02 means a 2% increase from last month)
                        day_results[sub] = gmean(price_relatives)
                    else:
                        day_results[sub] = np.nan # No overlapping products
                else:
                    # Output NaN if the scraper didn't run on this day last month
                    # (e.g., during the first month of data collection)
                    day_results[sub] = np.nan 
            
            results.append(day_results)
            
        except Exception as e:
            print(f"  ⚠️ Error processing file {file}: {e}")

    if results:
        final_df = pd.DataFrame(results)
        final_df.to_csv(output_index_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ MoM Index calculation complete.")
        print(f"   Saved to: {output_index_file}")
        print("\nPreview of the data:")
        print(final_df.tail())
    else:
        print("No results generated.")

if __name__ == "__main__":
    main()