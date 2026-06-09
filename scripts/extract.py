"""
Extract: Fetch weather data from data.gov.sg API
Project: Singapore Heat Stress Analysis
"""

import requests
import json
from datetime import datetime, timedelta
import os

# Configuration
API_URL = "https://api-open.data.gov.sg/v2/real-time/api/air-temperature"
API_KEY = os.getenv('DATA_GOV_SG_API_KEY', 'your_api_key_here')  # Use environment variable

headers = {"X-API-Key": API_KEY}

# Date range for extraction (Oct 1, 2025 to Dec 31, 2025)
start_date = '2025-10-01'
total_days = 92  # October (31) + November (30) + December (31)

# Store all extracted data
all_readings = []
current_date = datetime.strptime(start_date, "%Y-%m-%d")

print(f"Starting extraction for {total_days} days from {start_date}...")

for i in range(total_days):
    date_param = current_date.strftime("%Y-%m-%dT12:00:00")
    url = f"{API_URL}?date={date_param}"
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # Extract stations and readings
        stations = {s["id"]: s for s in data["data"]["stations"]}
        
        for reading_batch in data["data"]["readings"]:
            timestamp = reading_batch["timestamp"]
            for entry in reading_batch["data"]:
                station_info = stations.get(entry["stationId"], {})
                all_readings.append({
                    "timestamp": timestamp,
                    "station_id": entry["stationId"],
                    "station_name": station_info.get("name", ""),
                    "latitude": station_info.get("location", {}).get("latitude"),
                    "longitude": station_info.get("location", {}).get("longitude"),
                    "temperature_c": entry["value"]
                })
        
        print(f"Extracted data for {current_date.strftime('%Y-%m-%d')} - {len(reading_batch['data'])} records")
        
    except requests.exceptions.RequestException as e:
        print(f"Error on {current_date.strftime('%Y-%m-%d')}: {e}")
    
    # Move to next day
    current_date += timedelta(days=1)

print(f"\nExtraction complete. Total records: {len(all_readings)}")

# Save raw data to JSON
with open('../data/raw/air_temp_raw.json', 'w') as f:
    json.dump(all_readings, f, indent=2)

print("Raw data saved to data/raw/air_temp_raw.json")
