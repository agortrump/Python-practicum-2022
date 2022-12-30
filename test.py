import requests


def get_weather(city):
    api_key = '60aa068482d6ddc251ae5f53570ac5fb'
    units = 'metric'
    # MERGING API URL
    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + \
        city + '&appid=' + api_key + '&units=' + units + '&mode=json'
    weather_data = requests.get(weather_url).json()

    return weather_data


# print(get_weather('tallinn'))

# print(get_weather('tallinn')['main']['temp'])
