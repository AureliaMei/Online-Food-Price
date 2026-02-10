import pandas as pd
import numpy as np
import glob
import os
import re
from scipy.stats import gmean

# --- CONFIGURATION ---
# Updated paths for Dry Food
csv_folder = '/Users/my/Online Food Price/Dry_Food/CSV'
lookup_file = '/Users/my/Online Food Price/Dry_Food/cat_lookup_table.csv'
output_index_file = '/Users/my/Online Food Price/Dry_Food/jevons_price_index.csv'

def extract_date(filename):
    # Regex to find date patterns like YYYY-MM-DD
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    return match.group(0) if match else filename

def main():
    # 1. Load Lookup Table
    if not os.path.exists(lookup_file):
        print(f"❌ Lookup file not found: {lookup_file}")
        print("   Please run the categorization script first.")
        return

    # Loading product_name and subcategory
    try:
        lookup = pd.read_csv(lookup_file, usecols=['product_name', 'subcategory'])
    except Exception as e:
        print(f"❌ Error reading lookup file: {e}")
        return
    
    # 2. Identify and Sort CSV Files by Date
    files = sorted(glob.glob(os.path.join(csv_folder, '*.csv')))
    
    if not files:
        print(f"❌ No CSV files found in {csv_folder}")
        return

    # Storage for historical indices (Day 0 starts at 1.0)
    history = {} 
    prev_df = None
    prev_date = None
    
    results = []

    for file in files:
        current_date = extract_date(os.path.basename(file))
        print(f"Processing: {current_date}")
        
        try:
            # Load current day data
            curr_df = pd.read_csv(file, usecols=['product_name', 'final_price'])
            
            # Merge with lookup to get subcategories (Gạo, Ngũ cốc, etc.)
            curr_df = curr_df.merge(lookup, on='product_name', how='left')
            
            # Drop rows where subcategory is unknown or price is missing
            curr_df = curr_df.dropna(subset=['subcategory', 'final_price'])
            
            # --- DAY 0 INITIALIZATION ---
            if prev_df is None:
                day_results = {'date': current_date}
                subcategories = curr_df['subcategory'].unique()
                for sub in subcategories:
                    history[sub] = {current_date: 1.0}
                    day_results[sub] = 1.0
                results.append(day_results)
            
            # --- SUBSEQUENT DAYS ---
            else:
                day_results = {'date': current_date}
                
                # Iterate over subcategories that exist in our history
                for sub in history.keys():
                    # Get matched pairs (products existing in both days for this subcategory)
                    p_prev = prev_df[prev_df['subcategory'] == sub][['product_name', 'final_price']]
                    p_curr = curr_df[curr_df['subcategory'] == sub][['product_name', 'final_price']]
                    
                    matched = p_prev.merge(p_curr, on='product_name', suffixes=('_prev', '_curr'))
                    
                    # SAFETY CHECK: Filter out zero prices to prevent DivisionByZero errors
                    matched = matched[(matched['final_price_prev'] > 0) & (matched['final_price_curr'] > 0)]

                    if not matched.empty:
                        # Jevons Index Formula: Geometric mean of price relatives
                        price_relatives = matched['final_price_curr'] / matched['final_price_prev']
                        
                        # Calculate chain relative (daily change)
                        chain_relative = gmean(price_relatives)
                        
                        # New Index = Previous Day Index * Chain Relative
                        prev_index = history[sub].get(prev_date, 1.0)
                        new_index = prev_index * chain_relative
                        history[sub][current_date] = new_index
                    else:
                        # If no matched products, carry over previous index (Flat line)
                        history[sub][current_date] = history[sub].get(prev_date, 1.0)
                    
                    day_results[sub] = history[sub][current_date]
                
                results.append(day_results)
                
            prev_df = curr_df
            prev_date = current_date
            
        except Exception as e:
            print(f"  ⚠️ Error processing file {file}: {e}")

    # 3. Final Formatting
    if results:
        final_df = pd.DataFrame(results)
        final_df.to_csv(output_index_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ Jevons Index calculation complete.")
        print(f"   Saved to: {output_index_file}")
        print("\nPreview of last 5 days:")
        print(final_df.tail())
    else:
        print("No results generated.")

if __name__ == "__main__":
    main()