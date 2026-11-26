# libraries
import json
from pathlib import Path
import time
import requests

# Setup & Paths
# resolve() gives Absolute path & .parents[n] → to move n+1 folders upward from Current file
BASE_DIR = Path(__file__).resolve().parents[2] # Path(__file__) will find file on its own
RAW_DIR = BASE_DIR / "data" / "raw" # just the location / path where that file will be saved
RAW_DIR.mkdir(parents=True, exist_ok=True) # Folder creation: now all the above mentioned folders will be actually created here

# Configuration (Coordinates, URL aur Params)
LATITUDE = 24.8607
LONGITUDE = 67.0011

weather_url = "https://api.open-meteo.com/v1/forecast" # API endpoint for weather data where we will send our request to get the data
# Query Parameters[Parameters for the API request, telling the API what data we want to retrieve]
weather_params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "precipitation",
        "precipitation_probability",
        "uv_index",
        "wind_speed_10m",
        "wind_direction_10m",
    ],
    "timezone": "Asia/Karachi",
    "forecast_days": 1,
}

air_url = "https://air-quality-api.open-meteo.com/v1/air-quality" # API endpoint for air quality data where we will send our request to get the data
# Query Parameters[Parameters for the API request, telling the API what data we want to retrieve]
air_params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "hourly": ["us_aqi", "pm2_5", "pm10"],
    "timezone": "Asia/Karachi",
    "forecast_days": 1,
}

# Function to fetch data from the API with retry mechanism
def fetch_data(url, params, retries=3):
    for attempt in range(1, retries + 1):  # (include, exclude) → 1, 2, 3
        try: 
            response = requests.get(url, params=params, timeout=60)
            response.raise_for_status()
            return response.json() # .json() converts the JSON response into a Python dictionary.
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(3)
            else:
                raise

# Execution & Saving 
def main():
    print("Fetching Karachi weather data...")
    weather_data = fetch_data(weather_url, weather_params)

    print("Fetching Karachi air quality data...")
    air_data = fetch_data(air_url, air_params)

    with open(RAW_DIR / "karachi_weather.json", "w", encoding="utf-8") as file:
        json.dump(weather_data, file, indent=4) # .dump() → converts the Python dictionary into a JSON string and writes it to the file. indent=4 → makes the JSON output more readable by adding indentation.

    with open(RAW_DIR / "karachi_air_quality.json", "w", encoding="utf-8") as file:
        json.dump(air_data, file, indent=4)

    print("\nBoth API requests succeeded!")
    print(f"Raw files saved in: {RAW_DIR}")


if __name__ == "__main__":
    main()