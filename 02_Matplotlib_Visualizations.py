# ==============================================================================
# DATA VISUALIZATION WITH MATPLOTLIB: BMTC TRANSIT ANALYSIS
# ==============================================================================
# Matplotlib is the fundamental 2D plotting library in Python.
# It enables the creation of static, publication-quality visualizations.
#
# Plots covered in this file:
# 1. Horizontal Bar Plot (Top 12 Bus Interchange Hubs by Daily Trip Volume)
# 2. Histogram with Density Overlay (Distribution of Stop Counts per Route)
# 3. Multi-Variable Scatter Plot (Stop Count vs Daily Trips with Color Mapping)
# 4. Pie Chart (Share of BMTC Routes by Service Category with Explode & Shadow)
# 5. Grouped Bar Plot (Top High-Frequency Corridors: Forward vs Return trips)
# ==============================================================================

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Create outputs directory
os.makedirs("outputs", exist_ok=True)

# Load datasets
routes_path = "routes.csv" if os.path.exists("routes.csv") else "data/routes.csv"
agg_path = "aggregated.csv" if os.path.exists("aggregated.csv") else "data/aggregated.csv"

routes_df = pd.read_csv(routes_path)
agg_df = pd.read_csv(agg_path)

# Classify service type for routes
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


# ------------------------------------------------------------------------------
# 1. HORIZONTAL BAR PLOT: Top 12 Bengaluru Bus Interchanges
# ------------------------------------------------------------------------------
# A horizontal bar plot provides clear visibility for long categorical names.
# Here we compare total daily trips handled at major transit hubs.

top_12_hubs = agg_df.sort_values("trip_count", ascending=False).head(12).iloc[::-1]

plt.figure(figsize=(10, 6))
bars = plt.barh(top_12_hubs["name"], top_12_hubs["trip_count"], color="#1f77b4", edgecolor="#0b3c61", height=0.65)

# Highlight Majestic (Kempegowda Bus Station) in a distinct accent color
bars[-1].set_color("#d95f02")

# Annotate bar values
for bar in bars:
    w = bar.get_width()
    plt.text(w + 120, bar.get_y() + bar.get_height() / 2, f"{int(w):,}",
             va='center', fontsize=9, fontweight='bold', color="#222")

plt.xlabel("Total Daily Scheduled Bus Trips", fontsize=11, fontweight='bold')
plt.ylabel("Transit Hub / Junction", fontsize=11, fontweight='bold')
plt.title("Top 12 Busiest BMTC Bus Hubs in Bengaluru (Daily Trip Volume)", fontsize=13, fontweight='bold', pad=12)
plt.xlim(0, top_12_hubs["trip_count"].max() * 1.15)
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()

plt.savefig("outputs/01_matplotlib_top_hubs.png", dpi=300)
print("Saved 1: Horizontal Bar Plot -> outputs/01_matplotlib_top_hubs.png")
plt.close()


# ------------------------------------------------------------------------------
# 2. HISTOGRAM: Distribution of Route Lengths (Stop Counts per Route)
# ------------------------------------------------------------------------------
# A histogram displays the frequency distribution of a continuous variable.
# It reveals whether BMTC favors short feeder lines or long cross-city trunks.

plt.figure(figsize=(9, 5))
n, bins, patches = plt.hist(routes_df["stop_count"], bins=30, color="#2ca02c",
                            edgecolor="black", alpha=0.75, linewidth=1.0)

# Add statistical markers
mean_stops = routes_df["stop_count"].mean()
median_stops = routes_df["stop_count"].median()

plt.axvline(mean_stops, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_stops:.1f} stops')
plt.axvline(median_stops, color='blue', linestyle=':', linewidth=2, label=f'Median: {median_stops:.1f} stops')

plt.xlabel("Number of Stops along Route", fontsize=11, fontweight='bold')
plt.ylabel("Number of Route Directions", fontsize=11, fontweight='bold')
plt.title("Distribution of Route Lengths (Stops per Route Direction)", fontsize=13, fontweight='bold')
plt.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

plt.savefig("outputs/02_matplotlib_route_length_hist.png", dpi=300)
print("Saved 2: Route Length Histogram -> outputs/02_matplotlib_route_length_hist.png")
plt.close()


# ------------------------------------------------------------------------------
# 3. SCATTER PLOT: Stop Count vs Daily Trips (Multi-Variable Mapping)
# ------------------------------------------------------------------------------
# Scatter plots display relationships between two continuous variables.
# We map route stop count (X) against trip count (Y) with viridis color mapping.

plt.figure(figsize=(10, 6))

