import pandas as pd
import glob
import os
import json

# --- CONFIGURATION ---
csv_folder = '/Users/my/Online Food Price/Household_good/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Household_good/cat_lookup_table.csv'

# --- KEYWORD MAPPING (SUB_MAP) ---
# --- CẬP NHẬT LẠI SUB_MAP ---
# --- CẬP NHẬT KEYWORD MAPPING (SUB_MAP) ---
SUB_MAP = {
    "74": ["gối", "chăn", "ga", "đệm", "mền", "drap", "vỏ gối", "chiếu", "ruột gối"],
    
    "78": [
        # Chỉ dùng cụm từ rõ ràng, không dùng từ đơn gây nhiễu
        "pin ", "pin aaa", "pin aa", "ổ cắm", "bóng đèn", "điện quang", "energizer", 
        "công tắc", "vợt muỗi", "vợt bắt muỗi", "đèn bắt muỗi", "ổ điện"
    ],
    
    "77": [
        "nồi", "chảo", "dao", "kéo", "thớt", "bình nước", "bình giữ nhiệt", 
        "hộp", "bát", "đĩa", "đũa", "thìa", "muỗng", "nĩa", "vá", "muôi", 
        "màng bọc", "màng nhôm", "giấy thấm", "giấy nến", "giấy bạc", "giấy nướng",
        "túi đựng thực phẩm", "zipper", 
        "ly", "cốc", "ca nước", "ca nhựa", "tách",
        "ống hút", "cốc giấy", "đĩa giấy", "bát giấy", # Đồ dùng 1 lần
        "xửng", "khay", "hũ", "lọ", "khuôn", "thau", "rổ", "rá", 
        "bộ ăn", "beefsteak", "môi múc", 
        "băm", "xay", "vắt cam", "bào", "gọt" # Dụng cụ sơ chế
    ],
    
    "79": [
        "lau nhà", "chổi", "cây lăn bụi", "thùng rác", "sọt", "túi rác", "bao rác", 
        "găng tay", "mút", "cước", "bàn chải", "cọ rửa", "khăn lau", "túi giặt", 
        "sáp thơm", "sáp", "xịt phòng", "đuổi muỗi", "khử mùi", "làm sạch", "gel làm sạch", 
        "glade", "aisen", "scotch brite", "vim", "gift", "sunlight", "nước lau", "oasis", 
        "home deli" # Thường là túi rác hoặc găng tay (cẩn thận check kĩ)
    ],
    
    "76": ["kìm", "búa", "tua vít", "cờ lê", "mỏ lết", "khoan"],
    
    "75": [
        "khăn", "thảm", "móc", "giỏ", "tủ", "kệ", "ghế", "bàn", 
        "quảng phú", "mollis", "trang trí", "màn", "cầu là", "bắc bếp", "túi lohas"
    ]
}

def get_subcategory(name, labels_dict):
    name_lower = str(name).lower()
    
    # --- LOGIC ƯU TIÊN (ĐÃ TINH CHỈNH) ---
    
    # 1. Điện (Electrical) - Check kỹ các cụm từ "vợt muỗi" trước
    # Logic: Nếu khớp keyword nhóm 78 -> Là Điện
    if any(k in name_lower for k in SUB_MAP["78"]):
        return labels_dict.get("Label 78", "Thiết bị dùng điện trong nhà")

    # 2. Vệ sinh (Cleaning) 
    # Logic: Check sáp thơm, đuổi muỗi ở đây. 
    # Lưu ý: "Sáp thơm đuổi muỗi" sẽ khớp "đuổi muỗi" ở đây (đã pass qua bước 1 vì bước 1 không còn bắt từ "muỗi" lẻ nữa)
    if any(k in name_lower for k in SUB_MAP["79"]):
        return labels_dict.get("Label 79", "Vệ sinh nhà cửa")

    # 3. Phòng ngủ
    if any(k in name_lower for k in SUB_MAP["74"]):
        return labels_dict.get("Label 74", "Đồ Dùng Phòng Ngủ")

    # 4. Nhà bếp (Kitchen)
    if any(k in name_lower for k in SUB_MAP["77"]):
        return labels_dict.get("Label 77", "Đồ dùng nhà bếp")

    # 5. Sửa chữa
    if any(k in name_lower for k in SUB_MAP["76"]):
        return labels_dict.get("Label 76", "Dụng cụ sữa chữa")

    # 6. Mặc định (Household)
    # Các loại Móc áo, Kệ Inochi, Thảm... sẽ rơi vào đây
    return labels_dict.get("Label 75", "Đồ dùng trong nhà")

def main():
    # 1. Load JSON Labels
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            labels_list = json.load(f)
            labels_dict = labels_list[0]
    except Exception as e:
        print(f"Error loading JSON: {e}")
        labels_dict = {}

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
    master_df = pd.concat(all_names, ignore_index=True)
    master_df = master_df.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    
    # 4. Apply Categorization
    print("Categorizing products...")
    master_df['subcategory'] = master_df['product_name'].apply(lambda x: get_subcategory(x, labels_dict))
    master_df['parent_category'] = labels_dict.get("Label 80", "Đồ Dùng Gia Đình")

    # 5. Save
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\nSuccess! Saved to: {output_file}")
    
    # 6. Verification Preview
    print("\n--- Verification of Fixes ---")
    check_list = ["vợt muỗi", "vá canh", "cốc giấy", "sáp thơm oasis", "ống hút", "khuôn"]
    preview = master_df[master_df['product_name'].str.lower().str.contains('|'.join(check_list))]
    if not preview.empty:
        print(preview.head(10))
    else:
        print("No matching items found for verification.")

if __name__ == "__main__":
    main()