import pandas as pd
import glob
import os
import json

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Baby_product/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Baby_product/cat_lookup_table.csv'

# Keeping your exact keywords and filtering logic
SUB_MAP = {
    "70": ["sữa bột", "dinh dưỡng", "vani", "ăn dặm", "bột", "hộp", "sôcôla"], 
    "71": ["tã", "bỉm", "tã quần", "tã dán", "lót"],                
    "72": ["tắm", "gội", "phấn", "thân"]     
}
CATCH_ALL_BABY = "73" 

def get_subcategory(name, labels_dict):
    name_lower = str(name).lower()
    for code, keywords in SUB_MAP.items():
        if any(word in name_lower for word in keywords):
            return labels_dict.get(f"Label {code}", f"Label {code}")
    return labels_dict.get(f"Label {CATCH_ALL_BABY}", "Chăm Sóc Cá Nhân Cho Bé")

def main():
    # Load JSON Labels
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            labels_list = json.load(f)
            labels_dict = labels_list[0]
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return

    csv_files = glob.glob(os.path.join(csv_folder, '*.csv'))
    all_names = []

    print(f"Reading {len(csv_files)} files for unique products...")
    for file in csv_files:
        try:
            # We only read the product_name column to save memory
            df = pd.read_csv(file, encoding='utf-8-sig', usecols=['product_name'])
            all_names.append(df)
        except Exception as e:
            print(f"Skipping {file}: {e}")

    # Combine all names
    master_df = pd.concat(all_names, ignore_index=True)

    # --- THE DEDUPLICATION STEP ---
    # This removes exact duplicates of product names
    initial_count = len(master_df)
    master_df = master_df.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    final_count = len(master_df)
    
    print(f"Removed {initial_count - final_count} duplicate rows.")

    # Apply Categorization
    print("Mapping unique products to subcategories...")
    master_df['subcategory'] = master_df['product_name'].apply(lambda x: get_subcategory(x, labels_dict))
    master_df['parent_category'] = labels_dict.get("Label 69", "Chăm Sóc Bé")

    # Save final lookup table
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\nSuccess! Lookup table created with {final_count} unique items.")
    print(f"File saved to: {output_file}")
    
    # Display preview
    print("\nLookup Table Sample:")
    print(master_df.head(10))

if __name__ == "__main__":
    main()