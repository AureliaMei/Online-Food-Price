import pandas as pd
import glob
import os
import json
import unicodedata

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Non-alcohol_beverage/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Non-alcohol_beverage/cat_lookup_table.csv'

# --- KEYWORD MAPPING (MINIMALIST & OPTIMIZED VERSION) ---
SUB_MAP = {
    "37": [ # Cà Phê
        "cà phê", "cafe", "café", "coffee", "nescafe", "vinacafe", "g7", 
        "highlands", "maccoffee", "wake up", "cappuccino", "đen đá", "sữa đá", 
        "mê trang", "mr.viet"
    ],
    
    "38": [ # Nước Suối (Nước khoáng / tinh khiết)
        "nước khoáng", "nước suối", "nước tinh khiết", "nước lọc",
        "lavie", "aquafina", "dasani", "vivant", "vĩnh hảo", "ion life", "th true water", "alba", "evian", "faith"
    ],
    
    "40": [ # Trà - Các Loại Khác (Trà, Yến, Kombucha, Sữa hạt/ngũ cốc...)
        "trà", "tea", "ô long", "o long", "lipton", "cozy", "dilmah", "fuzetea", "fuze tea", "c2",
        "tổ yến", "nước yến", "yến sào", "yến việt", "nest iq", "song yến", "thiên việt",
        "kombucha", "cacao", "ca cao", "milo", "matcha", "sâm bí đao", "nha đam", "ovaltine",
        "ngũ cốc", "gạo lức", "gạo lứt", "trân châu" # Đưa ngũ cốc và topping trà sữa vào đây
    ],
    
    "39": [ # Nước Ngọt (Nước có ga, Nước trái cây, Tăng lực, Thể thao)
        "nước ngọt", "nước giải khát", "nước uống", "soda",
        "coca", "coca-cola", "pepsi", "sprite", "fanta", "7up", "mirinda", "thanh yên",
        "sting", "red bull", "redbull", "bò húc", "tăng lực", "monster", "number 1", "warrior", "rockstar", "thums up", "247",
        "aquarius", "revive", "nutri boost", "nutriboost", "pocari",
        "nước ép", "nước trái cây", "nước cam", "nước táo", "nước dừa", "nước chanh", "nước nho", "nước đào",
        "teppy", "pororo", "twister", "vfresh", "th true juice", "pushmax", "jele", "gumi", "latte", "good mood", "thaicoco", "cocoxim", "c-vitt"
    ]
}

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    return unicodedata.normalize('NFC', text).lower()

def get_subcategory(name, labels_dict):
    name_clean = normalize_text(name)
    
    # --- LOGIC ƯU TIÊN (CRITICAL ORDER) ---

    # 1. Cà Phê
    if any(normalize_text(k) in name_clean for k in SUB_MAP["37"]):
        return labels_dict.get("Label 37", "Cà Phê")

    # 2. Nước Suối
    if any(normalize_text(k) in name_clean for k in SUB_MAP["38"]):
        return labels_dict.get("Label 38", "Nước Suối")

    # 3. Trà - Các Loại Khác
    if any(normalize_text(k) in name_clean for k in SUB_MAP["40"]):
        return labels_dict.get("Label 40", "Trà - Các Loại Khác")

    # 4. Nước Ngọt
    if any(normalize_text(k) in name_clean for k in SUB_MAP["39"]):
        return labels_dict.get("Label 39", "Nước Ngọt")

    # 5. Mặc định (Fallback)
    return labels_dict.get("Label 39", "Nước Ngọt")

def main():
    # 1. Load Labels
    labels_dict = {
        "Label 36": "Đồ Uống - Giải Khát",
        "Label 37": "Cà Phê",
        "Label 38": "Nước Suối",
        "Label 39": "Nước Ngọt",
        "Label 40": "Trà - Các Loại Khác"
    }
    
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

    print("Combining and cleaning data...")
    master_df = pd.concat(all_names, ignore_index=True)
    master_df = master_df.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    
    print("Categorizing products...")
    master_df['subcategory'] = master_df['product_name'].apply(lambda x: get_subcategory(x, labels_dict))
    master_df['parent_category'] = labels_dict.get("Label 36", "Đồ Uống - Giải Khát")

    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Success! Saved to: {output_file}")
    
    # Verification Preview
    print("\n--- Verification of Edge Cases ---")
    test_items = ["café", "ca cao", "ngũ cốc", "trân châu", "coca", "yến"]
    preview = master_df[master_df['product_name'].apply(lambda x: any(k in normalize_text(x) for k in test_items))]
    if not preview.empty:
        print(preview.head(15))
    else:
        print("No matching items found for verification.")

if __name__ == "__main__":
    main()