import pandas as pd

# Test reading the data
file_path = "data/cicero-traffic-all-sources-med nyhetsbrev.xlsx"

try:
    # Skip first 2 rows and use row 3 as header (index 2)
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

    print("✅ Data loaded successfully!")
    print(f"\n📊 Statistics:")
    print(f"   - Total articles: {len(df)}")
    print(f"   - Total traffic: {df['Total'].sum():,.0f}")
    print(f"   - Google traffic: {df['Google'].sum():,.0f} ({df['Google'].sum() / df['Total'].sum() * 100:.1f}%)")
    print(f"   - Facebook traffic: {df['Facebook'].sum():,.0f} ({df['Facebook'].sum() / df['Total'].sum() * 100:.1f}%)")
    print(f"   - Newsletter traffic: {df['Newsletter'].sum():,.0f} ({df['Newsletter'].sum() / df['Total'].sum() * 100:.1f}%)")
    print(f"   - ChatGPT traffic: {df['ChatGPT'].sum():,.0f} ({df['ChatGPT'].sum() / df['Total'].sum() * 100:.1f}%)")
    print(f"   - LinkedIn traffic: {df['LinkedIn'].sum():,.0f} ({df['LinkedIn'].sum() / df['Total'].sum() * 100:.1f}%)")

    print(f"\n📈 Top 10 articles by traffic:")
    for idx, row in df.head(10).iterrows():
        print(f"   {idx+1}. {row['Article']}: {row['Total']:,.0f} views")

    print("\n✅ Dashboard is ready to launch!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