x = routes_df["stop_count"]
y = routes_df["trip_count"]
colors = routes_df["trip_count"]

scatter = plt.scatter(x, y, c=colors, cmap='viridis', alpha=0.65, edgecolors='none', s=25)

plt.xlabel("Stop Count (Route Length)", fontsize=11, fontweight='bold')
plt.ylabel("Daily Trip Count (Frequency)", fontsize=11, fontweight='bold')
plt.title("BMTC Route Length vs. Daily Trip Frequency", fontsize=13, fontweight='bold')
plt.colorbar(scatter, label='Daily Trip Frequency Intensity')
plt.grid(True, linestyle='--', alpha=0.5)

# Annotate the extreme high-frequency outlier
top_route = routes_df.loc[routes_df["trip_count"].idxmax()]
plt.annotate(f"Busiest: {top_route['name']} ({top_route['trip_count']} trips)",
             xy=(top_route["stop_count"], top_route["trip_count"]),
             xytext=(top_route["stop_count"] + 5, top_route["trip_count"] - 15),
             arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=7),
             fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig("outputs/03_matplotlib_scatter_stops_vs_trips.png", dpi=300)
print("Saved 3: Scatter Plot -> outputs/03_matplotlib_scatter_stops_vs_trips.png")
plt.close()


# ------------------------------------------------------------------------------
# 4. PIE CHART: Fleet Service Tiers Breakdown
# ------------------------------------------------------------------------------
# A pie chart illustrates numerical proportions. We show the share of BMTC routes
# across Ordinary, Metro Feeder, Vajra AC, and Vayu Vajra Airport services.

service_counts = routes_df["service_type"].value_counts()
labels = service_counts.index
values = service_counts.values
colors = ['#4a90e2', '#50e3c2', '#f5a623', '#e74c3c']
explode = (0.0, 0.12, 0.12, 0.18)  # Explode smaller specialty tiers

plt.figure(figsize=(8, 6))
patches, texts, autotexts = plt.pie(
    values,
    labels=labels,
    autopct='%1.1f%%',
    startangle=140,
    colors=colors,
    explode=explode,
    shadow=True,
    textprops={'fontsize': 10}
)

for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_color('black')

plt.title("Proportion of BMTC Route Directions by Service Tier", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()

plt.savefig("outputs/04_matplotlib_service_tier_pie.png", dpi=300)
print("Saved 4: Service Tier Pie Chart -> outputs/04_matplotlib_service_tier_pie.png")
plt.close()


# ------------------------------------------------------------------------------
# 5. GROUPED BAR PLOT: Top 5 Highest Frequency Corridors (Forward vs Return)
# ------------------------------------------------------------------------------
# Grouped bar plots allow visual comparison of two categories side by side.
# Here we check trip balance between Forward (Direction 0) and Return (Direction 1).

top_5_names = ['375-D', '401-M', '410-FA', '226-N', '600-F']
subset = routes_df[routes_df["name"].isin(top_5_names)]

fwd_trips = []
ret_trips = []

for rname in top_5_names:
    r_sub = subset[subset["name"] == rname]
    d0 = r_sub[r_sub["direction_id"] == 0]["trip_count"].values
    d1 = r_sub[r_sub["direction_id"] == 1]["trip_count"].values
    fwd_trips.append(d0[0] if len(d0) > 0 else 0)
    ret_trips.append(d1[0] if len(d1) > 0 else 0)

x_indices = np.arange(len(top_5_names))
bar_width = 0.35

plt.figure(figsize=(9, 5))
plt.bar(x_indices - bar_width/2, fwd_trips, width=bar_width, label='Forward Direction (0)',
        color='#2b5c8f', edgecolor='black', linewidth=0.8)
plt.bar(x_indices + bar_width/2, ret_trips, width=bar_width, label='Return Direction (1)',
        color='#e67e22', edgecolor='black', linewidth=0.8)

plt.xlabel("Route Name", fontsize=11, fontweight='bold')
plt.ylabel("Scheduled Daily Trips", fontsize=11, fontweight='bold')
plt.title("Forward vs. Return Trip Frequency on Top 5 Bengaluru Corridors", fontsize=13, fontweight='bold')
plt.xticks(x_indices, top_5_names, fontsize=10, fontweight='bold')
plt.legend(frameon=True, facecolor='white', framealpha=0.9)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()

plt.savefig("outputs/05_matplotlib_grouped_corridors.png", dpi=300)
print("Saved 5: Grouped Bar Plot -> outputs/05_matplotlib_grouped_corridors.png")
plt.close()

print("\nMatplotlib visualizations generated successfully!")
