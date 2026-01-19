import pandas as pd
import sys

# Read the Excel file
file_path = "data/clicks_per_url_by_sector affinity og utgave.xlsx"

try:
    # Read all sheets
    excel_file = pd.ExcelFile(file_path)
    print(f"Sheet names: {excel_file.sheet_names}\n")

    # Read the first sheet without header to see structure
    df_raw = pd.read_excel(file_path, sheet_name=0, header=None)
    print("First 10 rows (raw):")
    print(df_raw.head(10))
    print("\n" + "="*80 + "\n")

    # Try reading with default header
    df = pd.read_excel(file_path, sheet_name=0)
    print(f"Shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}\n")

    # Display first rows with all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_rows', 20)
    print(f"First 15 rows:\n{df.head(15)}\n")

    print(f"\nData types:\n{df.dtypes}\n")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
