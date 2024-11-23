import requests
from datetime import datetime, timedelta
from config import *
from zoneinfo import ZoneInfo


now = datetime.now()
five_minutes_earlier = now - timedelta(minutes=5)
x_hours_earlier = now - timedelta(hours=24)

# Format
five_min_formatted = five_minutes_earlier.strftime("%Y-%m-%d %H:%M:%S")
x_hours_formatted = x_hours_earlier.strftime("%Y-%m-%d %H:%M:%S")

# Set up the API endpoint
url = f"https://api.ecowitt.net/api/v3/device/history"
params = {
    "api_key": API_KEY,
    "application_key": APP_KEY,
    "mac": MAC,
    "start_date": x_hours_formatted,
    "end_date": five_min_formatted, 
    "temp_unitid": "1",
    "pressure_unitid": "3",
    "wind_speed_unitid": "6",
    "call_back": "outdoor.temperature,outdoor.humidity,wind.wind_speed,pressure"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Request failed:", response.status_code)
