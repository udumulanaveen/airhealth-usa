## Phase 5 — Streamlit Dashboard and EDA

Date: 2026-08-15

### Validations

| Check | Command | Result |
|---|---|---|
| App starts | streamlit run dashboard/streamlit_app.py | Runs without error, opens at localhost:8501 |
| Charts load | Visual check in browser | All 6 views render: national overview, current AQI by city, AQI trend by state, worst AQI days, category distribution, PM2.5 vs O3 trend |
| Filters work | Changed state/date range in sidebar | Charts and tables update correctly |
| Numbers match independent query | python3 -c "... GROUP BY state_name ..." vs chart hover | Top 5 states matched exactly: California 54.02, DC 49.65, Arizona 49.38, Utah 49.19, Oklahoma 47.17 |
| Jupyter installed | jupyter notebook --version | 7.6.0 |
| EDA notebook runs | notebooks/01_aqi_eda.ipynb, run top to bottom | No errors — describe() and groupby queries return expected results |
| Deployed URL opens publicly | (pending) | Not yet deployed |

### Findings

1. Mono County, CA shows extreme PM10 spikes (max_aqi up to 8368, far beyond the normal 0–500 AQI scale), concentrated in spring months (April–June account for 59% of occurrences). This matches known windblown dust events from the dry Mono/Owens Lake basin — a real environmental phenomenon, not a data pipeline error.
2. Contrary to the common assumption that PM2.5 peaks in winter, this dataset shows both PM2.5 and ozone AQI peaking together in summer (June–August). Likely explanation: US wildfire season (smoke → PM2.5) overlaps with peak ozone-forming heat and sunlight conditions.
3. California has the highest average AQI of any state (54.0) across 2021–2025, followed by District of Columbia (49.7), Arizona (49.4), Utah (49.2), and Oklahoma (47.2) — confirmed against an independent DuckDB query, not just the dashboard chart.

### Decisions
- Excluded "Country Of Mexico" (a non-US entry in EPA's state_name field) from the National Overview chart — a border-monitoring artifact, not a real state.
- National Overview limited to the worst 20 states, not all 54 — the full list was mostly uniform green and less readable.
- National Overview and Pollutant Trends charts are intentionally unfiltered by the sidebar (always show the full picture); Trend, Worst Days, and Category Distribution respect the state/date filters.

Change the row | Deployed URL opens publicly | (pending) | Not yet deployed | to:
| Deployed URL opens publicly | https://airhealth-usa-k5mbdcjcabhqjaysvjvrpz.streamlit.app | Confirmed — live and public, all 6 views render with real data |
Change ### Status: IN PROGRESS — dashboard and EDA complete, deployment to Streamlit Community Cloud pending to:
### Status: COMPLETE

### Status: IN PROGRESS — dashboard and EDA complete, deployment to Streamlit Community Cloud pending