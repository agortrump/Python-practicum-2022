from flask import Flask, render_template, request
import requests


app = Flask(__name__,
            template_folder='templates',
            static_url_path='',
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
@app.route('/', methods=['GET', 'POST'])
def get_weather():
    # Get input from HTML form
    if request.method == 'POST':
        city = request.form.get('city_name')

        # Merging city and API address
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + \
            city + '&appid=60aa068482d6ddc251ae5f53570ac5fb&units=metric&mode=json'

        # requesting json from url
        weather_json = requests.get(url).json()

        if 'sys' in weather_json:
            # returning input and weather data to output html
            return render_template('weather_output.html', data=weather_json, city_name=city)
        else:
            return render_template('not_found.html')

    return render_template('weather.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
