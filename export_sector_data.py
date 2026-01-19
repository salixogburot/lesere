import pandas as pd
import json
import os
import math

# Read the Excel file
file_path = "data/clicks_per_url_by_sector affinity og utgave.xlsx"

# Read the main sheet
df = pd.read_excel(file_path, sheet_name='totalt')

# Replace NaN values with None for valid JSON
df = df.where(pd.notnull(df), None)

print(f"✅ Loaded data from '{file_path}'")
print(f"   Shape: {df.shape}")
print(f"   Columns: {len(df.columns)}")

# Convert to JSON
data_json = df.to_dict('records')

# Clean NaN and Inf values for valid JSON
def clean_value(value):
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
    return value

# Replace NaN/Inf with None in all records
cleaned_data = []
for record in data_json:
    cleaned_record = {k: clean_value(v) for k, v in record.items()}
    cleaned_data.append(cleaned_record)

# Create docs directory if it doesn't exist
os.makedirs('docs', exist_ok=True)

# Export to JSON
output_file = 'docs/sector_data.json'
with open(output_file, 'w') as f:
    json.dump(cleaned_data, f, indent=2)

print(f"\n✅ Exported {len(data_json)} articles to {output_file}")

# Calculate statistics
total_clicks = df['total_clicks'].sum()
avg_clicks = df['total_clicks'].mean()

# Get sector columns (those ending with _ratio)
sector_columns = [col.replace('_ratio', '') for col in df.columns if col.endswith('_ratio')]

print(f"\n📊 Statistics:")
print(f"   - Total articles: {len(df)}")
print(f"   - Total clicks: {total_clicks:,.0f}")
print(f"   - Average clicks per article: {avg_clicks:.1f}")
print(f"   - Number of sectors: {len(sector_columns)}")
print(f"\n📈 Sectors tracked:")
for sector in sector_columns:
    if sector in df.columns:
        sector_clicks = df[sector].sum()
        pct = (sector_clicks / total_clicks * 100) if total_clicks > 0 else 0
        print(f"   - {sector}: {sector_clicks:,.0f} clicks ({pct:.1f}%)")

print("\n✅ Data export complete!")
