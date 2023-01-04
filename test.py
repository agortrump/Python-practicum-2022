import requests
from datetime import datetime
import pandas as pd
from meteostat import Point, Daily


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


def get_coordinates(city):
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
    city_point = Point(get_coordinates(city)["lat"], get_coordinates(city)["lon"])
    # Get daily data for last year
    historical_data = Daily(city_point, start, end)
    historical_data = historical_data.fetch()
    # Arranging hidtorical data to table and excel file
    historical_data = pd.DataFrame(historical_data)
    return historical_data


print(weather_history(city="kuressaare"))

# print(get_coordinates("Tallinn"))
# print(lat, lon)

# print(get_weather('tallinn'))

# print(get_weather('tallinn')['main']['temp'])
