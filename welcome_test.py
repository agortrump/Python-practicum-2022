from flask import Flask, render_template, request
import requests


app = Flask(__name__,
            template_folder='templates',
            static_url_path='/',
            static_folder='static')


@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/welcome/home')
def welcome_home():
    return 'Welcome Home'


@app.route('/welcome/back')
def welcome_back():
    return 'Welcome Back'


# Default city
city = 'Tallinn'


# API data
api_key = 'c89dc689f952d6b8abcbafe9569fbc8f'
units = 'metric'


# WEATHER API CALL


def get_weather(city):
    global weather_data
    # MERGING WEATHER API URL
    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + \
        city + '&appid=' + api_key + '&units=' + units + '&mode=json'
    weather_data = requests.get(weather_url).json()

    return weather_data

# CITY COORDINATES


def get_coordinates(city):
    global coordinate_data
    # MERGING Coordinates API URL
    coordinates_url = 'http://api.openweathermap.org/geo/1.0/direct?q=' + \
        city + ',' + get_weather['sys']['country'] + \
        '&limit=1&appid=' + api_key

    coordinate_data = requests.get(coordinates_url).json()

    return coordinate_data


# GET CITY FROM FORM

@app.route('/weather', methods=['POST', 'GET'])
def get_city(city='Tallinn'):
    # Get input from HTML form
    if request.method == 'POST':
        city = request.form.get('city_name').capitalize()
        # If nothing is typed in form return weather page
        if len(city) == 0:
            return render_template('weather.html', no_input="You should write the name of a city in the box!")
        elif city not in get_weather(city).values():
            return render_template('weather.html', no_city='Could not find such city')
    return (render_template('weather.html', temp=get_weather(city)['main']['temp'],
                            feels_like=get_weather(city)['main']['feels_like'],
                            wind=get_weather(city)['wind']['speed'],
                            city=city,
                            country=', ' + get_weather(city)['sys']['country'],
                            icon='https://openweathermap.org/img/wn/' +
                            get_weather(city)[
        'weather'][0]['icon'] + '@2x.png',
        country=get_weather['sys']['country']),
        city)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
