import pandas as pd
import glob
import os
import json

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Electronics/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Electronics/cat_lookup_table.csv'

def main():
    # 1. Load JSON Labels (Optional here since we have one category, but kept for consistency)
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            labels_list = json.load(f)
            labels_dict = labels_list[0]
    except Exception as e:
        print(f"Note: Could not load JSON ({e}), using default labels.")
        labels_dict = {}

    # 2. Read CSV Files
    if not os.path.exists(csv_folder):
        print(f"❌ Error: Folder not found at {csv_folder}")
        return

    csv_files = glob.glob(os.path.join(csv_folder, '*.csv'))
    all_names = []

    print(f"Reading {len(csv_files)} files...")
    for file in csv_files:
        try:
            df = pd.read_csv(file, encoding='utf-8-sig', usecols=['product_name'])
            all_names.append(df)
        except Exception as e:
            print(f"Skipping {file}: {e}")

    if not all_names:
        print("No data found.")
        return

    # 3. Combine and Deduplicate
    master_df = pd.concat(all_names, ignore_index=True)
    initial_count = len(master_df)
    master_df = master_df.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    
    print(f"Removed {initial_count - len(master_df)} duplicates.")

    # 4. Apply Categorization (One Big Category)
    print("Assigning category...")
    
    # Since it's all one category, we hardcode it.
    # You can change "Máy nước nóng" to "Electronics" if you prefer broader naming.
    master_df['subcategory'] = "Máy nước nóng"
    master_df['parent_category'] = "Electronics"

    # 5. Save
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Success! Lookup table created for {len(master_df)} products.")
    print(f"   Saved to: {output_file}")
    print(master_df.head())

if __name__ == "__main__":
    main()