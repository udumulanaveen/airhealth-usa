import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("AIRNOW_API_KEY")

# Cities across all US regions
CITIES = [
    {"name": "fort_wayne_in",   "lat": 41.0793, "lon": -85.1394},
    {"name": "chicago_il",      "lat": 41.8781, "lon": -87.6298},
    {"name": "new_york_ny",     "lat": 40.7128, "lon": -74.0060},
    {"name": "los_angeles_ca",  "lat": 34.0522, "lon": -118.2437},
    {"name": "houston_tx",      "lat": 29.7604, "lon": -95.3698},
    {"name": "phoenix_az",      "lat": 33.4484, "lon": -112.0740},
    {"name": "denver_co",       "lat": 39.7392, "lon": -104.9903},
    {"name": "seattle_wa",      "lat": 47.6062, "lon": -122.3321},
    {"name": "atlanta_ga",      "lat": 33.7490, "lon": -84.3880},
    {"name": "detroit_mi",      "lat": 42.3314, "lon": -83.0458},
    {"name": "miami_fl",        "lat": 25.7617, "lon": -80.1918},
    {"name": "minneapolis_mn",  "lat": 44.9778, "lon": -93.2650},
]

timestamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")
total_records = 0

for city in CITIES:
    url = (
        f"https://www.airnowapi.org/aq/observation/latLong/current/"
        f"?format=application/json"
        f"&latitude={city['lat']}"
        f"&longitude={city['lon']}"
        f"&distance=50"
        f"&API_KEY={API_KEY}"
    )

    response = requests.get(url)
    records = response.json()

    filename = os.path.join(BASE_DIR, "data", "bronze", "airnow_live", f"airnow_{city['name']}_{timestamp}.json")

    with open(filename, "w") as f:
        json.dump(records, f, indent=2)

    print(f"[{response.status_code}] {city['name']} — {len(records)} records — {filename}")
    total_records += len(records)

print(f"\nDone. Total records saved: {total_records}")