import pandas as pd
from pathlib import Path
from scipy.stats import gmean
from src.utils import PROJECT_ROOT, extract_date


def run_jevons_index(
    folder_name: str,
    dedup_lookup: bool = False,
    handle_new_subcats: bool = False,
    sort_output_columns: bool = False,
) -> None:
    """
    Chain-link Jevons index calculation for one category.

    Args:
        folder_name:         Category folder name (e.g. "Dairy").
        dedup_lookup:        Deduplicate lookup by product_name keeping last row.
                             Set True for Processed_food.
        handle_new_subcats:  Track subcategories that first appear after day 1.
                             Set True for Processed_food.
        sort_output_columns: Sort subcategory columns alphabetically in output.
                             Set True for Processed_food.

    Reads:  <folder>/CSV/*.csv  and  <folder>/cat_lookup_table.csv
    Writes: <folder>/jevons_price_index.csv
    """
    folder = PROJECT_ROOT / folder_name
    csv_folder = folder / "CSV"
    lookup_file = folder / "cat_lookup_table.csv"
    output_file = folder / "jevons_price_index.csv"

    if not lookup_file.exists():
        print(f"Lookup file not found: {lookup_file}")
        return

    lookup = pd.read_csv(lookup_file, usecols=['product_name', 'subcategory'])
    if dedup_lookup:
        lookup = lookup.drop_duplicates(subset=['product_name'], keep='last')

    files = sorted(csv_folder.glob("*.csv"))
    if not files:
        print(f"No CSV files in {csv_folder}")
        return

    history = {}
    prev_df = None
    prev_date = None
    results = []

    for file in files:
        current_date = extract_date(file.name)
        print(f"Processing: {current_date}")
        try:
            curr_df = pd.read_csv(file, usecols=['product_name', 'final_price'])
            curr_df = curr_df.merge(lookup, on='product_name', how='left')
            curr_df = curr_df.dropna(subset=['subcategory', 'final_price'])

            if prev_df is None:
                day_results = {'date': current_date}
                for sub in curr_df['subcategory'].unique():
                    history[sub] = {current_date: 1.0}
                    day_results[sub] = 1.0
                results.append(day_results)
            else:
                day_results = {'date': current_date}

                for sub in history:
                    p_prev = prev_df[prev_df['subcategory'] == sub][['product_name', 'final_price']]
                    p_curr = curr_df[curr_df['subcategory'] == sub][['product_name', 'final_price']]
                    matched = p_prev.merge(p_curr, on='product_name', suffixes=('_prev', '_curr'))
                    matched = matched[(matched['final_price_prev'] > 0) & (matched['final_price_curr'] > 0)]

                    if not matched.empty:
                        price_relatives = matched['final_price_curr'] / matched['final_price_prev']
                        new_index = history[sub].get(prev_date, 1.0) * gmean(price_relatives)
                        history[sub][current_date] = new_index
                    else:
                        history[sub][current_date] = history[sub].get(prev_date, 1.0)

                    day_results[sub] = history[sub][current_date]

                if handle_new_subcats:
                    for sub in curr_df['subcategory'].unique():
                        if sub not in history:
                            history[sub] = {current_date: 1.0}
                            day_results[sub] = 1.0

                results.append(day_results)

            prev_df = curr_df
            prev_date = current_date

        except Exception as e:
            print(f"  Error processing {file.name}: {e}")

    if results:
        final_df = pd.DataFrame(results)
        if sort_output_columns:
            cols = ['date'] + sorted(c for c in final_df.columns if c != 'date')
            final_df = final_df[cols]
        final_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\nJevons index saved to {output_file.name}")
        print(final_df.tail())
    else:
        print("No results generated.")
