import plotly.express as px
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

# Bar Plot: Top 15 Bus Corridors
top_15 = routes.sort_values(by="trip_count", ascending=False).head(15)
fig1 = px.bar(
    top_15,
    x="trip_count",
    y="full_name",
    color="service_type",
    orientation="h",
    title="Top 15 Bus Corridors in Bengaluru",
    labels={"trip_count": "Daily Trips", "full_name": "Route"}
)
print("Displaying 1: Interactive Bar Plot...")
fig1.show()

# Scatter Plot: Stops vs Trips
fig2 = px.scatter(
    routes,
    x="stop_count",
    y="trip_count",
    color="service_type",
    hover_name="name",
    title="Route Stop Count vs Daily Trips",
    labels={"stop_count": "Number of Stops", "trip_count": "Daily Trips"}
)
print("Displaying 2: Interactive Scatter Plot...")
fig2.show()
