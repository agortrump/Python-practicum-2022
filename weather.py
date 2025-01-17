from flask import Flask, render_template, request, Response, send_file
import requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from meteostat import Point, Daily
import pandas as pd
import io
from constants import api_key

app = Flask(
    __name__, template_folder="Templates", static_url_path="", static_folder="static"
)

# Default city and coordinates
city_input = "Tallinn"
# lat = 59.4372155
# lon = 24.7453688


# API data

units = "metric"

# Set time period
end_date = datetime.today()
start_date = pd.to_datetime(end_date) - pd.DateOffset(years=1)


#### Routing Pages ###

@app.route("/")
def welcome():
    return render_template("main.html")


@app.route("/weather", methods=["POST", "GET"])
def get_city(city="Tallinn"):
    global city_input
    lat = get_coordinates(city_input)["lat"]
    lon = get_coordinates(city_input)["lon"]
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
            lat_output=lat,
            lon_output=lon,
            map_src=('https://www.openstreetmap.org/export/embed.html?bbox=' + str(lon) +
                     '%2C' + str(lat) + '%2C'+str(lon+0.2) + '%2C' + str(lat+0.0) + '&amplayer=mapnik'),
            map_link=('https://www.openstreetmap.org/#map=10/' +
                      str(lat) + '/' + str(lon))
        ),
        city,
    )


### WEATHER API CALL ##


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
        + api_key)
    coordinate_data = requests.get(coordinates_url).json()
    return coordinate_data[0]

#### CITY INPUT LOG ####

@app.route("/log", methods=["GET"])
def city_log():
    global last_five_cities
    # Get city input log
    city_input_log = pd.read_csv("logs/city_input_log.csv")
    # Get current date and time
    current_date = datetime.now().strftime("%-d.%m.%Y")
    current_time = datetime.now().strftime("%H:%M:%S")

    # Making new city row

    new_row = pd.DataFrame(
        {
            "date": current_date,
            "time": [current_time],
            "city": city_input,
            "temp": (get_weather(city_input)["main"]["temp"]),
        },
        index=[-1],
    )
    # adding row to dataframe and sorting by date and time
    city_input_log = pd.concat([city_input_log, new_row])
    city_input_log.sort_values(by=["time", "date"], ascending=False, inplace=True)
    # Selecting last 5 inserted cities
    last_five_cities = city_input_log.head(6)
    last_five_cities = last_five_cities[1:6]
    # Saving new log file
    city_input_log.to_csv("logs/city_input_log.csv", index=False)
    return last_five_cities.to_html(columns=("date", "time", "city", "temp")
    )


#### ROUTING WEATHER HISTORY ####


@app.route("/weather_history", methods=["GET"])
def weather_history():
    global historical_data
    city_point = Point(get_coordinates(city_input)[
                       "lat"], get_coordinates(city_input)["lon"])
    # Get daily data for last year from METEOSTAT
    historical_data = Daily(city_point, start_date, end_date)
    historical_data = historical_data.fetch()
    # Data to dataframe and reseting index
    historical_data = pd.DataFrame(historical_data).reset_index()
    # set data type for time column to date
    historical_data["time"] = historical_data["time"].dt.date
    # Finding MAX and MIN temp values and dates
    max_temp_date = historical_data.loc[
        historical_data.tmax == historical_data.tmax.max(), "time"
    ].item()
    min_temp_date = historical_data.loc[
        historical_data.tmin == historical_data.tmin.min(), "time"
    ].item()

    return render_template(
        "weather_history.html",
        city=city_input,
        max_temp=historical_data["tmax"].max(),
        min_temp=historical_data["tmin"].min(),
        avg_temp=historical_data["tavg"].mean().round(decimals=2),
        max_temp_date=max_temp_date.strftime("%-d.%m.%Y"),
        min_temp_date=min_temp_date.strftime("%-d.%m.%Y"),
        start_date=start_date.strftime("%-d.%m.%Y"),
        end_date=end_date.strftime("%-d.%m.%Y"),
    )

#### ROUTING WEATHER GRAPH PLOT ###


@app.route("/plot")
def plot_png():

    historical_data

    fig = Figure(figsize=(10, 6), dpi=200)

    axis = fig.add_subplot(1, 1, 1)
    date = historical_data["time"]
    tmax = historical_data["tmax"]
    tmin = historical_data["tmin"]
    tavg = historical_data["tavg"]
    city = city_input
    axis.plot(date, tmax, label="Max Temp")
    axis.plot(date, tmin, label="Min Temp")
    axis.plot(date, tavg, label="AVG Temp")
    axis.set_title("Weather graph of " + city)
    axis.set_ylabel("Temperature C")
    axis.set_xlabel("Date")
    axis.legend()
    fig.savefig("history/graph.pdf", dpi=200)
    output = io.BytesIO()
    # pdf = fig.savefig("history/graph.pdf")
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


### DOWNLOAD FILES ####

# route for xlsx file
@app.route("/history/history.xlsx", methods=["GET"])
def weather_xlsx():
    historical_data.to_excel('history/history.xlsx',
                             sheet_name=city_input+'_history')
    return send_file(
        # File path for Linux/Mac
        "history/history.xlsx",
        # File path for Windows
        # ".\\history\\history.xlsx",
        download_name=city_input + " history.xlsx",
        as_attachment=True,
    )

# route for graph pdf


@app.route("/history/graph.pdf", methods=["GET"])
def weather_graph():
    return send_file(
        # File path for Linux/Mac
        "history/graph.pdf",
        # File path for Windows
        # ".\\history\\graph.pdf",
        download_name=city_input + " weather graph.pdf",
        as_attachment=True,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
    # app.run()
