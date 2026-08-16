import json
import os
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from prefect import flow, task

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("AIRNOW_API_KEY")
BRONZE_DIR = BASE_DIR / "data" / "bronze" / "airnow_live"

CITIES = {
    "fort_wayne_in": (41.0793, -85.1394),
    "chicago_il":    (41.8781, -87.6298),
}


@task
def pull_airnow(city_name, lat, lon):
    print(f"  Pulling AirNow data for {city_name}...")
    url = (
        f"https://www.airnowapi.org/aq/observation/latLong/current/"
        f"?format=application/json"
        f"&latitude={lat}&longitude={lon}"
        f"&distance=25&API_KEY={API_KEY}"
    )
    response = requests.get(url)
    return city_name, response.status_code, response.json()


@task
def validate(city_name, status_code, data):
    print(f"  Validating {city_name}...")
    assert status_code == 200, f"HTTP error: {status_code}"
    assert len(data) > 0, f"No records returned for {city_name}"
    print(f"  {city_name} — OK — {len(data)} records")
    return True


@task
def save_to_bronze(city_name, data):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    filename = BRONZE_DIR / f"airnow_{city_name}_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Saved: {filename.name}")


@flow(name="AirHealth Daily AirNow Pipeline")
def daily_airnow_pipeline():
    print("Starting daily AirNow pipeline...")
    for city_name, (lat, lon) in CITIES.items():
        city_name, status_code, data = pull_airnow(city_name, lat, lon)
        is_valid = validate(city_name, status_code, data)
        if is_valid:
            save_to_bronze(city_name, data)
    print("\nPipeline complete.")


if __name__ == "__main__":
    daily_airnow_pipeline()