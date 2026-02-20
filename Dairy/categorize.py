import pandas as pd
import glob
import os
import json

# --- CẤU HÌNH ĐƯỜNG DẪN ---
csv_folder = '/Users/my/Online Food Price/Dairy/CSV'
json_path = '/Users/my/Online Food Price/Category list' 
output_file = '/Users/my/Online Food Price/Dairy/cat_lookup_table.csv'

# --- TỪ KHÓA PHÂN LOẠI (SUB_MAP) ---
# Đã tinh chỉnh để tránh nhận diện nhầm
SUB_MAP = {
    "1": ["đậu nành", "đậu đen", "óc chó", "hạnh nhân", "mè đen", "gạo lứt", "bắp", "sữa hạt", "macca", "đậu đỏ", "lúa", "yến mạch", "milo", "ovaltine"], 
    "2": ["sữa bột", "bột", "công thức", "ensure", "pedia", "grow", "similac", "colosbaby", "famna", "optimum", "pediasure", "glucerna", "nan ", "nuvi"],             
    "3": ["bơ", "phô mai", "cheese", "bơ lạt", "bơ mặn", "thực vật", "mascarpone", "cream cheese", "phomai", "kem sữa", "whipping", "cooking cream"], 
    "4": ["sữa đặc", "ông thọ", "ngôi sao", "hoàn hảo", "creamer", "tài lộc"], 
    "5": ["chua", "váng", "men", "probi", "yakult", "betagen", "susu", "zott", "kun", "yomost"] 
}

def get_subcategory(name, labels_dict):
    name_lower = str(name).lower()
    
    # --- HỆ THỐNG ƯU TIÊN (PRIORITY SYSTEM) ---
    # Thứ tự kiểm tra rất quan trọng để tránh nhầm lẫn

    if "sữa trái cây" in name_lower:
        return "Sữa tươi"
    
    # 1. Ưu tiên Sữa Chua (Để bắt "Sữa chua uống vị phô mai" vào nhóm Sữa chua chứ không phải Phô mai)
    if any(k in name_lower for k in SUB_MAP["5"]):
        return labels_dict.get("Label 5", "Sữa Chua - Váng Sữa")
        
    # 2. Sữa đặc (Để bắt "Sữa đặc nguyên kem" vào nhóm Sữa đặc chứ không phải Sữa bột/tươi)
    if any(k in name_lower for k in SUB_MAP["4"]):
        return labels_dict.get("Label 4", "Sữa đặc")

    # 3. Sữa Hạt - Lúa mạch
    if any(k in name_lower for k in SUB_MAP["1"]):
        return labels_dict.get("Label 1", "Sữa Hạt - Sữa Đậu")

    # 4. Bơ - Phô Mai
    if any(k in name_lower for k in SUB_MAP["3"]):
        return labels_dict.get("Label 3", "Bơ Sữa - Phô Mai")

    # 5. Sữa Bột
    if any(k in name_lower for k in SUB_MAP["2"]):
        return labels_dict.get("Label 2", "Sữa Bột")

    # 6. Mặc định: Sữa tươi
    # Nếu không dính các từ khóa trên, ta coi nó là Sữa tươi (Fresh Milk)
    return "Sữa tươi"

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
    master_df['parent_category'] = "Sữa các loại"

    # 5. Lưu file kết quả
    master_df = master_df[['product_name', 'subcategory', 'parent_category']]
    master_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"\nThành công! Đã tạo bảng tra cứu với {len(master_df)} sản phẩm.")
    print(f"File lưu tại: {output_file}")
    
    # Hiển thị mẫu để kiểm tra
    print("\n--- Mẫu dữ liệu (5 dòng đầu) ---")
    print(master_df.head(5))

if __name__ == "__main__":
    main()