import requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
from meteostat import Point, Daily
import numpy as np


api_key = "c89dc689f952d6b8abcbafe9569fbc8f"
city = "tallinn"


def get_weather(city):
    api_key = "60aa068482d6ddc251ae5f53570ac5fb"
    units = "metric"
    # MERGING API URL
    weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?q="
        + city
        + "&appid="
        + api_key
        + "&units="
        + units
        + "&mode=json"
    )
    weather_data = requests.get(weather_url).json()

    return weather_data


def get_coordinates(city="tallinn"):
    global coordinate_data
    # MERGING Coordinates API URL
    coordinates_url = (
        "http://api.openweathermap.org/geo/1.0/direct?q="
        + city
        + ","
        + get_weather(city)["sys"]["country"]
        + "&limit=1&appid="
        + api_key
    )

    coordinate_data = requests.get(coordinates_url).json()

    return coordinate_data[0]


lat = get_coordinates(city)["lat"]
lon = get_coordinates(city)["lon"]

end = datetime.today()
start = pd.to_datetime(end) - pd.DateOffset(years=1)

# Create Point for Vancouver, BC
city_point = Point(get_coordinates(city)["lat"], get_coordinates(city)["lon"])


def weather_history(city="tallinn"):
    # Get daily data for 2018
    # Create Point for City
    city_point = Point(
        get_coordinates(city="tallinn")["lat"], get_coordinates(city="tallinn")["lon"]
    )
    # Get daily data for last year
    historical_data = Daily(city_point, start, end)
    historical_data = historical_data.fetch()
    # Arranging hidtorical data to table and excel file
    historical_data = pd.DataFrame(historical_data)
    return historical_data


# Get daily data for 2018
city = "tallinn"
# Create Point for City
city_point = Point(get_coordinates(city)["lat"], get_coordinates(city)["lon"])
# Get daily data for last year
historical_data = Daily(city_point, start, end)
historical_data = historical_data.fetch()
# Arranging hidtorical data to table and excel file
historical_data = pd.DataFrame(historical_data).reset_index()

max_temp_df = historical_data.iloc[historical_data.tmax.argmax()]
min_temp_df = historical_data.iloc[historical_data.tmin.argmax()]

max_temp = max_temp_df.tmax
min_temp = min_temp_df.tmin
max_temp_date = max_temp_df.time
min_temp_date = min_temp_df.time


# max_temp_date = historical_data.loc[
#     historical_data.tmax == historical_data.tmax.max(), "time"
# ]
# min_temp_date = historical_data.loc[
#     historical_data.tmin == historical_data.tmin.min(), "time"
# ]
# max_temp = historical_data["tmax"].max()
# min_temp = historical_data["tmin"].min()


# historical_data["time"] = historical_data["time"].dt.date
# historical_temp_data = historical_data.iloc[:, :4]
# max_temp_row = historical_temp_data[
#     historical_temp_data["tmax"] == historical_temp_data["tmax"].max()
# ]

# min_temp_row = historical_temp_data[
#     historical_temp_data["tmin"] == historical_temp_data["tmin"].min()
# ]

# max_temp = max_temp_row["tmax"].values[0]
# min_temp = min_temp_row["tmin"].values[0]

# min_temp_date = min_temp_row["time"].values[0]
# max_temp_date = max_temp_row["time"].values[0]

# end_date = date.today()
# start_date = date.today() - relativedelta(years=1)

# start_date = datetime(2018, 1, 1)
# end_date = datetime(2018, 12, 31)

# print(end_date)
# print(start_date)

print(historical_data)
print(max_temp)
print(min_temp)
print(max_temp_date)
print(min_temp_date)

# print(weather_history(city="kuressaare"))

# print(get_coordinates("Tallinn"))
# print(lat, lon)

# print(get_weather('tallinn'))

# print(get_weather('tallinn')['main']['temp'])
