import pandas as pd
from pathlib import Path

# Set the root directory explicitly
root_dir = Path('/Users/my/Online Food Price')

all_dfs = []

# Find all 'jevons_price_index.csv' files in all subdirectories
for file_path in root_dir.rglob('jevons_price_index.csv'):
    
    # Read the current CSV
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        print(f"Warning: {file_path} is empty. Skipping.")
        continue

    # Ensure there's a date column
    if 'date' not in df.columns:
        print(f"Warning: No 'date' column in {file_path}. Skipping.")
        continue
        
    # Get the name of the folder containing this CSV
    category_folder = file_path.parent.name
    
    # Apply the specific column filter for Baby_product
    if category_folder == 'Baby_product':
        target_col = 'Sữa Bột - Sữa Dinh Dưỡng'
        if target_col in df.columns:
            # Keep the date and ONLY the target column
            df = df[['date', target_col]]
        else:
            print(f"Warning: '{target_col}' not found in Baby_product. Skipping.")
            continue
            
    # Group by date to prevent the InvalidIndexError from duplicate days
    df = df.groupby('date').mean()
    all_dfs.append(df)

# Combine and calculate
if all_dfs:
    # Concatenate all DataFrames horizontally (axis=1).
    combined_df = pd.concat(all_dfs, axis=1)
    
    # Define your specific staple subcategories
    staple_targets = ['Gạo - Nông Sản Khô', 'Ngũ Cốc - Yến Mạch']
    
    # Automatically categorize the columns into Staples vs Other Food
    staple_cols = [col for col in combined_df.columns if col in staple_targets]
    other_cols = [col for col in combined_df.columns if col not in staple_targets]
    
    # Create a new DataFrame for the final output
    final_df = pd.DataFrame(index=combined_df.index)
    
    # 1. Overall Average (Everything)
    final_df['overall_average_index'] = combined_df.mean(axis=1)
    
    # 2. Staples Average
    if staple_cols:
        final_df['staples_average_index'] = combined_df[staple_cols].mean(axis=1)
    else:
        print("Warning: Could not find Staple columns in the parsed data.")
        
    # 3. Other Food Average (Everything minus Staples)
    if other_cols:
        final_df['other_food_average_index'] = combined_df[other_cols].mean(axis=1)
        
    # Reset index to make 'date' a standard column again and sort
    final_df.reset_index(inplace=True)
    final_df.sort_values('date', inplace=True)
    
    # Save the final aggregated data
    output_filename = root_dir / 'overall_daily_average_index.csv'
    final_df.to_csv(output_filename, index=False)
    
    print(f"Successfully processed files. Aggregated indices saved to '{output_filename.name}'")
    print("\nPreview of the final data:")
    print(final_df.head())
else:
    print("No data was found or processed. Check your directory path and file names.")