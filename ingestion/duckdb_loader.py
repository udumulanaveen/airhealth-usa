import duckdb
from pathlib import Path

# so the script works from any directory
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "airhealth_usa.duckdb"
AIRNOW_PATH = BASE_DIR / "data" / "bronze" / "airnow_live" / "airnow_*.json"
EPA_PATH = BASE_DIR / "data" / "bronze" / "epa_airdata" / "daily_aqi_by_county_*.csv"

def load_airnow(con):
    print("Loading AirNow JSON files into raw_airnow...")
    con.execute(f"""
        CREATE OR REPLACE TABLE raw_airnow AS
        SELECT
            DateObserved,
            HourObserved,
            LocalTimeZone,
            ReportingArea,
            StateCode,
            Latitude,
            Longitude,
            ParameterName,
            AQI,
            Category.Number AS category_number,
            Category.Name   AS category_name
        FROM read_json_auto('{AIRNOW_PATH}')
    """)
    count = con.execute("SELECT COUNT(*) FROM raw_airnow").fetchone()[0]
    print(f"  raw_airnow loaded: {count} rows")


def load_epa(con):
    print("Loading EPA CSV files into raw_epa_aqi...")
    con.execute(f"""
        CREATE OR REPLACE TABLE raw_epa_aqi AS
        SELECT *
        FROM read_csv_auto('{EPA_PATH}', header=true)
    """)
    count = con.execute("SELECT COUNT(*) FROM raw_epa_aqi").fetchone()[0]
    print(f"  raw_epa_aqi loaded: {count} rows")

def export_to_parquet(con):
    print("\nExporting to Parquet...")

    airnow_parquet = BASE_DIR / "data" / "silver" / "raw_airnow.parquet"
    epa_parquet = BASE_DIR / "data" / "silver" / "raw_epa_aqi.parquet"

    con.execute(f"COPY raw_airnow TO '{airnow_parquet}' (FORMAT PARQUET)")
    print(f"  Saved: {airnow_parquet}")

    con.execute(f"COPY raw_epa_aqi TO '{epa_parquet}' (FORMAT PARQUET)")
    print(f"  Saved: {epa_parquet}")


def main():
    print(f"Connecting to DuckDB at: {DB_PATH}")
    con = duckdb.connect(str(DB_PATH))

    load_airnow(con)
    load_epa(con)
    export_to_parquet(con)

    print("\nTables in database:")
    tables = con.execute("SHOW TABLES").fetchall()
    for table in tables:
        print(f"  {table[0]}")

    con.close()
    print("\nDone.")


if __name__ == "__main__":
    main()