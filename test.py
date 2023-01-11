import pandas as pd
from datetime import datetime

city_input_log = pd.read_csv("logs/city_input_log.csv")
# Get current date and time

# Making new city row

new_row = pd.DataFrame(
    {
        "date": datetime.today().strftime("%D.%M.%Y"),
        "time": datetime.today().strftime("%H:%M:%S"),
        "city": 'Türi',
        "temp": 111,
    },
    index=[-1],)
# adding row to dataframe and sorting by date and time
city_input_log = pd.concat([city_input_log, new_row])
city_input_log.sort_values(by=["time", "date"], ascending=False, inplace=True)
# Selecting last 5 inserted cities
last_five_cities = city_input_log.head(6)
last_five_cities = last_five_cities[1:6]
# Saving new log file
city_input_log.to_csv("logs/city_input_log.csv", index=False)

print(last_five_cities)