import pandas as pd
import glob
import os
import json

# --- CẤU HÌNH ĐƯỜNG DẪN ---
csv_folder = '/Users/my/Online Food Price/Egg_and_soy/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Egg_and_soy/cat_lookup_table.csv'

# --- TỪ KHÓA PHÂN LOẠI (SUB_MAP) ---
# Label 67: Trứng
# Label 68: Đậu hũ

SUB_MAP = {
    "67": ["trứng", "hột gà", "hột vịt", "quả"],
    "68": ["đậu hũ", "tàu hũ", "đậu phụ", "đậu thanh", "tafu", "tofu", "đậu non", "đậu mơ", "đâu"]
}

def get_subcategory(name, labels_dict):
    name_lower = str(name).lower()
    
    # --- HỆ THỐNG ƯU TIÊN ---
    
    # 1. Đậu hũ (Label 68) - Ưu tiên kiểm tra trước
    # Lý do: Để bắt "Tàu hũ trứng" vào nhóm Đậu hũ chứ không phải nhóm Trứng
    if any(k in name_lower for k in SUB_MAP["68"]):
        return labels_dict.get("Label 68", "Đậu hũ")

    # 2. Trứng (Label 67)
    if any(k in name_lower for k in SUB_MAP["67"]):
        return labels_dict.get("Label 67", "Trứng")

    # 3. Mặc định: Trứng - Đậu Hũ (Label 66)
    return labels_dict.get("Label 66", "Trứng - Đậu Hũ")

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
    
    # Parent category: Label 66
    master_df['parent_category'] = labels_dict.get("Label 66", "Trứng - Đậu Hũ")

    # 5. Lưu file kết quả
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\nThành công! Đã tạo bảng tra cứu với {len(master_df)} sản phẩm.")
    print(f"File lưu tại: {output_file}")
    
    # Hiển thị mẫu kiểm tra
    print("\n--- Mẫu dữ liệu (Kiểm tra Tàu hũ trứng) ---")
    test_keywords = ["tàu hũ trứng", "đậu phụ", "omega"]
    preview = master_df[master_df['product_name'].str.lower().str.contains('|'.join(test_keywords))]
    print(preview.head(10))

if __name__ == "__main__":
    main()