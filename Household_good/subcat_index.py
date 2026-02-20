import pandas as pd
import numpy as np
import glob
import os
import re
from scipy.stats import gmean

# --- CONFIGURATION ---
# Cập nhật đường dẫn cho Household_good
csv_folder = '/Users/my/Online Food Price/Household_good/CSV'
lookup_file = '/Users/my/Online Food Price/Household_good/cat_lookup_table.csv'
output_index_file = '/Users/my/Online Food Price/Household_good/jevons_price_index.csv'

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

    try:
        lookup = pd.read_csv(lookup_file, usecols=['product_name', 'subcategory'])
    except Exception as e:
        print(f"❌ Error reading lookup file: {e}")
        return
    
    # 2. Identify and Sort CSV Files
    files = sorted(glob.glob(os.path.join(csv_folder, '*.csv')))
    
    if not files:
        print(f"❌ No CSV files found in {csv_folder}")
        return

    history = {} 
    prev_df = None
    prev_date = None
    
    results = []

    for file in files:
        current_date = extract_date(os.path.basename(file))
        print(f"Processing: {current_date}")
        
        try:
            # Load Data
            curr_df = pd.read_csv(file, usecols=['product_name', 'final_price'])
            
            # Merge with Lookup
            curr_df = curr_df.merge(lookup, on='product_name', how='left')
            
            # Clean Data
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
                
                # Iterate through existing subcategories
                for sub in history.keys():
                    p_prev = prev_df[prev_df['subcategory'] == sub][['product_name', 'final_price']]
                    p_curr = curr_df[curr_df['subcategory'] == sub][['product_name', 'final_price']]
                    
                    matched = p_prev.merge(p_curr, on='product_name', suffixes=('_prev', '_curr'))
                    
                    # SAFETY CHECK: Filter out zero prices
                    matched = matched[(matched['final_price_prev'] > 0) & (matched['final_price_curr'] > 0)]

                    if not matched.empty:
                        # Jevons Index Formula
                        price_relatives = matched['final_price_curr'] / matched['final_price_prev']
                        chain_relative = gmean(price_relatives)
                        
                        # Update Index
                        prev_index = history[sub].get(prev_date, 1.0)
                        new_index = prev_index * chain_relative
                        history[sub][current_date] = new_index
                    else:
                        # Carry over previous index if no matches found
                        history[sub][current_date] = history[sub].get(prev_date, 1.0)
                    
                    day_results[sub] = history[sub][current_date]
                
                results.append(day_results)
                
            prev_df = curr_df
            prev_date = current_date
            
        except Exception as e:
            print(f"  ⚠️ Error processing file {file}: {e}")

    # 3. Final Output
    if results:
        final_df = pd.DataFrame(results)
        final_df.to_csv(output_index_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ Jevons Index calculated for Household Goods. Saved to: {output_index_file}")
        print(final_df.tail())
    else:
        print("No results generated.")

if __name__ == "__main__":
    main()