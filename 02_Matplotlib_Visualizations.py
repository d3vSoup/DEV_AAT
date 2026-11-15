import matplotlib.pyplot as plt
import pandas as pd

routes = pd.read_csv("routes.csv")
agg = pd.read_csv("aggregated.csv")

def get_service_type(name):
    name = str(name).strip()
    if name.startswith("KIA"):
        return "Airport"
    elif name.startswith("V"):
        return "Vajra AC"
    elif "MF" in name:
        return "Metro Feeder"
    return "Ordinary"

routes['service_type'] = routes['name'].apply(get_service_type)

# 1. Bar Plot: Top 10 Bus Hubs
top_10 = agg.sort_values(by="trip_count", ascending=False).head(10).iloc[::-1]
plt.figure(figsize=(9, 5))
plt.barh(top_10["name"], top_10["trip_count"], color="skyblue", edgecolor="navy")
plt.xlabel("Daily Trips")
plt.ylabel("Hub Name")
plt.title("Top 10 Busiest Bus Hubs in Bengaluru")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.tight_layout()
print("Displaying 1: Bar Plot...")
plt.show()

# 2. Histogram: Stops per Route
plt.figure(figsize=(8, 5))
plt.hist(routes["stop_count"], bins=25, color="lightgreen", edgecolor="black")
plt.xlabel("Number of Stops")
plt.ylabel("Number of Routes")
plt.title("Distribution of Stops per Route")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
print("Displaying 2: Histogram...")
plt.show()

# 3. Scatter Plot: Stops vs Daily Trips
plt.figure(figsize=(8, 5))
plt.scatter(routes["stop_count"], routes["trip_count"], alpha=0.5, c="purple", edgecolors="none")
plt.xlabel("Stop Count")
plt.ylabel("Daily Trips")
plt.title("Route Stops vs. Daily Trip Frequency")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
print("Displaying 3: Scatter Plot...")
plt.show()

# 4. Pie Chart: Service Types
counts = routes["service_type"].value_counts()
plt.figure(figsize=(6, 6))
plt.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=140)
plt.title("BMTC Routes by Service Type")
plt.tight_layout()
print("Displaying 4: Pie Chart...")
plt.show()
