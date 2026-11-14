# ==============================================================================
# BMTC PUBLIC TRANSPORTATION: PANDAS DATA MANIPULATION & ANALYSIS
# ==============================================================================
# This script performs core data manipulation operations on Bengaluru's real
# public bus transit data using Pandas.
#
# Datasets used:
# 1. routes.csv     : 7,475 route directions, trip frequencies, stop counts
# 2. stops.csv      : 9,960 individual bus stops across Bengaluru
# 3. aggregated.csv : 5,211 merged transit junctions and bus hubs
#
# Operations covered:
# 1. Loading & Inspecting Datasets (.shape, .info(), .describe(), null checks)
# 2. Series & DataFrame Access, Slicing, and Querying
# 3. Filtering & Boolean Indexing (High-frequency, Airport, Metro Feeder)
# 4. Feature Engineering (Categorizing Service Types, Extracting Terminals)
# 5. Groupby Aggregations (Summary statistics across bus service tiers)
# 6. Sorting, Ranking, and Exporting Clean Data (.to_csv)
# ==============================================================================

import pandas as pd
import numpy as np
import os

# Create outputs directory for exported data
os.makedirs("outputs", exist_ok=True)

# ------------------------------------------------------------------------------
# 1. LOADING & INSPECTING THE DATASETS
# ------------------------------------------------------------------------------
print("==================================================================")
print("1. LOADING & INSPECTING BMTC DATASETS")
print("==================================================================")

routes_path = "routes.csv" if os.path.exists("routes.csv") else "data/routes.csv"
stops_path = "stops.csv" if os.path.exists("stops.csv") else "data/stops.csv"
agg_path = "aggregated.csv" if os.path.exists("aggregated.csv") else "data/aggregated.csv"

routes_df = pd.read_csv(routes_path)
stops_df = pd.read_csv(stops_path)
agg_df = pd.read_csv(agg_path)

print(f"Routes dataset loaded     : {routes_df.shape[0]:,} rows, {routes_df.shape[1]} columns")
print(f"Stops dataset loaded      : {stops_df.shape[0]:,} rows, {stops_df.shape[1]} columns")
print(f"Aggregated hubs loaded    : {agg_df.shape[0]:,} rows, {agg_df.shape[1]} columns")

print("\n--- Routes Column Overview ---")
print(routes_df[['name', 'full_name', 'trip_count', 'stop_count']].head(3))

print("\n--- Checking for Missing / Null Values ---")
print("Routes null count     :", routes_df[['name', 'trip_count', 'stop_count']].isnull().sum().to_dict())
print("Stops null count      :", stops_df[['name', 'trip_count', 'route_count']].isnull().sum().to_dict())
print("Aggregated null count :", agg_df[['name', 'trip_count', 'route_count']].isnull().sum().to_dict())


# ------------------------------------------------------------------------------
# 2. STATISTICAL SUMMARIES (.describe)
# ------------------------------------------------------------------------------
print("\n==================================================================")
print("2. DESCRIPTIVE STATISTICS FOR NUMERICAL FEATURES")
print("==================================================================")
print("--- Route Statistics (Trip Count & Stop Count) ---")
print(routes_df[['trip_count', 'stop_count']].describe().round(2))

print("\n--- Hub Statistics from aggregated.csv ---")
print(agg_df[['trip_count', 'route_count']].describe().round(2))


# ------------------------------------------------------------------------------
# 3. FEATURE ENGINEERING: SERVICE CLASSIFICATION & TERMINALS
# ------------------------------------------------------------------------------
print("\n==================================================================")
print("3. FEATURE ENGINEERING")
print("==================================================================")

def classify_service(route_name):
    """Classifies route into BMTC service tiers based on naming convention."""
    name_str = str(route_name).strip()
    if name_str.startswith("KIA"):
        return "Vayu Vajra (Airport)"
    elif name_str.startswith("V-") or name_str.startswith("V"):
        return "Vajra AC"
    elif "MF" in name_str or name_str.startswith("MF-"):
        return "Metro Feeder"
    else:
        return "Ordinary / General"

