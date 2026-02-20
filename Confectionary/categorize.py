import pandas as pd
import glob
import os
import json
import unicodedata

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Confectionary/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Confectionary/cat_lookup_table.csv'

# --- KEYWORD MAPPING ---
SUB_MAP = {
    "31": [ # Kẹo - Chocolate
        "kẹo", "socola", "chocolate", "sô cô la", "scl", "chobisca",
        "thạch", "jelly", "marshmallow", "marsmallows", "gum", "xylitol", "mentos", "tictac"
    ],
    
    "32": [ # Bánh Snack
        "snack", "khoai tây", "pringles", "lay", "ostar", "mực tẩm", "bento",
        "bánh que", "marine boy", "doakbua", "akiko", "bim bim", "swing",
        "doritos", "karamucho", "talaethong"
    ],
    
    "33": [ # Hạt - Trái Cây Sấy Khô 
        "ô mai ", "sấy", "nho khô", "hướng dương", "hạt bí", "hạt sen",
        "chà là", "mứt", "trái cây khô", "hạt điều", "đậu phộng", "đậu tỏi", "hạnh nhân", 
        "hạt dẻ", "macca", "macadamia", "óc chó", "bò khô", "khô bò", "yến nhung"
    ],
    
    "30": [ # Bánh Xốp - Bánh Quy (Và các loại bánh ngọt khác)
        "bánh quy", "bánh xốp", "bánh gạo", "chocopie", "custas", "bánh quế", 
        "bánh bông lan", "solite", "bánh trứng", "tipo", "bánh dừa", "mochi", 
        "bánh", "gouté", "danisa", "cosy", "oreo", "afc", "kenju", "bắp chiên"
    ]
}

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    return " " + unicodedata.normalize('NFC', text).lower() + " "

def get_subcategory(name, labels_dict):
    name_clean = normalize_text(name)
    
    # 0. Loại bỏ rác
    if "kem đánh răng" in name_clean:
        return "Bỏ qua (Lỗi Dữ Liệu)"

    # --- THỨ TỰ ƯU TIÊN LOGIC ---

    # 1. Kẹo - Chocolate
    if any(normalize_text(k) in name_clean for k in SUB_MAP["31"]):
        return labels_dict.get("Label 31", "Kẹo - Chocolate")

    # 2. Bánh Snack 
    if any(normalize_text(k) in name_clean for k in SUB_MAP["32"]):
        return labels_dict.get("Label 32", "Bánh Snack")

    # 3. Hạt - Trái cây sấy khô & Khô bò
    if any(normalize_text(k) in name_clean for k in SUB_MAP["33"]):
        return labels_dict.get("Label 33", "Hạt - Trái Cây Sấy Khô")

    # 4. Bánh Xốp - Bánh Quy
    if any(normalize_text(k) in name_clean for k in SUB_MAP["30"]):
        return labels_dict.get("Label 30", "Bánh Xốp - Bánh Quy")

    # 5. Mặc định (Fallback)
    return labels_dict.get("Label 30", "Bánh Xốp - Bánh Quy")

def main():
    labels_dict = {
        "Label 29": "Bánh Kẹo",
        "Label 30": "Bánh Xốp - Bánh Quy",
        "Label 31": "Kẹo - Chocolate",
        "Label 32": "Bánh Snack",
        "Label 33": "Hạt - Trái Cây Sấy Khô"
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
    
    # Lọc bỏ rác
    master_df = master_df[master_df['subcategory'] != "Bỏ qua (Lỗi Dữ Liệu)"]
    master_df['parent_category'] = labels_dict.get("Label 29", "Bánh Kẹo")

    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ Success! Saved to: {output_file}")

if __name__ == "__main__":
    main()