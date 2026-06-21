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