# Create new column 'service_type'
routes_df["service_type"] = routes_df["name"].apply(classify_service)
print("Service Type Distribution across Bengaluru routes:")
print(routes_df["service_type"].value_counts())

# Extract Origin and Destination from full_name (format: "Origin → Destination")
def get_origin(full_name):
    parts = str(full_name).split("→")
    return parts[0].strip() if len(parts) > 1 else full_name

def get_destination(full_name):
    parts = str(full_name).split("→")
    return parts[1].strip() if len(parts) > 1 else full_name

routes_df["origin"] = routes_df["full_name"].apply(get_origin)
routes_df["destination"] = routes_df["full_name"].apply(get_destination)

print("\nSample Engineered Columns (Origin, Destination, Service Type):")
print(routes_df[["name", "origin", "destination", "service_type"]].head(3))


# ------------------------------------------------------------------------------
# 4. FILTERING & BOOLEAN INDEXING
# ------------------------------------------------------------------------------
print("\n==================================================================")
print("4. FILTERING & BOOLEAN INDEXING")
print("==================================================================")

# A. High frequency routes: >= 100 trips per day
high_freq_routes = routes_df[routes_df["trip_count"] >= 100].sort_values("trip_count", ascending=False)
print(f"A. Number of routes operating 100+ trips/day: {len(high_freq_routes)}")
print(high_freq_routes[["name", "full_name", "trip_count", "service_type"]].head(5).to_string(index=False))

# B. Vayu Vajra Airport Routes
airport_routes = routes_df[routes_df["service_type"] == "Vayu Vajra (Airport)"]
print(f"\nB. Total Vayu Vajra Airport Route Directions: {len(airport_routes)}")
print(airport_routes[["name", "full_name", "trip_count", "stop_count"]].head(3).to_string(index=False))

# C. Stops connecting directly to Namma Metro Stations
metro_stops = stops_df[stops_df["name"].str.contains("Metro", case=False, na=False)].copy()
print(f"\nC. Number of BMTC bus stops with direct Metro interchange: {len(metro_stops)}")
print(metro_stops[["name", "route_count", "trip_count"]].head(5).to_string(index=False))


# ------------------------------------------------------------------------------
# 5. GROUPBY AGGREGATIONS
# ------------------------------------------------------------------------------
print("\n==================================================================")
print("5. GROUPBY AGGREGATIONS")
print("==================================================================")

# Grouping by Service Type
service_summary = routes_df.groupby("service_type").agg(
    total_routes=("name", "count"),
    total_daily_trips=("trip_count", "sum"),
    avg_trips_per_route=("trip_count", "mean"),
    avg_stops_per_route=("stop_count", "mean"),
    max_trips=("trip_count", "max")
).round(2).reset_index()

print("--- Service Tier Performance Summary ---")
print(service_summary.to_string(index=False))

# Top 10 Major Transit Interchanges in Bengaluru (from aggregated.csv)
top_hubs = agg_df.sort_values("trip_count", ascending=False).head(10)[["name", "route_count", "trip_count"]]
print("\n--- Top 10 Busiest Bus Hubs (Aggregated Junctions) ---")
print(top_hubs.to_string(index=False))


# ------------------------------------------------------------------------------
# 6. EXPORTING PROCESSED TABLES
# ------------------------------------------------------------------------------
print("\n==================================================================")
print("6. EXPORTING SUMMARY DATAFRAMES TO CSV")
print("==================================================================")

top_hubs.to_csv("outputs/top_10_transit_hubs.csv", index=False)
service_summary.to_csv("outputs/service_tier_summary.csv", index=False)
metro_stops.sort_values("trip_count", ascending=False).to_csv("outputs/metro_connected_stops.csv", index=False)
high_freq_routes.head(50).to_csv("outputs/top_50_high_freq_routes.csv", index=False)

print("Exported files created in 'outputs/':")
print("  - outputs/top_10_transit_hubs.csv")
print("  - outputs/service_tier_summary.csv")
print("  - outputs/metro_connected_stops.csv")
print("  - outputs/top_50_high_freq_routes.csv")
print("\nData manipulation script completed successfully!")

