# ==============================================================================
# TIME SERIES ANALYSIS: 24-HOUR BMTC DEPARTURE FREQUENCY PROFILE
# ==============================================================================
# Time series analysis examines data ordered sequentially over time.
# In urban transit, departure schedules reveal critical supply patterns:
# - Morning and evening commuter rush hours
# - Mid-day base service levels
# - Late-night and early-morning off-peak operations
#
# Operations covered:
# 1. Parsing Timestamp Strings into Structured Time Data (from trip_list)
# 2. Hourly Resampling & Aggregation across 24 hours (00:00 - 23:00)
# 3. Rolling Window Smoothing (3-hour Moving Average)
# 4. Line Plot with Peak Annotations & Area Shading
# 5. Hour-by-Service-Tier Heatmap (Ordinary vs AC vs Feeder vs Airport)
# 6. Exporting Hourly Transit Profile to CSV
# ==============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# Create outputs directory
os.makedirs("outputs", exist_ok=True)

# Load routes dataset
routes_path = "routes.csv" if os.path.exists("routes.csv") else "data/routes.csv"
routes_df = pd.read_csv(routes_path)

print("==================================================================")
print("1. PARSING 57,000+ DEPARTURE TIMESTAMPS ACROSS BENGALURU")
print("==================================================================")

def classify_service(name):
    name_str = str(name).strip()
    if name_str.startswith("KIA"):
        return "Vayu Vajra (Airport)"
    elif name_str.startswith("V-") or name_str.startswith("V"):
        return "Vajra AC"
    elif "MF" in name_str or name_str.startswith("MF-"):
        return "Metro Feeder"
    else:
        return "Ordinary"

routes_df["service_type"] = routes_df["name"].apply(classify_service)

# Extract hour (0-23) for each departure trip and pair with service_type
records = []
for _, row in routes_df.iterrows():
    stype = row["service_type"]
    trip_str = str(row["trip_list"])
    # Extract HH from 'HH:MM:SS'
    hours = re.findall(r"'(\d{2}):\d{2}:\d{2}'", trip_str)
    for h in hours:
        records.append({"hour": int(h), "service_type": stype})

time_df = pd.DataFrame(records)
print(f"Total parsed individual bus departures: {len(time_df):,}")

# ------------------------------------------------------------------------------
# 2. HOURLY AGGREGATION & ROLLING SMOOTHING
# ------------------------------------------------------------------------------
print("\n==================================================================")
print("2. HOURLY AGGREGATION & ROLLING AVERAGE")
print("==================================================================")

hourly_total = time_df["hour"].value_counts().reindex(range(24), fill_value=0).sort_index()

hourly_df = pd.DataFrame({
    "Hour": hourly_total.index,
    "Departures": hourly_total.values
})

# Calculate 3-hour centered rolling average for smoothing
hourly_df["Rolling_Avg"] = hourly_df["Departures"].rolling(window=3, center=True, min_periods=1).mean()

print(hourly_df.to_string(index=False))

# ------------------------------------------------------------------------------
# 3. TIME SERIES PLOT: 24-HOUR TRANSIT PROFILE
# ------------------------------------------------------------------------------
plt.figure(figsize=(11, 6))

plt.plot(hourly_df["Hour"], hourly_df["Departures"], marker='o', markersize=6,
         color='#1f77b4', linewidth=2.5, label='Actual Departures / Hour')
plt.plot(hourly_df["Hour"], hourly_df["Rolling_Avg"], linestyle='--',
         color='#d95f02', linewidth=2, label='3-Hour Moving Average')

# Fill under the curve
plt.fill_between(hourly_df["Hour"], hourly_df["Departures"], color='#1f77b4', alpha=0.15)

# Annotate Morning Peak (8 AM)
am_peak_val = hourly_df.loc[hourly_df["Hour"] == 8, "Departures"].values[0]
plt.annotate(f"AM Peak: {am_peak_val:,} buses/hr\n(08:00 AM)",
             xy=(8, am_peak_val), xytext=(8.5, am_peak_val + 300),
             arrowprops=dict(facecolor='#d95f02', shrink=0.08, width=1.5, headwidth=7),
             fontweight='bold', fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#d95f02"))

# Annotate Afternoon / Evening Operations
pm_peak_val = hourly_df.loc[hourly_df["Hour"] == 15, "Departures"].values[0]
plt.annotate(f"Afternoon Peak: {pm_peak_val:,} buses/hr\n(03:00 PM)",
             xy=(15, pm_peak_val), xytext=(15.5, pm_peak_val + 300),
             arrowprops=dict(facecolor='#2ca02c', shrink=0.08, width=1.5, headwidth=7),
             fontweight='bold', fontsize=10, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#2ca02c"))

plt.title("Bengaluru 24-Hour Public Bus Service Profile (BMTC Trip Departures)", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Hour of the Day (24-Hour Format)", fontsize=11, fontweight='bold')
plt.ylabel("Number of Scheduled Departures", fontsize=11, fontweight='bold')
plt.xticks(range(0, 24), [f"{h:02d}:00" for h in range(24)], rotation=45, fontsize=9)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper left')
plt.tight_layout()

plt.savefig("outputs/10_time_series_24h_departures.png", dpi=300)
print("\nSaved 1: 24-Hour Time Series Plot -> outputs/10_time_series_24h_departures.png")
plt.close()


# ------------------------------------------------------------------------------
# 4. HOURLY HEATMAP BY SERVICE TIER
# ------------------------------------------------------------------------------
print("\n==================================================================")
print("3. HOURLY BREAKDOWN BY SERVICE TIER (CROSSTAB)")
print("==================================================================")

crosstab = pd.crosstab(time_df["service_type"], time_df["hour"]).reindex(columns=range(24), fill_value=0)
print(crosstab)

plt.figure(figsize=(12, 5))
sns.heatmap(
    crosstab,
    cmap="YlGnBu",
    linewidths=0.5,
    cbar_kws={'label': 'Scheduled Departures in Hour'},
    annot=False
)

plt.title("Hourly Service Density Heatmap across BMTC Tiers", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Hour of Day (00:00 - 23:00)", fontsize=11, fontweight='bold')
plt.ylabel("Service Tier", fontsize=11, fontweight='bold')
plt.xticks(ticks=[h + 0.5 for h in range(24)], labels=[f"{h:02d}:00" for h in range(24)], rotation=45, fontsize=9)
plt.tight_layout()

plt.savefig("outputs/11_time_series_tier_heatmap.png", dpi=300)
print("Saved 2: Hourly Service Tier Heatmap -> outputs/11_time_series_tier_heatmap.png")
plt.close()

# ------------------------------------------------------------------------------
# 5. EXPORT HOURLY METRICS TO CSV
# ------------------------------------------------------------------------------
hourly_df.to_csv("outputs/hourly_trip_departures.csv", index=False)
crosstab.reset_index().to_csv("outputs/hourly_by_service_tier.csv", index=False)

print("\nExported time-series tables:")
print("  - outputs/hourly_trip_departures.csv")
print("  - outputs/hourly_by_service_tier.csv")
print("Time series analysis script completed successfully!")

