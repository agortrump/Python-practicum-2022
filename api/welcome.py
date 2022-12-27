from flask import Flask, render_template
import urllib.request

app = Flask(__name__, template_folder='Templates')


@app.route('/weather')
def get_weather():
    city = 'Tallinn'
    url = 'https://api.openweathermap.org/data/2.5/weather?q=' + \
        city + '&appid=60aa068482d6ddc251ae5f53570ac5fb&units=metric'

    weather = urllib.request.urlopen(url)
    data = weather.read

    return render_template('/Templates/weather.html')


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
