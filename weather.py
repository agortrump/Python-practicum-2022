from flask import Flask, render_template, request
import requests
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from meteostat import Point, Daily
import pandas as pd
import base64
from io import BytesIO
from openpyxl.workbook import workbook
import os

path = os.getcwd()

app = Flask(
    __name__, template_folder="templates", static_url_path="", static_folder="static"
)


@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/welcome/home")
def welcome_home():
    return "Welcome Home"


@app.route("/welcome/back")
def welcome_back():
    return "Welcome Back"


# Default city
city = "Tallinn"


# API data
api_key = "c89dc689f952d6b8abcbafe9569fbc8f"
units = "metric"


# WEATHER API CALL


def get_weather(city):
    global weather_data
    # MERGING WEATHER API URL
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


# CITY COORDINATES FROM API


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


# CITY COORDINATES VARIABLES
lat = get_coordinates(city)["lat"]
lon = get_coordinates(city)["lon"]


# PYTHON METEOSTAT DATA

# Set time period
end = datetime.today()
start = pd.to_datetime(end) - pd.DateOffset(years=1)

# Create Point for City
city_point = Point(get_coordinates(city)["lat"], get_coordinates(city)["lon"])

# Plot line chart including average, minimum and maximum temperature
# historical_data.plot(y=["tavg", "tmin", "tmax"])
# plt.show()

# GET CITY FROM FORM


@app.route("/weather", methods=["POST", "GET"])
def get_city(city="Tallinn"):
    # Get input from HTML form
    if request.method == "POST":
        city = request.form.get("city_name").capitalize()
        # If city not in values, return could not find
        if city not in get_weather(city).values():
            return render_template("weather.html", no_city="Could not find such city")
        # Create Point for City
        city_point = Point(get_coordinates(
            city)["lat"], get_coordinates(city)["lon"])
        # Get daily data for last year
        historical_data = Daily(city_point, start, end)
        historical_data = historical_data.fetch()
        # Arranging hidtorical data to table and excel file
        historical_data = pd.DataFrame(historical_data)

    return (
        render_template(
            "weather.html",
            temp=get_weather(city)["main"]["temp"],
            feels_like=get_weather(city)["main"]["feels_like"],
            wind=get_weather(city)["wind"]["speed"],
            city=city,
            country=get_weather(city)["sys"]["country"],
            icon="https://openweathermap.org/img/wn/"
            + get_weather(city)["weather"][0]["icon"]
            + "@2x.png",
            lat=get_coordinates(city)["lat"],
            lon=get_coordinates(city)["lon"],
            weather_history=weather_history(city),
        ),
        city,
    )


@app.route("/weather_history", methods=["GET"])
def weather_history(city='Tallinn'):
    if request.method == 'GET':
        # Create Point for City
        city_point = Point(get_coordinates(
            city)["lat"], get_coordinates(city)["lon"])
        # Get daily data for last year
        historical_data = Daily(city_point, start, end)
        historical_data = historical_data.fetch()
        # Arranging hidtorical data to table and excel file
        historical_data = pd.DataFrame(historical_data)
        return historical_data.to_excel(
            "history/history.xlsx", sheet_name=city + "_history"
        )
    return 'ajalugu'


@app.route("/weather_history", methods=["POST"])
def weather_graph(city):
    fig = Figure()
    ax = fig.subplots()
    ax.plot([1, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    graph_data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"graph_data:image/png;base64,{graph_data}"


history_graph = weather_graph(city)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
    # app.run()
