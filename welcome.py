from flask import Flask, render_template, request
import requests

app = Flask(__name__, template_folder='Templates')


# Weather information and city input
@app.route('/weather', methods=['GET', 'POST'])
def get_weather():
    # Get input from HTML form
    if request.method == 'POST':
        city = request.form.get('city_name')

        # Merging city and API address
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' + \
            city + '&appid=60aa068482d6ddc251ae5f53570ac5fb&units=metric&mode=json'

        # requesting json from url
        weather_json = requests.get(url).json()

        # returning input and weather data to output html
        return render_template('weather_output.html', data=weather_json, city_name=city)

    return render_template('weather.html')


@app.route('/welcome')
def welcome():
    return 'Welcome'


@app.route('/welcome/home')
def welcome_home():
    return 'Welcome Home'


@app.route('/welcome/back')
def welcome_back():
    return 'Welcome Back'


if __name__ == '__main__':
    app.run(debug=True)
