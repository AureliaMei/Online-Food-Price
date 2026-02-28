import pandas as pd
from pathlib import Path

# Set this to the root directory containing your category folders
# '.' assumes you are running the script from within the 'ONLINE FOOD PRICE' folder
root_dir = Path('.') 

all_dfs = []

# Find all 'jevons_price_index.csv' files in all subdirectories
for file_path in root_dir.rglob('jevons_price_index.csv'):
    
    # Read the current CSV
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        print(f"Warning: {file_path} is empty. Skipping.")
        continue

    # Ensure there's a date column and set it as the index for alignment later
    if 'date' not in df.columns:
        print(f"Warning: No 'date' column in {file_path}. Skipping.")
        continue
        
    df.set_index('date', inplace=True)
    
    # Get the name of the folder containing this CSV
    category_folder = file_path.parent.name
    
    # Apply the specific column filter for Baby_product
    if category_folder == 'Baby_product':
        target_col = 'Sữa Bột - Sữa Dinh Dưỡng'
        if target_col in df.columns:
            # Keep ONLY the target column as a DataFrame
            df = df[[target_col]]
        else:
            print(f"Warning: '{target_col}' not found in Baby_product. Skipping.")
            continue
            
    all_dfs.append(df)

# Combine and calculate
if all_dfs:
    # Concatenate all DataFrames horizontally (axis=1).
    # This automatically aligns all data by the 'date' index. 
    # Missing dates for certain subcategories will be filled with NaN.
    combined_df = pd.concat(all_dfs, axis=1)
    
    # Calculate the average across all subcategory columns for each row (day).
    # .mean(axis=1) automatically ignores NaN values, so it correctly averages 
    # only the available subcategories for that specific day.
    daily_average_index = combined_df.mean(axis=1).reset_index()
    
    # Rename columns and sort by date
    daily_average_index.columns = ['date', 'overall_average_index']
    daily_average_index.sort_values('date', inplace=True)
    
    # Save the final aggregated data
    output_filename = 'overall_daily_average_index.csv'
    daily_average_index.to_csv(output_filename, index=False)
    
    print(f"Successfully processed files. Aggregated index saved to '{output_filename}'")
    print("\nPreview of the data:")
    print(daily_average_index.head())
else:
    print("No data was found or processed. Check your directory path and file names.")