import pandas as pd
import glob
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRONZE_PATH = os.path.join(BASE_DIR, "data", "bronze", "epa_airdata")

files = sorted(glob.glob(os.path.join(BRONZE_PATH, "daily_aqi_by_county_*.csv")))

for filepath in files:
    filename = os.path.basename(filepath)
    df = pd.read_csv(filepath)
    print(f"\n--- {filename} ---")
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"Distinct states: {df['State Name'].nunique()}")
    print(f"Null AQI values: {df['AQI'].isnull().sum()}")