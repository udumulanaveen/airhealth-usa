# Data Sources

---

## 1. AirNow API — Live AQI

- **Source:** US EPA AirNow API
- **URL:** https://www.airnowapi.org/aq/observation/latLong/current/
- **Phase:** 1
- **Key required:** Yes — free registration at airnowapi.org
- **Update frequency:** Hourly
- **Coverage:** 12 US cities (Fort Wayne IN, Chicago IL, New York NY, 
  Los Angeles CA, Houston TX, Phoenix AZ, Denver CO, Seattle WA, 
  Atlanta GA, Detroit MI, Miami FL, Minneapolis MN)

### Schema

| Field | Type | Description |
|---|---|---|
| DateObserved | string | Date of the reading |
| HourObserved | integer | Hour in local time |
| LocalTimeZone | string | Timezone of the monitoring station |
| ReportingArea | string | City or reporting area name |
| StateCode | string | Two-letter US state code |
| Latitude | float | Station latitude |
| Longitude | float | Station longitude |
| ParameterName | string | Pollutant measured — O3 or PM2.5 |
| AQI | integer | Air Quality Index value, range 0-500 |
| Category.Number | integer | 1=Good 2=Moderate 3=Unhealthy for Sensitive Groups 4=Unhealthy 5=Very Unhealthy 6=Hazardous |
| Category.Name | string | Human readable AQI category label |

### Notes
- Category field is nested in raw JSON — will be flattened in silver layer
- Each API call returns one row per pollutant per location
- Bronze files saved as: airnow_{city}_{YYYY_MM_DD_HHMMSS}.json
- AQI values update hourly — rerunning script creates new file, never overwrites


## EPA AirData — Daily AQI by County

- Source: https://aqs.epa.gov/aqsweb/airdata/download_files.html
- Download date: 2026-06-21
- Files: daily_aqi_by_county_2021.csv through daily_aqi_by_county_2025.csv
- Location: data/bronze/epa_airdata/
- Total rows: ~1.5 million across 5 files
- Grain: one row per county per day

### Columns
| Field | Type | Notes |
|---|---|---|
| State Name | string | Full state name |
| county Name | string | County name — lowercase c, EPA inconsistency |
| State Code | integer | Numeric state FIPS code |
| County Code | integer | Numeric county FIPS code |
| Date | string | YYYY-MM-DD format, read as string in bronze |
| AQI | integer | Air Quality Index 0-500 |
| Category | string | Good / Moderate / Unhealthy etc. |
| Defining Parameter | string | Pollutant that drove the AQI value |
| Defining Site | string | Monitoring station ID |
| Number of Sites Reporting | integer | Count of stations contributing |

### Validation Notes
- 54 distinct states including DC and US territories
- Zero null AQI values across all years
- 2025 file is partial — runs through 2025-11-13