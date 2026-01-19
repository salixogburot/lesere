import pandas as pd
import sys

# Read the Excel file
file_path = "data/cicero-traffic-all-sources-med nyhetsbrev.xlsx"

try:
    # Read without header to see raw data
    df_raw = pd.read_excel(file_path, sheet_name=0, header=None)
    print("First 5 rows (raw):")
    print(df_raw.head(5))
    print("\n" + "="*80 + "\n")

    # Now read with proper header
    df = pd.read_excel(file_path, sheet_name=0)
    print(f"Shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}\n")

    # Display first rows with all columns
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(f"First 10 rows:\n{df.head(10)}\n")

    print(f"\nData types:\n{df.dtypes}\n")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
