import pandas as pd
import glob
import os
import json
import unicodedata

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Hygene/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Hygene/cat_lookup_table.csv'

# --- KEYWORD MAPPING (UPDATED) ---
SUB_MAP = {
    "19": [ # Răng Miệng (Dental)
        "kem đánh răng", "bàn chải", "nước súc miệng", "chỉ nha khoa", 
        "tăm nha khoa", "kdr", "trắng răng", "súc miệng", "tăm nước",
        "colgate", "p/s", "closeup", "sensodyne", "listerine", "oral-b", "darlie",
        "close up", "lipzo", "mondahmin", "sparkle", "oral clean"
    ],
    
    "20": [ # Chăm Sóc Da (Skincare)
        "sữa rửa mặt", "kem rửa mặt", "gel rửa mặt", "bọt rửa mặt",
        "kem dưỡng", "dưỡng thể", "lotion", "serum", "toner", "nước hoa hồng",
        "mặt nạ", "mask", "tẩy tế bào chết", "tẩy da chết", "peeling",
        "chống nắng", "sunplay", "tẩy trang", "trị mụn", "lột mụn", "xịt khoáng",
        "senka", "acnes", "pond's", "biore", "hazzeline", "vaseline", "nivea", 
        "simple", "cocoon", "garnier", "hatomugi", "hada labo", "neutrogena", "l'oreal"
    ],
    
    "21": [ # Chăm Sóc Tóc (Hair)
        "dầu gội", "dầu xả", "kem xả", "kem ủ", "ủ tóc", "dưỡng tóc", 
        "nhuộm tóc", "gel tạo kiểu", "wax", "vuốt tóc", "bọt tạo kiểu",
        "tresemme", "pantene", "sunsilk", "head & shoulder", "head&shoulder",
        "clear", "romano", "x-men", "nguyên xuân", "double rich", "rejoice",
        "oliv", "lashe", "ogx", "kerasys", "bigen", "selsun"
    ],
    
    "22": [ # Chăm Sóc Phụ Nữ (Feminine)
        "băng vệ sinh", "bvs", "dung dịch vệ sinh phụ nữ", 
        "kotex", "diana", "laurier", "uucare", "lactacyd", "sofy"
        # REMOVED: "sensi" to avoid conflict with "sensitive" in other categories
    ],
    
    "23": [ # Cá Nhân Khác (General Personal Care)
        # Keywords used in priority check
        "sữa tắm", "tắm gội", "xà bông", "xà phòng", "nước rửa tay", "gel rửa tay", "muối tắm",
        "lăn khử mùi", "xịt khử mùi", "ngăn mùi", "khử mùi", "xịt toàn thân", "sáp khử mùi",
        "cạo râu", "dao cạo", "bọt cạo", "gillette", "lưỡi dao",
        "khăn giấy", "giấy vệ sinh", "khăn ướt", "giấy ăn", "giấy rút", 
        "bông tẩy trang", "tăm bông", "bông trang điểm", "bông tai", "khẩu trang",
        "bao cao su", "durex", "tesori", "purite", "on the body"
    ]
}

def normalize_text(text):
    if not isinstance(text, str):
        return str(text)
    return unicodedata.normalize('NFC', text).lower()

def get_subcategory(name, labels_dict):
    name_clean = normalize_text(name)
    
    # --- LOGIC ƯU TIÊN (CRITICAL ORDER) ---

    # 1. Chăm Sóc Phụ Nữ (Đặc thù nhất)
    # Check trước tiên vì từ khóa rất riêng biệt (Kotex, Diana...)
    if any(normalize_text(k) in name_clean for k in SUB_MAP["22"]):
        return labels_dict.get("Label 22", "Chăm Sóc Phụ Nữ")

    # 2. Chăm Sóc Răng Miệng
    # Check tiếp theo vì ít trùng lặp
    if any(normalize_text(k) in name_clean for k in SUB_MAP["19"]):
        return labels_dict.get("Label 19", "Chăm Sóc Răng Miệng")

    # 3. Sàng lọc Nhóm 23 (Priority Check) - BƯỚC QUAN TRỌNG NHẤT
    # Phải bắt Sữa tắm, Dao cạo, Bông tẩy trang... TẠI ĐÂY
    # Để tránh việc "Sữa tắm Dove" bị rơi vào nhóm Tóc (do có chữ Dove)
    # Hoặc "Dao cạo Sensitive" bị rơi lung tung.
    priority_keywords_23 = [
        "bông tẩy trang", "tăm bông", "khăn ướt", "khăn giấy", "giấy vệ sinh", "giấy ăn",
        "sữa tắm", "tắm gội", "xà bông", "xà phòng", "muối tắm", "nước rửa tay",
        "dao cạo", "cạo râu", "bọt cạo", "lưỡi dao",
        "bao cao su", "khẩu trang", "băng cá nhân",
        "lăn khử mùi", "lăn ngăn mùi", "xịt khử mùi", "xịt ngăn mùi", "ngăn mùi", "sáp khử mùi", "xịt toàn thân"
    ]
    if any(normalize_text(k) in name_clean for k in priority_keywords_23):
        return labels_dict.get("Label 23", "Chăm Sóc Cá Nhân Khác")

    # 4. Chăm Sóc Tóc (Hair)
    # An toàn để check gội/xả/ủ vì sữa tắm/khử mùi đã bị bắt ở bước 3
    if any(normalize_text(k) in name_clean for k in SUB_MAP["21"]):
        return labels_dict.get("Label 21", "Chăm Sóc Tóc")

    # 5. Chăm Sóc Da (Skincare)
    # An toàn để check Nivea/Dove rửa mặt vì các sản phẩm body đã bị bắt ở bước 3
    if any(normalize_text(k) in name_clean for k in SUB_MAP["20"]):
        return labels_dict.get("Label 20", "Chăm Sóc Da")

    # 6. Mặc định Catch-all
    return labels_dict.get("Label 23", "Chăm Sóc Cá Nhân Khác")

def main():
    # 1. Load Labels
    labels_dict = {
        "Label 18": "Chăm Sóc Cá Nhân",
        "Label 19": "Chăm Sóc Răng Miệng",
        "Label 20": "Chăm Sóc Da",
        "Label 21": "Chăm Sóc Tóc",
        "Label 22": "Chăm Sóc Phụ Nữ",
        "Label 23": "Chăm Sóc Cá Nhân Khác"
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

    # 3. Combine and Deduplicate (CLEANING STEP)
    print("Combining and cleaning data...")
    master_df = pd.concat(all_names, ignore_index=True)
    # Quan trọng: Loại bỏ trùng lặp để file kết quả sạch nhất
    master_df = master_df.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    
    # 4. Apply Categorization
    print("Categorizing products...")
    master_df['subcategory'] = master_df['product_name'].apply(lambda x: get_subcategory(x, labels_dict))
    master_df['parent_category'] = labels_dict.get("Label 18", "Chăm Sóc Cá Nhân")

    # 5. Save
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\nSuccess! Saved to: {output_file}")
    
    # 6. Verification Preview
    print("\n--- Verification of Edge Cases ---")
    test_items = ["dao cạo", "sensitive", "kem xả", "sữa tắm", "bông tẩy trang"]
    preview = master_df[master_df['product_name'].apply(lambda x: any(k in normalize_text(x) for k in test_items))]
    if not preview.empty:
        print(preview.head(15))
    else:
        print("No matching items found for verification.")

if __name__ == "__main__":
    main()