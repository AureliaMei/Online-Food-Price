import pandas as pd
import glob
import os
import json

# --- CẤU HÌNH ĐƯỜNG DẪN ---
csv_folder = '/Users/my/Online Food Price/Frozen/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Frozen/cat_lookup_table.csv'

# --- TỪ KHÓA PHÂN LOẠI ---
SUB_MAP = {
    # 62: Chả giò
    "62": ["chả giò", "chả", "giò"],
    
    # 63: Viên (Thêm "thả lẩu" vào đây)
    "63": ["viên", "mọc", "thả lẩu"],
    
    # 64: Chế biến sẵn (Bánh, Khoai, Pizza...)
    "64": [
        "bánh", "pizza", "há cảo", "xíu mại", "khoai", "lẩu", "phô mai que", 
        "sủi cảo", "mandoo", "nugget", "rau", "nấm", "mỳ ý", "cơm chiên", "xôi", "chả ốc", "nem", 
        "xúc xích", "lạp xưởng"
    ],
    
    # 60: Hải sản
    "60": [
        "hải sản", "tôm", "mực", "cá", "nghêu", "sò", "ốc", "hến", "hàu", 
        "cua", "ghẹ", "surimi", "thanh cua", "bạch tuộc", "chả mực", "tép", "lươn"
    ],
    
    # 61: Thịt
    "61": [
        "thịt", "bò", "heo", "gà", "trâu", "dồi", "ba chỉ", "lõi vai", "bắp", "steak"
    ]
}

def get_subcategory(name, labels_dict):
    name_lower = str(name).lower()
    
    # --- THỨ TỰ ƯU TIÊN MỚI (QUAN TRỌNG) ---
    
    # 1. Chả Giò (Rất đặc thù, check đầu tiên)
    if any(k in name_lower for k in SUB_MAP["62"]):
        return labels_dict.get("Label 62", "Chả Giò")

    # 2. Cá - Bò Viên (Đưa lên trên nhóm 64)
    # Để bắt "Viên thả lẩu" vào đây trước khi bị từ khóa "lẩu" của nhóm 64 bắt.
    if any(k in name_lower for k in SUB_MAP["63"]):
        return labels_dict.get("Label 63", "Cá - Bò Viên")

    # 3. Thực Phẩm Đông Lạnh Khác (Đồ chế biến sẵn)
    # Kiểm tra "Nugget", "Pizza", "Há cảo" ở đây.
    # Lưu ý: "Nugget mực" sẽ vào đây (vì Nugget thuộc 64) thay vì vào Mực (60).
    if any(k in name_lower for k in SUB_MAP["64"]):
        return labels_dict.get("Label 64", "Thực Phẩm Đông Lạnh Khác")

    # 4. Hải Sản Đông Lạnh
    if any(k in name_lower for k in SUB_MAP["60"]):
        return labels_dict.get("Label 60", "Hải Sản Đông Lạnh")

    # 5. Thịt Đông Lạnh
    if any(k in name_lower for k in SUB_MAP["61"]):
        return labels_dict.get("Label 61", "Thịt Đông Lạnh")

    # 6. Mặc định (Catch-all)
    # Gán cứng tên để đảm bảo không bị nhầm với Parent Category
    return "Thực Phẩm Đông Lạnh Khác"

def main():
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            labels_list = json.load(f)
            labels_dict = labels_list[0]
    except Exception as e:
        print(f"Lỗi đọc file JSON: {e}")
        labels_dict = {}

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

    master_df = pd.concat(all_names, ignore_index=True)
    master_df = master_df.drop_duplicates(subset=['product_name']).reset_index(drop=True)
    
    print("Đang phân loại sản phẩm...")
    master_df['subcategory'] = master_df['product_name'].apply(lambda x: get_subcategory(x, labels_dict))
    master_df['parent_category'] = labels_dict.get("Label 65", "Thực Phẩm Đông Lạnh")

    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\nThành công! File lưu tại: {output_file}")
    
    # Kiểm tra lại các trường hợp bị lỗi cũ
    print("\n--- Kiểm tra Logic Mới ---")
    test_keywords = ["viên thả lẩu", "nugget", "bánh xếp", "chả ốc"]
    preview = master_df[master_df['product_name'].str.lower().str.contains('|'.join(test_keywords))]
    if not preview.empty:
        print(preview.head(10))

if __name__ == "__main__":
    main()