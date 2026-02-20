import pandas as pd
import numpy as np
import glob
import os
import re
from scipy.stats import gmean

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Baby_product/CSV'
lookup_file = '/Users/my/Online Food Price/Baby_product/cat_lookup_table.csv'
output_index_file = '/Users/my/Online Food Price/Baby_product/jevons_price_index.csv'

def extract_date(filename):
    # Regex to find date patterns like YYYY-MM-DD or YYYYMMDD
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    return match.group(0) if match else filename

def main():
    # 1. Load Lookup Table
    lookup = pd.read_csv(lookup_file, usecols=['product_name', 'subcategory'])
    
    # 2. Identify and Sort CSV Files by Date
    files = sorted(glob.glob(os.path.join(csv_folder, '*.csv')))
    
    # Storage for historical indices (Day 0 starts at 1.0)
    # Format: {subcategory: {date: index_value}}
    history = {} 
    # To store the previous day's data for comparison
    prev_df = None
    prev_date = None
    
    results = []

    for file in files:
        current_date = extract_date(os.path.basename(file))
        print(f"Processing: {current_date}")
        
        # Load current day data and merge with subcategories
        curr_df = pd.read_csv(file, usecols=['product_name', 'final_price'])
        curr_df = curr_df.merge(lookup, on='product_name', how='left')
        
        # Drop rows where subcategory is unknown or price is missing
        curr_df = curr_df.dropna(subset=['subcategory', 'final_price'])
        
        # If it's the first file, initialize everything to 1.0
        if prev_df is None:
            day_results = {'date': current_date}
            subcategories = curr_df['subcategory'].unique()
            for sub in subcategories:
                history[sub] = {current_date: 1.0}
                day_results[sub] = 1.0
            results.append(day_results)
        else:
            day_results = {'date': current_date}
            # Calculate index for each subcategory
            for sub in history.keys():
                # Get matched pairs (products existing in both days for this subcategory)
                p_prev = prev_df[prev_df['subcategory'] == sub][['product_name', 'final_price']]
                p_curr = curr_df[curr_df['subcategory'] == sub][['product_name', 'final_price']]
                
                matched = p_prev.merge(p_curr, on='product_name', suffixes=('_prev', '_curr'))
                
                if not matched.empty:
                    # Jevons Index: Geometric mean of (Price_curr / Price_prev)
                    price_relatives = matched['final_price_curr'] / matched['final_price_prev']
                    # Calculate chain relative
                    chain_relative = gmean(price_relatives)
                    
                    # New Index = Previous Day Index * Chain Relative
                    new_index = history[sub][prev_date] * chain_relative
                    history[sub][current_date] = new_index
                else:
                    # If no matched products, carry over previous index
                    history[sub][current_date] = history[sub][prev_date]
                
                day_results[sub] = history[sub][current_date]
            
            results.append(day_results)
            
        prev_df = curr_df
        prev_date = current_date

    # 3. Final Formatting
    final_df = pd.DataFrame(results)
    final_df.to_csv(output_index_file, index=False, encoding='utf-8-sig')
    print(f"\nJevons Index calculation complete. Saved to {output_index_file}")
    print(final_df.tail())

if __name__ == "__main__":
    main()