import duckdb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "airhealth_usa.duckdb"

con = duckdb.connect(str(DB_PATH))

print("=== raw_airnow ===")
print(con.execute("SELECT COUNT(*) AS total_rows FROM raw_airnow").df())
print(con.execute("SELECT DISTINCT StateCode FROM raw_airnow ORDER BY StateCode").df())

print("=== raw_epa_aqi ===")
print(con.execute("SELECT COUNT(*) AS total_rows FROM raw_epa_aqi").df())
print(con.execute("SELECT MIN(Date) AS min_date, MAX(Date) AS max_date FROM raw_epa_aqi").df())
print(con.execute("SELECT COUNT(DISTINCT \"State Name\") AS distinct_states FROM raw_epa_aqi").df())

con.close()
