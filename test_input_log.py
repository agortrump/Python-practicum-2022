import pandas as pd
from datetime import datetime, date

cuurent_date = datetime.today()

print(cuurent_date)

# weather_log = pd.read_csv("logs/log.csv")
# wheater_log = (datetime.today(date), datetime.time(), "Tallinn", 15.7)
# wheater_log = pd.DataFrame(wheater_log)

# new_row = pd.DataFrame(
#     {"date": datetime.today(), "time": "15.30.28", "city": "Tallinn", "temp": 15.6},
#     index=[0],
# )
# weather_log = pd.concat([new_row, weather_log.loc[:]], ignore_index=True)
# print(weather_log)

# weather_log.to_csv("logs/log.csv")

# print(weather_log)
