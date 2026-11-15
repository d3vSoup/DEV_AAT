import pandas as pd

routes = pd.read_csv("routes.csv")
stops = pd.read_csv("stops.csv")
agg = pd.read_csv("aggregated.csv")

print("--- Routes Dataset ---")
print("Shape:", routes.shape)
print(routes[['name', 'full_name', 'trip_count', 'stop_count']].head())

print("\n--- Stops Dataset ---")
print("Shape:", stops.shape)
print(stops.head())

print("\n--- Route Statistics ---")
print(routes[['trip_count', 'stop_count']].describe())

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

print("\n--- Route Counts by Service Type ---")
print(routes['service_type'].value_counts())

high_freq = routes[routes['trip_count'] >= 100].sort_values(by='trip_count', ascending=False)
print("\n--- Top High Frequency Routes (100+ trips) ---")
print(high_freq[['name', 'full_name', 'trip_count', 'service_type']].head(10))

metro_stops = stops[stops['name'].str.contains('Metro', case=False, na=False)]
print(f"\n--- Total Metro Connected Stops: {len(metro_stops)} ---")
print(metro_stops[['name', 'route_count', 'trip_count']].head(10))

summary = routes.groupby('service_type').agg(
    total_routes=('name', 'count'),
    total_trips=('trip_count', 'sum'),
    avg_stops=('stop_count', 'mean')
).round(2)
print("\n--- Service Type Summary ---")
print(summary)

top_hubs = agg.sort_values(by='trip_count', ascending=False).head(10)
print("\n--- Top 10 Busiest Bus Hubs ---")
print(top_hubs[['name', 'route_count', 'trip_count']])
