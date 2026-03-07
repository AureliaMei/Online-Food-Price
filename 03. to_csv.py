import os
import json
import pandas as pd
import re
from datetime import datetime

# --- CONFIGURATION ---
TARGET_START_DATE = datetime(2026, 3, 5).date()
TARGET_END_DATE = datetime(2026, 3, 7).date()

def clean_price(val):
    if not val or pd.isna(val) or val == "":
        return 0.0
    digits = re.sub(r'[^\d]', '', str(val))
    return float(digits) if digits else 0.0

def get_price_logic(p1, p2):
    """
    Standard Logic: 
    - Lower price is Final.
    - Higher price is Marked.
    """
    if p1 > 0 and p2 > 0:
        return min(p1, p2), max(p1, p2)
    elif p1 > 0:
        return p1, None
    elif p2 > 0:
        return p2, None
    return 0.0, None

def is_date_in_range(filename):
    """
    Extracts date from filename: 'run_2026-02-07_4da2...'
    Returns True if date is between Jan 31 and Feb 07.
    """
    try:
        parts = filename.split('_')
        # Usually format is: run_[DATE]_[ID]
        date_str = parts[1] 
        file_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return TARGET_START_DATE <= file_date <= TARGET_END_DATE
    except:
        return False

# --- MAPPING FUNCTIONS ---
def map_dairy(item):
    p_marked = clean_price(item.get('Marked Price'))
    p_discount = clean_price(item.get('Discounted Price'))
    final, marked = get_price_logic(p_discount, p_marked)
    return {'product_name': item.get('Product Name'), 'unit': item.get('Unit'), 'final_price': final, 'marked_price': marked, 'product_url': item.get('Product URL')}

def map_detergents(item):
    p1, p2 = clean_price(item.get('Label 6')), clean_price(item.get('Label 7'))
    final, marked = get_price_logic(p1, p2)
    return {'product_name': item.get('Label 4'), 'unit': item.get('Label 5'), 'final_price': final, 'marked_price': marked, 'product_url': item.get('Label 1')}

def map_dry_food(item):
    p1, p2 = clean_price(item.get('Label 7')), clean_price(item.get('Label 8'))
    final, marked = get_price_logic(p1, p2)
    return {'product_name': item.get('Label 5'), 'unit': item.get('Label 6'), 'final_price': final, 'marked_price': marked, 'product_url': item.get('Label 4')}

def map_veg_fruit(item):
    p1, p2 = clean_price(item.get('Final Price')), clean_price(item.get('Marked Price'))
    final, marked = get_price_logic(p1, p2)
    return {'product_name': item.get('Product Name'), 'unit': item.get('Unit'), 'final_price': final, 'marked_price': marked, 'product_url': item.get('Product URL')}

def map_spice(item):
    p1, p2 = clean_price(item.get('Label 8')), clean_price(item.get('Label 9'))
    final, marked = get_price_logic(p1, p2)
    return {'product_name': item.get('Label 5'), 'unit': item.get('Label 6'), 'final_price': final, 'marked_price': marked, 'product_url': item.get('Label 4')}

def map_processed_food(item):
    p1, p2 = clean_price(item.get('Label 7')), clean_price(item.get('Label 8'))
    final, marked = get_price_logic(p1, p2)
    return {'product_name': item.get('Label 5'), 'unit': item.get('Label 6'), 'final_price': final, 'marked_price': marked, 'product_url': item.get('Label 4')}

def map_hygiene(item):
    p1, p2 = clean_price(item.get('Label 5')), clean_price(item.get('Label 6'))
    final, marked = get_price_logic(p1, p2)
    return {'product_name': item.get('Label 3'), 'unit': item.get('Label 4'), 'final_price': final, 'marked_price': marked, 'product_url': item.get('Label 1')}

def map_electronics(item):
    p1, p2 = clean_price(item.get('Label 8')), clean_price(item.get('Label 9'))
    final, marked = get_price_logic(p1, p2)
    return {'product_name': item.get('Label 5'), 'unit': item.get('Label 6'), 'final_price': final, 'marked_price': marked, 'product_url': item.get('product_url', 'N/A')}

