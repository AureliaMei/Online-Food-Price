import pandas as pd
import numpy as np
import glob
import os
import re
from scipy.stats import gmean

# --- CONFIGURATION (Cấu hình cho Confectionary) ---
csv_folder = '/Users/my/Online Food Price/Confectionary/CSV'
lookup_file = '/Users/my/Online Food Price/Confectionary/cat_lookup_table.csv'
output_index_file = '/Users/my/Online Food Price/Confectionary/jevons_price_index.csv'

def extract_date(filename):
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    return match.group(0) if match else filename

def main():
    # 1. Load Lookup Table
    if not os.path.exists(lookup_file):
        print(f"❌ Lookup file not found: {lookup_file}")
        return

    try:
        lookup = pd.read_csv(lookup_file, usecols=['product_name', 'subcategory'])
        lookup = lookup.drop_duplicates(subset=['product_name'], keep='last')
    except Exception as e:
        print(f"❌ Error reading lookup file: {e}")
        return
    
    # 2. Identify CSV Files
    files = sorted(glob.glob(os.path.join(csv_folder, '*.csv')))
    if not files:
        print(f"❌ No CSV files found in {csv_folder}")
        return

    history = {} 
    prev_df = None
    prev_date = None
    results = []

    print(f"Found {len(files)} files. Calculating Jevons index for Confectionary...")

    for file in files:
        current_date = extract_date(os.path.basename(file))
        print(f"Processing: {current_date}")
        
        try:
            curr_df = pd.read_csv(file, usecols=['product_name', 'final_price'])
            curr_df = curr_df.merge(lookup, on='product_name', how='left')
            curr_df = curr_df.dropna(subset=['subcategory', 'final_price'])
            
            # --- BASE PERIOD ---
            if prev_df is None:
                day_results = {'date': current_date}
                for sub in curr_df['subcategory'].unique():
                    history[sub] = {current_date: 1.0}
                    day_results[sub] = 1.0
                results.append(day_results)
            
            # --- SUBSEQUENT DAYS ---
            else:
                day_results = {'date': current_date}
                
                for sub in history.keys():
                    p_prev = prev_df[prev_df['subcategory'] == sub][['product_name', 'final_price']]
                    p_curr = curr_df[curr_df['subcategory'] == sub][['product_name', 'final_price']]
                    
                    matched = p_prev.merge(p_curr, on='product_name', suffixes=('_prev', '_curr'))
                    matched = matched[(matched['final_price_prev'] > 0) & (matched['final_price_curr'] > 0)]

                    if not matched.empty:
                        price_relatives = matched['final_price_curr'] / matched['final_price_prev']
                        chain_relative = gmean(price_relatives)
                        new_index = history[sub].get(prev_date, 1.0) * chain_relative
                        history[sub][current_date] = new_index
                    else:
                        history[sub][current_date] = history[sub].get(prev_date, 1.0)
                    
                    day_results[sub] = history[sub][current_date]
                
                # Check for new subcategories
                for sub in curr_df['subcategory'].unique():
                    if sub not in history:
                        history[sub] = {current_date: 1.0}
                        day_results[sub] = 1.0

                results.append(day_results)
                
            prev_df = curr_df
            prev_date = current_date
            
        except Exception as e:
            print(f"  ⚠️ Error processing file {file}: {e}")

    # 3. Export Output
    if results:
        final_df = pd.DataFrame(results)
        cols = ['date'] + sorted([c for c in final_df.columns if c != 'date'])
        final_df = final_df[cols]
        final_df.to_csv(output_index_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ Jevons Index calculated successfully. Saved to: {output_index_file}")
        print(final_df.tail())
    else:
        print("No results generated.")

if __name__ == "__main__":
    main()