import pandas as pd
import glob
import os
import json
import unicodedata

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Processed_Food/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Processed_Food/cat_lookup_table.csv'

# --- KEYWORD MAPPING ---
SUB_MAP = {
    "54": [ # Bánh mì (Bread & Sandwiches)
        "bánh mì", "banh my", "sandwich", "sanwhich", "bánh sừng bò"
    ],
    
    "55": [ # Xúc xích - Thịt Nguội (Sausages & Cold Cuts)
        "xúc xích", "xx", "lạp xưởng", "lạp sườn",
        "thịt nguội", "ba rọi", "ba chỉ", "xông khói", "hun khói", "hong khói",
        "dăm bông", "jambong", "thăn lưng", "salami", "chân giò", "bắp bò", "gà tây",
        "thịt lợn hun khói", "gà muối", "tai heo muối"
    ],
    
    "56": [ # Bánh bao (Steamed Buns)
        "bánh bao" # Đã xóa "bb" để tránh nhầm với "BBQ"
    ],
    
    "57": [ # Kim chi (Kimchi)
        "kim chi"
    ],
    
    "58": [ # Thực Phẩm Chế Biến Khác (Other Processed Foods)
        # Các loại bánh ngọt ăn liền / đồ ngọt
        "bánh trứng", "karo", "bánh pía", "bánh cốm", "bánh bông lan", "dorayaki",
        "bánh phồng tôm", "bánh ngon", "bánh đậu", "thanh cơm lứt", "tráng", "bánh chưng",
        "bông lan",
        # Đồ ăn vặt / Mồi nhậu / Món ăn kèm
        "khô bò", "khô gà", "chà bông", "chân gà", "da cá", "nugget", "nem bùi", "bóng bì",
        "chả cốm", "măng muối", "gà xì dầu", "trà sữa", "thạch đen", "sữa bắp"
    ]
}

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    # Thêm dấu cách vào đầu và cuối để xử lý regex-like matching cho từ ngắn nếu cần
    # nhưng ở đây việc dùng "in" với từ khoá rõ ràng là đủ.
    return unicodedata.normalize('NFC', text).lower()

def get_subcategory(name, labels_dict):
    name_clean = normalize_text(name)
    
    # --- THỨ TỰ ƯU TIÊN LOGIC ---

    # 1. Bánh bao
    if any(normalize_text(k) in name_clean for k in SUB_MAP["56"]):
        return labels_dict.get("Label 56", "Bánh bao")

    # 2. Bánh mì
    if any(normalize_text(k) in name_clean for k in SUB_MAP["54"]):
        return labels_dict.get("Label 54", "Bánh mì")

    # 3. Kim chi
    if any(normalize_text(k) in name_clean for k in SUB_MAP["57"]):
        return labels_dict.get("Label 57", "Kim chi")

    # 4. Xúc xích - Thịt Nguội
    # Ưu tiên kiểm tra kỹ các loại thịt chế biến sẵn
    if any(normalize_text(k) in name_clean for k in SUB_MAP["55"]):
        return labels_dict.get("Label 55", "Xúc xích - Thịt Nguội")

    # 5. Các loại thực phẩm chế biến khác
    if any(normalize_text(k) in name_clean for k in SUB_MAP["58"]):
        return labels_dict.get("Label 58", "Thực Phẩm Chế Biến Khác")

    # 6. Fallback (Mặc định cho các món ăn liền chưa có từ khóa)
    return labels_dict.get("Label 58", "Thực Phẩm Chế Biến Khác")

def main():
    # 1. Load Labels
    labels_dict = {
        "Label 53": "Thực Phẩm Chế Biến",
        "Label 54": "Bánh mì",
        "Label 55": "Xúc xích - Thịt Nguội",
        "Label 56": "Bánh bao",
        "Label 57": "Kim chi",
        "Label 58": "Thực Phẩm Chế Biến Khác"
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
    master_df['parent_category'] = labels_dict.get("Label 53", "Thực Phẩm Chế Biến")

    # 5. Save
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Success! Saved to: {output_file}")
    
    # 6. Verification test
    print("\n--- Verification of Fixes (BBQ vs Bánh Bao) ---")
    test_items = ["bbq", "bánh bao", "kim chi", "vissan"]
    preview = master_df[master_df['product_name'].apply(lambda x: any(k in normalize_text(x) for k in test_items))]
    if not preview.empty:
        print(preview.head(10))

if __name__ == "__main__":
    main()