def map_egg_soy(item):
    p1, p2 = clean_price(item.get('Label 6')), clean_price(item.get('Label 7'))
    final, marked = get_price_logic(p1, p2)
    return {'product_name': item.get('Label 4'), 'unit': item.get('Label 5'), 'final_price': final, 'marked_price': marked, 'product_url': item.get('Label 1')}

def map_baby_product(item):
    # Based on your JSON: Label 7 & 8 are prices, Label 5 is Name, Label 6 is Unit, Label 4 is URL
    p1, p2 = clean_price(item.get('Label 7')), clean_price(item.get('Label 8'))
    final, marked = get_price_logic(p1, p2)
    return {
        'product_name': item.get('Label 5'), 
        'unit': item.get('Label 6'), 
        'final_price': final, 
        'marked_price': marked, 
        'product_url': item.get('Label 4')
    }

def map_instant_food(item):
    # Updated to handle the new explicit keys
    p1, p2 = clean_price(item.get('Actual price')), clean_price(item.get('Marked Price'))
    final, marked = get_price_logic(p1, p2)
    return {
        'product_name': item.get('Product_name'), 
        'unit': item.get('Unit'), 
        'final_price': final, 
        'marked_price': marked, 
        'product_url': item.get('URL')
    }

# --- CONFIG ---
ROBOT_CONFIG = {
    "Dry_Food": map_dry_food,
    "Instant_food": map_instant_food,
    "Confectionary": map_processed_food, # ĐÃ THÊM DÒNG NÀY (sử dụng map_processed_food vì cùng cấu trúc Label)
    "Dairy": map_dairy,
    "Egg_and_soy": map_egg_soy,
    "Spice": map_spice,
    "Processed_food": map_processed_food,
    "Veg_Fruit": map_veg_fruit,
    "Frozen": map_processed_food,
    "Baby_product": map_baby_product
}

def process_all_robots():
    base_path = os.getcwd()
    print(f"📅 Filter Range: {TARGET_START_DATE} to {TARGET_END_DATE}")

    for folder_name, mapper_func in ROBOT_CONFIG.items():
        robot_path = os.path.join(base_path, folder_name)
        json_dir = os.path.join(robot_path, "JSON")
        csv_dir = os.path.join(robot_path, "CSV")

        if not os.path.exists(json_dir): continue
        if not os.path.exists(csv_dir): os.makedirs(csv_dir)

        print(f"🔍 {folder_name}...")

        processed_count = 0
        skipped_count = 0

        for file in os.listdir(json_dir):
            if not file.endswith(".json"): continue

            # 1. CHECK DATE FROM FILENAME
            if not is_date_in_range(file):
                continue
            
            # 2. Setup Paths
            json_path = os.path.join(json_dir, file)
            # Create CSV filename by swapping extension
            csv_filename = file.replace(".json", ".csv")
            csv_path = os.path.join(csv_dir, csv_filename)

            # 3. SKIP LOGIC: If CSV exists, skip immediately
            if os.path.exists(csv_path):
                skipped_count += 1
                continue

            # 4. Process if not skipped
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    run_data = json.load(f)

                if run_data.get('status') != 'success': continue

                raw_list = run_data.get('data', {}).get('listData', {}).get('List Data 1', [])
                cleaned_rows = []

                for item in raw_list:
                    mapped_data = mapper_func(item)
                    mapped_data['scrape_timestamp'] = run_data.get('startedAt')
                    mapped_data['run_id'] = run_data.get('id')
                    cleaned_rows.append(mapped_data)

                if cleaned_rows:
                    pd.DataFrame(cleaned_rows).to_csv(csv_path, index=False, encoding='utf-8-sig')
                    print(f"  ✅ Converted: {file}")
                    processed_count += 1

            except Exception as e:
                print(f"  ⚠️ Error {file}: {e}")
        
        if skipped_count > 0:
            print(f"     (Skipped {skipped_count} existing files)")

if __name__ == "__main__":
    process_all_robots()