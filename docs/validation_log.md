## Phase 0 — Project Setup

- git status: nothing to commit, working tree clean
- ls data/bronze/: airnow_live, cdc_health, epa_airdata, weather all present
- .gitignore confirms data/** pattern is in place
- First commit: fc87fea — Initialize AirHealth USA project structure
- GitHub push: confirmed at https://github.com/udumulanaveen/airhealth-usa
- Decision: used .venv for isolation, python3 consistently over python

---

## Phase 1 — AirNow API Live Ingestion
Date: 2026-06-21

### Validations

| Check | Command | Result |
|---|---|---|
| API key loads from .env | python3 -c "from dotenv import load_dotenv..." | Key printed correctly |
| HTTP status all cities | python3 ingestion/airnow_api_ingest.py | 200 for all 12 cities |
| Files saved to bronze | ls data/bronze/airnow_live/ | 24 files after 2 runs |
| No overwrite on rerun | ls data/bronze/airnow_live/ wc -l | 12 new files per run |
| JSON schema inspected | cat airnow_fort_wayne_in_...json | 2 records, all fields present |
| Schema documented | cat docs/data_sources.md | 11 fields documented |

### Observations
- Each city returns 2-3 records depending on pollutants monitored
- 12 cities across all US regions — 32 total records per run
- Category field is nested — will flatten in silver layer
- Fort Wayne O3 changed from 25 to 35 between runs — confirms live data
- Total records saved across 2 runs: 64

### Status: COMPLETE

## Phase 2 — EPA AirData Historical Backfill

Date: 2026-06-21

### Files Downloaded
- daily_aqi_by_county_2021.csv — 326,540 rows
- daily_aqi_by_county_2022.csv — 324,419 rows
- daily_aqi_by_county_2023.csv — 325,399 rows
- daily_aqi_by_county_2024.csv — 329,166 rows
- daily_aqi_by_county_2025.csv — 213,103 rows (partial year through 2025-11-13)
- Total: ~1.5 million rows

### Validation Results
- All files land in data/bronze/epa_airdata/ untouched
- Date ranges confirmed correct for all 5 years
- Distinct states: 54 (50 states + DC + territories)
- Null AQI values: 0 across all files
- Loader script runs without error: ingestion/epa_airdata_loader.py

### Decisions
- Bronze files kept as-is — no modification
- Date column left as string in bronze — will cast to date type in silver layer
- county Name lowercase inconsistency noted — will standardize in silver layer