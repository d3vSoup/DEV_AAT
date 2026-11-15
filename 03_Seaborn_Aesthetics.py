import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

routes = pd.read_csv("routes.csv")

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

sns.set_theme(style="whitegrid")

# 1. Box Plot: Trips by Service Type
plt.figure(figsize=(8, 5))
sns.boxplot(data=routes[routes["trip_count"] <= 50], x="service_type", y="trip_count", hue="service_type", legend=False)
plt.title("Trip Frequency by Service Type")
plt.xlabel("Service Type")
plt.ylabel("Daily Trips")
plt.tight_layout()
print("Displaying 1: Box Plot...")
plt.show()

# 2. Violin Plot: Stops by Service Type
plt.figure(figsize=(8, 5))
sns.violinplot(data=routes, x="service_type", y="stop_count", hue="service_type", legend=False)
plt.title("Stop Count by Service Type")
plt.xlabel("Service Type")
plt.ylabel("Stops")
plt.tight_layout()
print("Displaying 2: Violin Plot...")
plt.show()

# 3. Correlation Heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(routes[["trip_count", "stop_count", "direction_id"]].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
print("Displaying 3: Heatmap...")
plt.show()
