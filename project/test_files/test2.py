import requests
import asyncio
import tracemalloc
import timeit

api_key = "44b1426a79ac8397051a943fc50f9b79"
city_list = ["tallinn", "tartu", "keila", "kohila", "pärnu"]


## WEATHER API CALL ##
for city in city_list:
    # MERGING WEATHER API URL
    weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?q="
        + city
        + "&appid="
        + api_key
        + "&units=metric"
    )
    weather_data = requests.get(weather_url).json()

    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    wind = weather_data["wind"]["speed"]
    country = weather_data["sys"]["country"]

    print(temp, feels_like, wind, country)

    coordinates_url = (
        "http://api.openweathermap.org/geo/1.0/direct?q="
        + city
        + ","
        + "EE"
        + "&limit=1&appid="
        + api_key
    )
    coordinate_data = requests.get(coordinates_url).json()
    lat = coordinate_data[0]["lat"]
    lon = coordinate_data[0]["lon"]
    print(lat, lon)


# print(timeit.timeit(lambda: get_weather(city_list)))
