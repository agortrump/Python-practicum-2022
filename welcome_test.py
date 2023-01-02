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

# WEATHER API CALL


def get_weather(city):
    global weather_data
    api_key = '60aa068482d6ddc251ae5f53570ac5fb'
    units = 'metric'
    # MERGING API URL
    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + \
        city + '&appid=' + api_key + '&units=' + units + '&mode=json'
    weather_data = requests.get(weather_url).json()

    return weather_data


# Get city from form


@app.route('/weather', methods=['POST', 'GET'])
def get_city(city='Tallinn'):
    # Get input from HTML form
    if request.method == 'POST':
        city = request.form('city_name_form').get('city_name').capitalize()
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
                            icon='https://openweathermap.org/img/wn/' + get_weather(city)['weather'][0]['icon'] + '@2x.png'),
            city)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
