import pandas as pd
import glob
import os
import json
import unicodedata

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Instant_food/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Instant_food/cat_lookup_table.csv'

# --- KEYWORD MAPPING ---
SUB_MAP = {
    "44": [ # Cháo
        "cháo", "soup", "súp", "chao to yen", "chao thit"
    ],
    
    "45": [ # Phở - Bún
        "phở", "bún", "bun bo", "bun rieu", "pho bo", "pho ga"
    ],
    
    "43": [ # Miến - Hủ Tíu - Bánh Canh
        "miến", "hủ tíu", "hủ tiếu", "bánh canh", "bánh đa", "mien dong"
    ],
    
    "42": [ # Mì (Gồm cả Nui, Tokpokki, Pasta)
        "mì", "mỳ", "nui", "spaghetti", "pasta", 
        "tokpokki", "topokki", "bánh gạo", # Tokpokki đưa vào nhóm này
        "ramen", "udon", "yakisoba", "kimchi", 
        "omachi", "kokomi", "hảo hảo", "vifon", "acecook", "indomie", "koreno", "meizan"
    ]
}

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    return unicodedata.normalize('NFC', text).lower()

def get_subcategory(name, labels_dict):
    name_clean = normalize_text(name)
    
    # --- LOGIC ƯU TIÊN ---

    # 1. Cháo (Rất rõ ràng, tách trước)
    if any(normalize_text(k) in name_clean for k in SUB_MAP["44"]):
        return labels_dict.get("Label 44", "Cháo")

    # 2. Phở - Bún
    if any(normalize_text(k) in name_clean for k in SUB_MAP["45"]):
        return labels_dict.get("Label 45", "Phở - Bún")

    # 3. Miến - Hủ Tíu - Bánh Canh
    if any(normalize_text(k) in name_clean for k in SUB_MAP["43"]):
        return labels_dict.get("Label 43", "Miến - Hủ Tíu - Bánh Canh")

    # 4. Mì (Nhóm chung cho Mì, Nui, Tokpokki...)
    if any(normalize_text(k) in name_clean for k in SUB_MAP["42"]):
        return labels_dict.get("Label 42", "Mì")

    # 5. Mặc định (Nếu không tìm thấy từ khóa, gán vào Mì - nhóm phổ biến nhất)
    return labels_dict.get("Label 42", "Mì")

def main():
    # 1. Load Labels (Giả lập)
    labels_dict = {
        "Label 41": "Mì - Thực Phẩm Ăn Liền",
        "Label 42": "Mì",
        "Label 43": "Miến - Hủ Tíu - Bánh Canh",
        "Label 44": "Cháo",
        "Label 45": "Phở - Bún"
    }
    
    # 2. Read CSV Files
    if not os.path.exists(csv_folder):
        print(f"Error: Folder not found at {csv_folder}")
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
    print("Combining and cleaning data...")
    master_df = pd.concat(all_names, ignore_index=True)
    master_df = master_df.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    
    # 4. Apply Categorization
    print("Categorizing products...")
    master_df['subcategory'] = master_df['product_name'].apply(lambda x: get_subcategory(x, labels_dict))
    master_df['parent_category'] = labels_dict.get("Label 41", "Mì - Thực Phẩm Ăn Liền")

    # 5. Save
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\nSuccess! Saved to: {output_file}")
    
    # 6. Verification Preview
    print("\n--- Verification of Instant Food ---")
    test_items = ["tokpokki", "bánh gạo", "nui", "cháo", "bún bò", "phở", "mì trứng"]
    preview = master_df[master_df['product_name'].apply(lambda x: any(k in normalize_text(x) for k in test_items))]
    if not preview.empty:
        print(preview.head(15))
    else:
        print("No matching items found for verification.")

if __name__ == "__main__":
    main()