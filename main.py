import requests
from datetime import datetime, timedelta
from config import *
import json

def apply_formula (data):
    temperature_json = data["data"]["outdoor"]["temperature"]["list"]
    temperature_list = list(temperature_json.values())
    t_old = float(temperature_list[0])
    t = float(temperature_list[-1])
    del_t = abs(t_old - t)
    
    humidity_json = data["data"]["outdoor"]["humidity"]["list"]
    humidity_list = list(humidity_json.values())
    f = float(humidity_list[-1])

    wind_json = data["data"]["wind"]["wind_speed"]["list"]
    wind_list = list(wind_json.values())
    v = float(wind_list[-1])

    pressure_json = data["data"]["pressure"]["relative"]["list"]
    pressure_list = list(pressure_json.values())
    p_old = float(pressure_list[0])
    p = float(pressure_list[-1])
    del_p = abs(p_old - p)

    if t <= 18:
        i_t = 0.02 * (18 - t)**2
    else:
        i_t = 0.2 * (t - 18)**2
    i_f = (f - 70) / 2
    i_v = 0.2 * v ** 2
    i_del_t = 0.3 * del_t**2
    i_del_p = 0.06 * del_p**2

    I_total = i_t + i_f + i_v + i_del_t + i_del_p
    return round(I_total, 2)

# get current time and format it
now = datetime.now()
five_minutes_earlier = now - timedelta(minutes=5)
x_hours_earlier = now - timedelta(hours=24)
# Format
five_min_formatted = five_minutes_earlier.strftime("%Y-%m-%d %H:%M:%S")
x_hours_formatted = x_hours_earlier.strftime("%Y-%m-%d %H:%M:%S")

print(f"<p>Оновлено: {five_min_formatted}</p>")

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

# Check for successful response
if response.status_code == 200:
    data = response.json()
    result_index = apply_formula(data)
    print(f"<p>Значення індексу Бокші: <b>{result_index}</b></p>")
else:
    print("Request failed:", response.status_code)

if result_index <= 9:
    print("<p>Оптимальні значення</p>")
elif result_index < 30:
    print("<p>Подразнюючі значення</p>")
else:
    print("<p>Гострі значення</p>")