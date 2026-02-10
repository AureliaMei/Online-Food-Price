import pandas as pd
import glob
import os
import json

# --- CẤU HÌNH ĐƯỜNG DẪN ---
csv_folder = '/Users/my/Online Food Price/Detergents/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Detergents/cat_lookup_table.csv'

# --- TỪ KHÓA CHỨC NĂNG (FUNCTIONAL KEYWORDS) ---
SUB_MAP = {
    "12": ["nước giặt", "bột giặt", "viên giặt", "giặt xả", "giặt tẩy", "giặt máy", "giặt tay"], 
    "13": ["nước xả", "xả vải", "làm mềm vải", "xịt vải", "thơm vải", "khô", "giấy thơm", "NXV"],             
    "14": ["rửa chén", "rửa bát", "viên rửa chén", "rửa ly", "gel rửa chén"], 
    "15": ["côn trùng", "muỗi", "kiến", "gián", "ruồi", "xông đuổi"], 
    "16": ["lau sàn", "lau kính", "lau bếp", "lau đa năng", "lau bề mặt", "lau nhà", "vệ sinh kính", "tẩy rửa đa năng"],
    "17": ["tẩy", "bồn cầu", "toilet", "thông tắc", "viên treo", "ố vàng", "mảng bám", "nhà tắm", "viên tẩy", "VIM"] 
}

def get_subcategory(name, labels_dict):
    name_lower = str(name).lower()
    
    # --- HỆ THỐNG ƯU TIÊN ---
    
    # 1. Lau Sàn / Kính / Bếp
    if any(k in name_lower for k in SUB_MAP["16"]):
        return labels_dict.get("Label 16", "Nước Lau Sàn - Lau Kính") 

    # 2. Rửa Chén Bát
    if any(k in name_lower for k in SUB_MAP["14"]):
        return labels_dict.get("Label 14", "Nước Rửa Chén")

    # 3. Diệt Côn Trùng
    if any(k in name_lower for k in SUB_MAP["15"]):
        return labels_dict.get("Label 15", "Bình Xịt Côn Trùng")
        
    # 4. Giặt (Laundry Detergent)
    if any(k in name_lower for k in SUB_MAP["12"]):
        return labels_dict.get("Label 12", "Nước Giặt")

    # 5. Tẩy Rửa Chuyên Dụng
    if any(k in name_lower for k in SUB_MAP["17"]):
        return labels_dict.get("Label 17", "Nước Tẩy Rửa")

    # 6. Xả Vải
    if any(k in name_lower for k in SUB_MAP["13"]):
        return labels_dict.get("Label 13", "Nước Xả")

    # 7. Mặc định (nếu không khớp gì cả)
    # Trả về một nhóm chung chung, nhưng KHÔNG phải là tên Parent Category
    return "Bug catcher / Detergents"

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
    
    # Cột subcategory: Chạy hàm get_subcategory
    master_df['subcategory'] = master_df['product_name'].apply(lambda x: get_subcategory(x, labels_dict))
    
    # Cột parent_category: Cố định là "Hóa Phẩm - Tẩy rửa" (Label 11)
    # Lấy tên chuẩn từ file JSON nếu có, hoặc dùng chuỗi mặc định
    parent_name = labels_dict.get("Label 11", "Hóa Phẩm - Tẩy rửa")
    master_df['parent_category'] = parent_name

    # 5. Lưu file kết quả
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\nThành công! Đã tạo bảng tra cứu với {len(master_df)} sản phẩm.")
    print(f"File lưu tại: {output_file}")
    
    # Hiển thị mẫu
    print("\n--- Mẫu dữ liệu (10 dòng đầu) ---")
    print(master_df.head(10))

if __name__ == "__main__":
    main()