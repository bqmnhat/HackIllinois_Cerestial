import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 40,
    "longitude": -88,
    "current": ["temperature_2m", "relative_humidity_2m", "is_day", "precipitation", "rain", "snowfall", "wind_speed_10m", "weather_code"],
    "hourly": ["temperature_2m", "precipitation_probability", "snowfall", "cloud_cover", "wind_speed_80m", "soil_temperature_18cm", "soil_moisture_3_to_9cm", "weather_code"],
    "timezone": "America/Chicago",
    "forecast_days": 1
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

def get_current_weather():
    
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")


    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()

    current_temperature_2m = current.Variables(0).Value()

    current_relative_humidity_2m = current.Variables(1).Value()

    current_is_day = current.Variables(2).Value()

    current_precipitation = current.Variables(3).Value()

    current_rain = current.Variables(4).Value()

    current_snowfall = current.Variables(5).Value()
    
    current_wind_speed_10m = current.Variables(6).Value()
    
    current_weather_code = current.Variables(7).Value()

    current_weather_dict = {
    "temperature_2m": current_temperature_2m,
    "relative_humidity_2m": current_relative_humidity_2m,
    "is_day": current_is_day,
    "precipitation": current_precipitation,
    "rain": current_rain,
    "snowfall": current_snowfall,
    "wind_speed_10m": current_wind_speed_10m,
    "weather_code": current_weather_code
    }

    #current_dataframe = pd.DataFrame(data = current_weather_dict)
    
    return current_weather_dict

    # print(f"Current time {current.Time()}")

    # print(f"Current  {current_}")
    # # Process minutely_15 data. The order of variables needs to be the same as requested.
    # minutely_15 = response.Minutely15()
    # minutely_15_ = minutely_15.Variables(0).ValuesAsNumpy()

    # minutely_15_data = {"date": pd.date_range(
    # 	start = pd.to_datetime(minutely_15.Time(), unit = "s", utc = True),
    # 	end = pd.to_datetime(minutely_15.TimeEnd(), unit = "s", utc = True),
    # 	freq = pd.Timedelta(seconds = minutely_15.Interval()),
    # 	inclusive = "left"
    # )}

    # minutely_15_data[""] = minutely_15_

    # minutely_15_dataframe = pd.DataFrame(data = minutely_15_data)
    # print(minutely_15_dataframe)

    # Process hourly data. The order of variables needs to be the same as requested.
def get_24h_weather():
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(2).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_speed_80m = hourly.Variables(4).ValuesAsNumpy()
    hourly_soil_temperature_18cm = hourly.Variables(5).ValuesAsNumpy()
    hourly_soil_moisture_3_to_9cm = hourly.Variables(6).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(7).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["precipitation_probability"] = hourly_precipitation_probability
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["cloud_cover"] = hourly_cloud_cover
    hourly_data["wind_speed_80m"] = hourly_wind_speed_80m
    hourly_data["soil_temperature_18cm"] = hourly_soil_temperature_18cm
    hourly_data["soil_moisture_3_to_9cm"] = hourly_soil_moisture_3_to_9cm
    hourly_data["weather_code"] = hourly_weather_code

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    return hourly_dataframe
    # print(hourly_dataframe)

    # Process daily data. The order of variables needs to be the same as requested.
    # daily = response.Daily()
    # daily_ = daily.Variables(0).ValuesAsNumpy()

    # daily_data = {"date": pd.date_range(
    # 	start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
    # 	end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
    # 	freq = pd.Timedelta(seconds = daily.Interval()),
    # 	inclusive = "left"
    # )}

    # daily_data[""] = daily_

    # daily_dataframe = pd.DataFrame(data = daily_data)
    # print(daily_dataframe)