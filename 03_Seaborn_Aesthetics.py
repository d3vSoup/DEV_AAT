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

# Box Plot: Trips by Service Type
plt.figure(figsize=(8, 5))
sns.boxplot(data=routes[routes["trip_count"] <= 50], x="service_type", y="trip_count", hue="service_type", legend=False)
plt.title("Trip Frequency by Service Type")
plt.xlabel("Service Type")
plt.ylabel("Daily Trips")
plt.tight_layout()
print("Displaying 1: Box Plot...")
plt.show()

# Violin Plot: Stops by Service Type
plt.figure(figsize=(8, 5))
sns.violinplot(data=routes, x="service_type", y="stop_count", hue="service_type", legend=False)
plt.title("Stop Count by Service Type")
plt.xlabel("Service Type")
plt.ylabel("Stops")
plt.tight_layout()
print("Displaying 2: Violin Plot...")
plt.show()

# Correlation Heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(routes[["trip_count", "stop_count", "direction_id"]].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.tight_layout()
print("Displaying 3: Heatmap...")
plt.show()

# Binned Pivot Heatmap: Average Trips by Length and Service Type
bins = [0, 20, 35, 50, 100]
labels = ["Short (<20)", "Medium (20-35)", "Long (35-50)", "Ultra-Long (>50)"]
routes["length_bin"] = pd.cut(routes["stop_count"], bins=bins, labels=labels)

pivot = routes.pivot_table(index="service_type", columns="length_bin", values="trip_count", aggfunc="mean", observed=False).round(1)

plt.figure(figsize=(8, 5))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=1, cbar_kws={'label': 'Average Daily Trips'})
plt.title("Average Daily Trips by Route Length and Service Type")
plt.xlabel("Route Length Bin")
plt.ylabel("Service Type")
plt.tight_layout()
print("Displaying 4: Binned Pivot Heatmap...")
plt.show()
