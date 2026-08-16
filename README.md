# AirHealth USA

**Air Quality × Weather × Public Health — Data Engineering Platform**

A full-stack data engineering project that ingests, models, and analyzes US air quality data alongside weather and public health indicators.

## Live Dashboard
https://airhealth-usa-k5mbdcjcabhqjaysvjvrpz.streamlit.app

## What This Project Builds
- Live AQI ingestion pipeline from the AirNow API
- Historical backfill from EPA AirData
- Local data warehouse using DuckDB + Parquet (bronze/silver/gold)
- SQL transformations with dbt Core
- Scheduled daily pipeline using Prefect
- Interactive dashboard in Streamlit
- Weather and CDC public health joins
- ML models tracked with MLflow, served via FastAPI

## Tools
Python · DuckDB · Parquet · dbt Core · Prefect · Great Expectations · Streamlit · MLflow · FastAPI

## Data Sources
- AirNow API (live AQI)
- EPA AirData (historical AQI)
- Open-Meteo (weather)
- CDC PLACES (public health)

## Status
- Phase 0 — Project setup — complete
- Phase 1 — AirNow live AQI ingestion — complete
- Phase 2 — EPA AirData historical backfill — complete
- Phase 3 — DuckDB + Parquet local warehouse — complete
- Phase 4 — dbt Core star schema and gold marts — complete
- Phase 5 — Streamlit dashboard and EDA — complete
- Phase 6 — Open-Meteo weather integration — next