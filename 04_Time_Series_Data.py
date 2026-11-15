import matplotlib.pyplot as plt
import pandas as pd
import re

routes = pd.read_csv("routes.csv")

hours = []
for trip_str in routes["trip_list"]:
    matches = re.findall(r"'(\d{2}):\d{2}:\d{2}'", str(trip_str))
    hours.extend([int(m) for m in matches])

hourly = pd.Series(hours).value_counts().reindex(range(24), fill_value=0).sort_index()

plt.figure(figsize=(10, 5))
plt.plot(hourly.index, hourly.values, marker="o", color="blue", linewidth=2)
plt.fill_between(hourly.index, hourly.values, color="skyblue", alpha=0.4)
plt.xlabel("Hour of Day (00:00 - 23:00)")
plt.ylabel("Total Bus Departures")
plt.title("24-Hour BMTC Bus Departure Profile")
plt.xticks(range(24))
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
print("Displaying Time Series Plot...")
plt.show()
