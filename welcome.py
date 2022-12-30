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


# Weather information and city input
@app.route('/weather', methods=['GET', 'POST'])
def get_weather():
    api_key = '60aa068482d6ddc251ae5f53570ac5fb'
    units = 'metric'
    # Get input from HTML form
    if request.method == 'POST':
        city = request.form.get('city_name').capitalize()
        # If nothing is typed in form return weather page
        if len(city) == 0:
            return render_template('weather.html', no_city="You should write the name of a city in the box")
        # Merging city and API address
        weather_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + \
            city + '&appid=' + api_key + '&units=' + units + '&mode=json'

        # Requesting data from url
        weather_data = requests.get(weather_url).json()

        # Checking if city is in weather data
        if city in weather_data.values():
            # returning input and weather data to output html if city found in weather data
            return render_template('weather_output.html', data=weather_data, city_name=city)
        else:
            # If city not in weather data returning not found page
            return render_template('not_found.html')

    return render_template('weather.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
