import requests
from datetime import datetime, timedelta
from config import *
from zoneinfo import ZoneInfo



# Set up the API endpoint
url = f"https://api.ecowitt.net/api/v3/device/real_time"
params = {
    "api_key": API_KEY,
    "application_key": APP_KEY,
    "mac": MAC,
    "call_back": "all"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Request failed:", response.status_code)

if result_index <= 9:
    print("<p>Оптимальні значення</p>")
elif result_index < 30:
    print("<p>Подразнюючі значення</p>")
else:
    print("<p>Гострі значення</p>")