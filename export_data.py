import pandas as pd
import json

# Read and prepare the data
file_path = "data/cicero-traffic-all-sources-med nyhetsbrev.xlsx"

# Skip first 2 rows and use row 3 as header
df = pd.read_excel(file_path, sheet_name=0, skiprows=[0, 1])

# Rename columns to clean names
df.columns = ['Article', 'Total', 'Google', 'Facebook', 'Newsletter', 'ChatGPT',
              'LinkedIn', 'Pct_Google', 'Pct_Facebook', 'Pct_Newsletter',
              'Pct_ChatGPT', 'Pct_LinkedIn']

# Convert numeric columns
numeric_cols = ['Total', 'Google', 'Facebook', 'Newsletter', 'ChatGPT', 'LinkedIn',
                'Pct_Google', 'Pct_Facebook', 'Pct_Newsletter', 'Pct_ChatGPT', 'Pct_LinkedIn']

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove rows with missing Article names
df = df.dropna(subset=['Article'])

# Sort by Total traffic
df = df.sort_values('Total', ascending=False).reset_index(drop=True)

# Convert to JSON
data_json = df.to_dict('records')

# Create docs directory if it doesn't exist
import os
os.makedirs('docs', exist_ok=True)

# Export to JSON
with open('docs/traffic_data.json', 'w') as f:
    json.dump(data_json, f, indent=2)

print(f"✅ Exported {len(data_json)} articles to docs/traffic_data.json")
print(f"📊 Total traffic: {df['Total'].sum():,.0f}")
