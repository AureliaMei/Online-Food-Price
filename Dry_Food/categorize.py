import pandas as pd
import glob
import os
import json

# --- CẤU HÌNH ĐƯỜNG DẪN ---
csv_folder = '/Users/my/Online Food Price/Dry_Food/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Dry_Food/cat_lookup_table.csv'

# --- TỪ KHÓA PHÂN LOẠI (SUB_MAP) ---
# Label 47: Gạo - Nông Sản Khô
# Label 48: Ngũ Cốc - Yến Mạch
# Label 49: Thực Phẩm Đóng Hộp
# Label 50: Rong Biển - Tảo Biển
# Label 51: Bột Các Loại
# Label 52: Thực Phẩm Chay

SUB_MAP = {
    "52": ["chay", "thực phẩm chay", "âu lạc", "an nhiên"], 
    "50": ["rong biển", "tảo", "lá kim", "rong nho", "kimnori", "kimbap", "cuộn cơm", "tokyolin", "r ong", "lá"],
    "51": ["bột", "thạch", "sương sáo", "nêm sẵn", "aji-quick", "chiên giòn", "chiên xù", "làm bánh", "pancake", "bánh rán"],
    "48": ["yến mạch", "ngũ cốc", "corn flakes", "muesli", "granola", "oatta", "kellogg", "nestlé", "milo", "froot loops", "koko krunch", "honey star", "calbee", "ngũ cốc", "oats"],
    "47": ["gạo", "nếp", "đậu xanh", "đậu đen", "đậu đỏ", "hạt sen", "lạc nhân", "hạt điều", "đậu phộng", "mè", "vừng", "nông sản", "nấm", "mộc nhĩ", "măng khô", "đỗ", "hạt"],
    # Label 49: Gom hết các loại đóng hộp, hũ, gói sốt, thịt chế biến sẵn
    "49": [
        "pate", "cá", "heo hầm", "bò hầm", "thịt xay", "thịt hộp", "spam", "tép", "tôm", "mực",
        "dưa chuột ngâm", "mứt", "bơ đậu phộng", "oliu", "bơ thực vật", "xúc xích", 
        "thịt viên", "cà chua", "đóng hộp", "lon", "lọ", "hũ", "ruốc",
        "nutella", "phết", "cacao", # Spreads
        "thịt áp chảo", "heo cao bồi", "ponnie", "cột đèn", # Các brand thịt chế biến
        "xốt", "gia vị", "nước mắm", "kho quẹt", # Sốt/Gia vị lỏng
        "rim", "sấy giòn", "ăn liền", "tẩm gia vị" # Đồ ăn vặt chế biến (Mực rim, cá cơm sấy)
    ]
}

def get_subcategory(name, labels_dict):
    name_lower = str(name).lower()
    
    # --- HỆ THỐNG ƯU TIÊN ---
    
    # 1. Thực Phẩm Chay (Ưu tiên cao nhất)
    if any(k in name_lower for k in SUB_MAP["52"]):
        return labels_dict.get("Label 52", "Thực Phẩm Chay")

    # 2. Rong Biển - Tảo Biển
    if any(k in name_lower for k in SUB_MAP["50"]):
        return labels_dict.get("Label 50", "Rong Biển - Tảo Biển")

    # 3. Bột Các Loại
    if any(k in name_lower for k in SUB_MAP["51"]):
        return labels_dict.get("Label 51", "Bột Các Loại")

    # 4. Ngũ Cốc - Yến Mạch
    if any(k in name_lower for k in SUB_MAP["48"]):
        return labels_dict.get("Label 48", "Ngũ Cốc - Yến Mạch")

    # 5. Gạo - Nông Sản Khô
    if any(k in name_lower for k in SUB_MAP["47"]) and "bơ" not in name_lower: # Tránh Bơ đậu phộng
        return labels_dict.get("Label 47", "Gạo - Nông Sản Khô")

    # 6. Thực Phẩm Đóng Hộp (Pate, Đồ hộp, Bơ, Mứt...)
    if any(k in name_lower for k in SUB_MAP["49"]):
        return labels_dict.get("Label 49", "Thực Phẩm Đóng Hộp")

    # 7. Mặc định: Thực Phẩm Khô (Label 46)
    # Các loại khô cá, khô mực, tôm khô không nằm trong danh sách con sẽ vào đây
    return labels_dict.get("Label 46", "Thực Phẩm Khô")

def main():
    # 1. Tải danh sách nhãn từ JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            labels_list = json.load(f)
            labels_dict = labels_list[0]
    except Exception as e:
        print(f"Lỗi đọc file JSON: {e}")
        labels_dict = {}

    # 2. Đọc các file CSV dữ liệu
    if not os.path.exists(csv_folder):
        print(f"Lỗi: Không tìm thấy thư mục {csv_folder}")
        return

    csv_files = glob.glob(os.path.join(csv_folder, '*.csv'))
    all_names = []

    print(f"Đang đọc {len(csv_files)} file CSV...")
    for file in csv_files:
        try:
            df = pd.read_csv(file, encoding='utf-8-sig', usecols=['product_name'])
            all_names.append(df)
        except Exception as e:
            print(f"Bỏ qua file {file}: {e}")

    if not all_names:
        print("Không có dữ liệu nào.")
        return

    # 3. Gộp và Lọc trùng lặp
    master_df = pd.concat(all_names, ignore_index=True)
    initial_count = len(master_df)
    master_df = master_df.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    
    print(f"Đã loại bỏ {initial_count - len(master_df)} dòng trùng lặp.")

    # 4. Áp dụng Phân loại
    print("Đang phân loại sản phẩm...")
    master_df['subcategory'] = master_df['product_name'].apply(lambda x: get_subcategory(x, labels_dict))
    
    # Parent category: Label 46
    master_df['parent_category'] = labels_dict.get("Label 46", "Thực Phẩm Khô")

    # 5. Lưu file kết quả
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\nThành công! Đã tạo bảng tra cứu với {len(master_df)} sản phẩm.")
    print(f"File lưu tại: {output_file}")
    
    # Hiển thị mẫu kiểm tra
    print("\n--- Mẫu dữ liệu (Kiểm tra các nhóm) ---")
    test_keywords = ["gạo", "yến mạch", "pate", "rong", "bột", "tôm khô"]
    preview = master_df[master_df['product_name'].str.lower().str.contains('|'.join(test_keywords))]
    print(preview.head(10))

if __name__ == "__main__":
    main()