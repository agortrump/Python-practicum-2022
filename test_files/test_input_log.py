import pandas as pd
from datetime import datetime, date
import numpy as np
import csv

current_date = datetime.now().strftime("%D.%M.%Y")
current_time = datetime.now().strftime("%H:%M:%S")
city = "Tallinn"
current_temp = 13


print(current_date)
print(current_time)

city_input_log = pd.read_csv("logs/city_input_log.csv")


new_row = pd.DataFrame(
    {
        "date": current_date,
        "time": current_time,
        "city": "türi",
        "temp": 8,
    },
    index=[-1],
)

city_input_log = pd.concat([city_input_log, new_row])
city_input_log.sort_values(by=["date", "time"], ascending=True, inplace=True)

last_five_cities = city_input_log.head(6).reindex()

city_input_log.to_csv("logs/city_input_log.csv", index=False)


print(last_five_cities)

# print(city_input_log)
# print(last_five_cities)


# print(city_input_log)
