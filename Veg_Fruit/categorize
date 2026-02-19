import pandas as pd
import glob
import os
import json
import unicodedata

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Veg_Fruit/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Veg_Fruit/cat_lookup_table.csv'

# --- KEYWORD MAPPING ---
# --- KEYWORD MAPPING (UPDATED) ---
SUB_MAP = {
    "10": [ # Trái cây tươi
        "cam", "quất", "chanh", "xoài", "dưa hấu", "dưa lưới", "dưa lê", 
        "thanh long", "chôm chôm", "hồng xiêm", "sapo", "kiwi", "chuối", 
        "bưởi", "nho", "lê", "táo", "dứa", "khóm", "mận", "việt quất", 
        "dâu", "chà là", "dừa xiêm", "dừa tiện lợi", "cherry", "đu đủ", "ổi" # Bổ sung Dâu, Cherry, Đu đủ, Ổi
    ],
    
    "8": [ # Rau Lá
        "cải", "rau", "xà lách", "giá đỗ", "hẹ lá", "hành lá", 
        "cần tây", "cần nước", "ngọn", "lá", "húng", "mùi tàu", "mùi ta", "ngò", "dọc mùng" # Bổ sung Cần nước, Mùi ta, Ngò
    ],
    
    "9": [ # Củ, Quả, Nấm
        "nấm", "măng", 
        "su hào", "bí", "khoai", "củ cải", "su su", "cà tím", "ngô", "đậu bắp", "đậu cove", "cà rốt",
        "hành củ", "hành lý sơn", "tỏi", "củ gừng", "củ sả", "củ nghệ", "củ riềng", "ớt",
        "hạt sen", "thực phẩm hỗn hợp", "cà chua"
    ]
}

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    return unicodedata.normalize('NFC', text).lower()

def get_subcategory(name, labels_dict):
    name_clean = normalize_text(name)
    
    # --- LOGIC ƯU TIÊN ---

    # 1. Trái cây tươi
    # Lưu ý: check "chanh" phải cẩn thận không nhầm với "khô gà lá chanh" nhưng vì đây là thư mục rau quả nên khá an toàn.
    if any(normalize_text(k) in name_clean for k in SUB_MAP["10"]):
        return labels_dict.get("Label 10", "Trái cây tươi")

    # 2. Rau Lá
    # Lưu ý: "Bắp cải" chứa chữ "cải" sẽ rơi vào đây, điều này là chính xác.
    if any(normalize_text(k) in name_clean for k in SUB_MAP["8"]):
        return labels_dict.get("Label 8", "Rau Lá")

    # 3. Củ, Quả (và Nấm/Măng)
    if any(normalize_text(k) in name_clean for k in SUB_MAP["9"]):
        return labels_dict.get("Label 9", "Củ, Quả")

    # 4. Mặc định (Fallback)
    # Phần lớn các món rau củ khó phân loại sẽ rơi vào nhóm Củ Quả.
    return labels_dict.get("Label 9", "Củ, Quả")

def main():
    # 1. Load Labels
    labels_dict = {
        "Label 7": "Rau - Củ - Trái Cây",
        "Label 8": "Rau Lá",
        "Label 9": "Củ, Quả",
        "Label 10": "Trái cây tươi"
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

    # 3. Combine and Clean
    print("Combining and cleaning data...")
    master_df = pd.concat(all_names, ignore_index=True)
    master_df = master_df.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    
    # 4. Categorize
    print("Categorizing products...")
    master_df['subcategory'] = master_df['product_name'].apply(lambda x: get_subcategory(x, labels_dict))
    master_df['parent_category'] = labels_dict.get("Label 7", "Rau - Củ - Trái Cây")

    # 5. Save
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Success! Saved to: {output_file}")
    
    # 6. Verification
    print("\n--- Verification Preview ---")
    test_items = ["su hào", "cải", "nấm", "táo", "xoài", "hành", "bí đỏ"]
    preview = master_df[master_df['product_name'].apply(lambda x: any(k in normalize_text(x) for k in test_items))]
    if not preview.empty:
        print(preview.head(15))

if __name__ == "__main__":
    main()