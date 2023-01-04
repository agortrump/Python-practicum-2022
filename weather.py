from flask import Flask, render_template, request, Response, send_file
import requests
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from meteostat import Point, Daily
import pandas as pd
import base64
import io
import numpy as np
import pdfkit

app = Flask(
    __name__, template_folder="Templates", static_url_path="", static_folder="static"
)

# Default city

city_input = "Tallinn"

# API data
api_key = "c89dc689f952d6b8abcbafe9569fbc8f"
units = "metric"

# WEATHER PAGE ROUTING


@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/weather", methods=["POST", "GET"])
def get_city(city="Tallinn"):
    global city_input
    # Get input from HTML form
    if request.method == "POST":
        city = request.form.get("city_name").capitalize()
        # If city not in values, return could not find
        if city not in get_weather(city).values():
            return render_template("weather.html", no_city="Could not find such city")
        # Create Point for City
        city_input = city
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
        ),
        city,
    )


# WEATHER API CALL


def get_weather(city=city_input):
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


# PYTHON METEOSTAT DATA

# Set time period
end = datetime.today()
start = pd.to_datetime(end) - pd.DateOffset(years=1)

# CITY COORDINATES FROM API


def get_coordinates(city=city_input):
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


@app.route("/weather_history", methods=["GET"])
def weather_history():
    global historical_data
    city_point = Point(
        get_coordinates(city_input)["lat"], get_coordinates(city_input)["lon"]
    )
    # Get daily data for last year
    historical_data = Daily(city_point, start, end)
    historical_data = historical_data.fetch()
    # Data to dataframe and reseting index
    historical_data = pd.DataFrame(historical_data).reset_index()
    # set data type for time column to date
    historical_data["time"] = historical_data["time"].dt.date
    # selecting only temperature and date data
    historical_temp_data = historical_data.iloc[:, :4]
    # Finding MAX and MIN temp values and dates
    max_temp_row = historical_temp_data[
        historical_temp_data["tmax"] == historical_temp_data["tmax"].max()
    ]
    min_temp_row = historical_temp_data[
        historical_temp_data["tmin"] == historical_temp_data["tmin"].min()
    ]
    return (
        render_template(
            "weather_history.html",
            city=city_input,
            max_temp=max_temp_row["tmax"].values[0],
            min_temp=min_temp_row["tmin"].values[0],
            # Get MIN and MAX temp date
            min_temp_date=min_temp_row["time"].values[0],
            max_temp_date=max_temp_row["time"].values[0],
        )
    ), historical_data.to_excel(
        "history/history.xlsx", sheet_name=city_input + "_history"
    )


@app.route("/plot")
def plot_png():

    historical_data

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    date = historical_data["time"]
    tmax = historical_data["tmax"]
    tmin = historical_data["tmin"]
    tavg = historical_data["tavg"]
    axis.plot(date, tmax, label="Max Temp")
    axis.plot(date, tmin, label="Min Temp")
    axis.plot(date, tavg, label="AVG Temp")
    axis.legend()
    output = io.BytesIO()
    # pdf = fig.savefig("history/graph.pdf")
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


@app.route("/history/history.xlsx", methods=["GET"])
def weather_xlsx():
    return send_file(
        # File path for Linux/Mac
        "history/history.xlsx",
        # File path for Windows
        # ".\\history\\history.xlsx",
        download_name=city_input + " history.xlsx",
        as_attachment=True,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
