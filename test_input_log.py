import pandas as pd
from datetime import datetime, date
import numpy as np
import csv

current_date = datetime.now().strftime("%-d.%m.%Y")
current_time = datetime.now().strftime("%H:%M:%S")
city = "Tallinn"
current_temp = 13


print(current_date)
print(current_time)

# city_input_log = pd.read_csv("logs/city_input_log.csv")


# new_row = pd.DataFrame(
#     {"date": current_date, "time": [current_time], "city": city, "temp": current_temp},
#     index=[-1],
# )

# city_input_log = pd.concat([city_input_log, new_row])
# city_input_log.sort_values(by=["time", "date"], ascending=False, inplace=True)

# last_five_cities = city_input_log.head(5)

# city_input_log.to_csv("logs/city_input_log.csv", index=False)


# print(city_input_log)
# print(last_five_cities)

with open("logs/city_input_log.csv", "r") as city_input_log:
    for line in csv.reader(city_input_log):
        city_input_log


print(city_input_log)
