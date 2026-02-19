import pandas as pd
import numpy as np
import glob
import os
import re
from scipy.stats import gmean

# --- CONFIGURATION (Cấu hình cho Spice) ---
csv_folder = '/Users/my/Online Food Price/Spice/CSV'
output_index_file = '/Users/my/Online Food Price/Spice/jevons_price_index.csv'

def extract_date(filename):
    # Tìm chuỗi ngày tháng dạng YYYY-MM-DD trong tên file
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    return match.group(0) if match else filename

def main():
    # 1. Quét và Sắp xếp file CSV theo ngày
    files = sorted(glob.glob(os.path.join(csv_folder, '*.csv')))
    
    if not files:
        print(f"❌ No CSV files found in {csv_folder}")
        return

    # Khởi tạo lịch sử chỉ số (Base period = 1.0)
    history = {'Gia Vị': {}} 
    prev_df = None
    prev_date = None
    
    results = []

    print(f"Found {len(files)} files. Starting Jevons index calculation for ALL spices as one category...")

    for file in files:
        current_date = extract_date(os.path.basename(file))
        print(f"Processing: {current_date}")
        
        try:
            # Load dữ liệu giá của ngày hiện tại
            curr_df = pd.read_csv(file, usecols=['product_name', 'final_price'])
            
            # GÁN TRỰC TIẾP: Tất cả sản phẩm đều thuộc nhóm "Gia Vị"
            curr_df['subcategory'] = 'Gia Vị'
            
            # Loại bỏ sản phẩm không có tên hoặc không có giá
            curr_df = curr_df.dropna(subset=['product_name', 'final_price'])
            
            # --- NGÀY ĐẦU TIÊN (BASE PERIOD) ---
            if prev_df is None:
                history['Gia Vị'][current_date] = 1.0
                results.append({'date': current_date, 'Gia Vị': 1.0})
            
            # --- CÁC NGÀY TIẾP THEO ---
            else:
                day_results = {'date': current_date}
                sub = 'Gia Vị'
                
                # Lấy danh sách sản phẩm & giá ở Ngày trước và Ngày nay
                p_prev = prev_df[['product_name', 'final_price']]
                p_curr = curr_df[['product_name', 'final_price']]
                
                # Tìm sản phẩm chung (Matched items)
                matched = p_prev.merge(p_curr, on='product_name', suffixes=('_prev', '_curr'))
                
                # SAFETY CHECK: Loại bỏ giá = 0
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
                results.append(day_results)
                
            # Lưu lại dữ liệu hôm nay để làm cơ sở cho ngày mai
            prev_df = curr_df
            prev_date = current_date
            
        except Exception as e:
            print(f"  ⚠️ Error processing file {file}: {e}")

    # 2. Xuất kết quả ra file CSV
    if results:
        final_df = pd.DataFrame(results)
        final_df.to_csv(output_index_file, index=False, encoding='utf-8-sig')
        print(f"\n✅ Jevons Index calculated for Spice. Saved to: {output_index_file}")
        print("\nPreview of last 5 days:")
        print(final_df.tail())
    else:
        print("No results generated.")

if __name__ == "__main__":
    main()