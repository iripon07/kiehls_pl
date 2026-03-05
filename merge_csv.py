import pandas as pd
import os

file_paths = [
    "kiehls_pl/kiehls_stores_poland.csv",
    "kiehls_sk/kiehls_stores_slovakia.csv",
    "kiehls_hu/kiehls_stores_hungary.csv",
    "kiehls_hr/kiehls_stores_croatia.csv",
    "kiehls_cz/kiehls_stores_czech.csv",
    "kiehls_bg/kiehls_stores_bulgaria.csv",
]

df_list = []

for path in file_paths:
    if os.path.exists(path):
        print(f"Loading: {path}")
        # Standardizing encoding to utf-8 for European characters
        temp_df = pd.read_csv(path, encoding="utf-8", low_memory=False)

        # We append the dataframe directly without adding any new columns
        df_list.append(temp_df)
    else:
        print(f"Warning: File not found at {path}")

if df_list:
    # Concatenate all dataframes into one
    # ignore_index=True ensures a clean 0-N index for the final file
    merged_df = pd.concat(df_list, axis=0, ignore_index=True, sort=False)

    output_name = "kiehls_stores_data.csv"

    # Save with utf-8 encoding to preserve Polish, Czech, and Bulgarian characters
    merged_df.to_csv(output_name, index=False, encoding="utf-8")

    print(f"\nSuccess! Merged {len(df_list)} files into '{output_name}'.")
    print(f"Total Rows: {len(merged_df)}")
else:
    print("No files were found to merge.")
