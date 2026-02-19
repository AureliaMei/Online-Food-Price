import pandas as pd
import numpy as np
import glob
import os
import re
from scipy.stats import gmean

# --- CONFIGURATION (Cấu hình cho Veg_Fruit) ---
csv_folder = '/Users/my/Online Food Price/Veg_Fruit/CSV'
lookup_file = '/Users/my/Online Food Price/Veg_Fruit/cat_lookup_table.csv'
output_index_file = '/Users/my/Online Food Price/Veg_Fruit/jevons_price_index.csv'

def extract_date(filename):
    # Tìm chuỗi ngày tháng dạng YYYY-MM-DD trong tên file
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    return match.group(0) if match else filename

def main():
    # 1. Load Lookup Table (Bảng phân loại)
    if not os.path.exists(lookup_file):
        print(f"❌ Lookup file not found: {lookup_file}")
        print("   Vui lòng chạy script phân loại (categorization) trước.")
        return

    try:
        # Load bảng phân loại và loại bỏ trùng lặp (giữ dòng mới nhất)
        lookup = pd.read_csv(lookup_file, usecols=['product_name', 'subcategory'])
        lookup = lookup.drop_duplicates(subset=['product_name'], keep='last')
    except Exception as e:
        print(f"❌ Error reading lookup file: {e}")
        return
    
    # 2. Quét và Sắp xếp file CSV theo ngày
    files = sorted(glob.glob(os.path.join(csv_folder, '*.csv')))
    
    if not files:
        print(f"❌ No CSV files found in {csv_folder}")
        return

    # Khởi tạo lịch sử chỉ số (Base period = 1.0)
    history = {} 
    prev_df = None
    prev_date = None
    
    results = []

    print(f"Found {len(files)} files. Starting Jevons index calculation for Veg & Fruit...")

    for file in files:
        current_date = extract_date(os.path.basename(file))
        print(f"Processing: {current_date}")
        
        try:
            # Load dữ liệu giá của ngày hiện tại
            curr_df = pd.read_csv(file, usecols=['product_name', 'final_price'])
            
            # Ghép với bảng phân loại (Lookup)
            curr_df = curr_df.merge(lookup, on='product_name', how='left')
            
            # Loại bỏ sản phẩm không có nhóm hoặc không có giá
            curr_df = curr_df.dropna(subset=['subcategory', 'final_price'])
            
            # --- NGÀY ĐẦU TIÊN (BASE PERIOD) ---
            if prev_df is None:
                day_results = {'date': current_date}
                subcategories = curr_df['subcategory'].unique()
                for sub in subcategories:
                    # Khởi tạo chỉ số 1.0 cho tất cả nhóm
                    history[sub] = {current_date: 1.0}
                    day_results[sub] = 1.0
                results.append(day_results)
            
            # --- CÁC NGÀY TIẾP THEO ---
            else:
                day_results = {'date': current_date}
                
                # Duyệt qua từng nhóm hàng đã có trong lịch sử (Rau lá, Củ quả, Trái cây tươi)
                for sub in history.keys():
                    # Lấy danh sách sản phẩm & giá của nhóm đó ở Ngày trước và Ngày nay
                    p_prev = prev_df[prev_df['subcategory'] == sub][['product_name', 'final_price']]
                    p_curr = curr_df[curr_df['subcategory'] == sub][['product_name', 'final_price']]
                    
                    # Tìm sản phẩm chung (Matched items)
                    matched = p_prev.merge(p_curr, on='product_name', suffixes=('_prev', '_curr'))
                    
                    # SAFETY CHECK: Loại bỏ giá = 0 để tránh lỗi chia cho 0
                    matched = matched[(matched['final_price_prev'] > 0) & (matched['final_price_curr'] > 0)]

                    if not matched.empty:
                        # Công thức Jevons: Trung bình nhân (Geometric Mean) của tỷ lệ giá
                        price_relatives = matched['final_price_curr'] / matched['final_price_prev']
                        chain_relative = gmean(price_relatives)
                        
                        # Cập nhật chỉ số: Index Mới = Index Cũ * Chain Relative
                        prev_index = history[sub].get(prev_date, 1.0)
                        new_index = prev_index * chain_relative
                        history[sub][current_date] = new_index
                    else:
                        # Nếu không có sản phẩm chung, giữ nguyên chỉ số cũ (Flat)
                        history[sub][current_date] = history[sub].get(prev_date, 1.0)
                    
                    day_results[sub] = history[sub][current_date]
                
                # Kiểm tra nhóm mới xuất hiện (nếu có trường hợp data bị thiếu ở ngày đầu)
                current_subs = curr_df['subcategory'].unique()
                for sub in current_subs:
                    if sub not in history:
                        history[sub] = {current_date: 1.0}
                        day_results[sub] = 1.0

                results.append(day_results)
                
            # Lưu lại dữ liệu hôm nay để làm cơ sở cho ngày mai
            prev_df = curr_df
            prev_date = current_date
            
        except Exception as e:
            print(f"  ⚠️ Error processing file {file}: {e}")

    # 3. Xuất kết quả ra file CSV
    if results:
        final_df = pd.DataFrame(results)
        
        # Sắp xếp cột: Date đứng đầu, các nhóm xếp theo thứ tự alphabet
        cols = ['date'] + sorted([c for c in final_df.columns if c != 'date'])
        final_df = final_df[cols]
        
        final_df.to_csv(output_index_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ Jevons Index calculated for Veg & Fruit. Saved to: {output_index_file}")
        print("\nPreview of last 5 days:")
        print(final_df.tail())
    else:
        print("No results generated.")

if __name__ == "__main__":
    main()