from openmeteopy import OpenMeteo
from openmeteopy.options import EcmwfOptions
from openmeteopy.hourly import HourlyEcmwf
from openmeteopy.utils.constants import *
import json
import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
from files_utils import appendFile
import os

def updateWeatherContext():
    data = getWeatherContext(os.getenv("LATITUDE"), os.getenv("LONGITUDE"))
    appendFile(os.getenv("WEATHER_CONTEXT_PATH"), data)

def getWeatherContext(latitude, longitude):
    """
    Fetches daily weather data from Open-Meteo API and formats it into a text string.

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.

    Returns:
        A text string containing the formatted weather forecast.
    """
    try:
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration", "precipitation_sum", "wind_speed_10m_max"],
            "timezone": "America/Chicago",
            "forecast_days": 10
        }
        responses = openmeteo.weather_api(url, params=params)

        response = responses[0]

        text_output = f"Weather Forecast for\n"
        text_output += f"Timezone: {response.Timezone()} {response.TimezoneAbbreviation()}\n"
        text_output += f"Unit: Temperature - Farenheit; daylight or sunshine duration - seconds; precipitation - mm; Wind Speed - m/s\n"

        daily = response.Daily()
        daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
        daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
        daily_sunrise = daily.Variables(2).ValuesAsNumpy()
        daily_sunset = daily.Variables(3).ValuesAsNumpy()
        daily_daylight_duration = daily.Variables(4).ValuesAsNumpy()
        daily_sunshine_duration = daily.Variables(5).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(6).ValuesAsNumpy()
        daily_wind_speed_10m_max = daily.Variables(7).ValuesAsNumpy()

        daily_data = {"date": pd.date_range(
            start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
            end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = daily.Interval()),
            inclusive = "left"
        )}

        daily_data["temperature_2m_max"] = daily_temperature_2m_max
        daily_data["temperature_2m_min"] = daily_temperature_2m_min
        daily_data["sunrise"] = daily_sunrise
        daily_data["sunset"] = daily_sunset
        daily_data["daylight_duration"] = daily_daylight_duration
        daily_data["sunshine_duration"] = daily_sunshine_duration
        daily_data["precipitation_sum"] = daily_precipitation_sum
        daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max

        df = pd.DataFrame(daily_data)
        for index, row in df.iterrows():
            date = row['date'].strftime('%Y-%m-%d')
            text_output += f"Date: {date}\n"
            text_output += f"  Max Temperature: {row['temperature_2m_max']}\n"
            text_output += f"  Min Temperature: {row['temperature_2m_min']}\n"
            text_output += f"  Daylight Duration: {row['daylight_duration']}\n"
            text_output += f"  Sunshine Duration: {row['sunshine_duration']}\n"
            text_output += f"  Precipitation: {row['precipitation_sum']}\n"
            text_output += f"  Max Wind Speed: {row['wind_speed_10m_max']}\n"

        return text_output

    except Exception as e:
        return f"An error occurred: {e}"
    
