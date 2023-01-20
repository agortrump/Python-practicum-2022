import requests
import asyncio
import tracemalloc
import timeit

api_key = "44b1426a79ac8397051a943fc50f9b79"
units = "metric"
city_list = ["tallinn", "tartu", "keila", "kohila", "pärnu"]


## WEATHER API CALL ##
async def get_weather(city):
    # MERGING WEATHER API URL
    weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?q="
        + city
        + "&appid="
        + api_key
        + "&units=metric"
    )
    weather_data = requests.get(weather_url).json()
    await asyncio.sleep(3)
    temp = weather_data["main"]["temp"]
    feels_like = weather_data["main"]["feels_like"]
    wind = weather_data["wind"]["speed"]
    country = weather_data["sys"]["country"]
    return print(temp, feels_like, wind, country)
    # return print(weather_data)


async def get_coordinates(city):
    # MERGING Coordinates API URL
    api_key = "44b1426a79ac8397051a943fc50f9b79"
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
    return print(lat, lon)


# lat = get_coordinates(city)["lat"]
# lon = get_coordinates(city)["lon"]
# favorites = Favorite.query.all()


async def main():
    print("Async testing")
    for city in city_list:
        task1 = asyncio.create_task(get_weather(city))
        task2 = asyncio.create_task(get_coordinates(city))

        weather = await task1
        coordinates = await task2


# if __name__ == "__main__":

asyncio.run(main())
