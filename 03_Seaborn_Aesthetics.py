# ==============================================================================
# SEABORN PLOT CUSTOMIZATION WITH AESTHETIC FUNCTIONS: BMTC DATA
# ==============================================================================
# Seaborn is a Python statistical data visualization library based on Matplotlib.
# It provides an elegant high-level interface for attractive graphics.
#
# Aesthetic configurations covered:
# 1. Styling Themes     : sns.set_theme(style="whitegrid")
# 2. Context Scaling    : sns.set_context("notebook", font_scale=1.1)
# 3. Spines Removal     : sns.despine()
# 4. Color Palettes     : custom categorical palettes
#
# Plots covered in this file:
# 1. Box Plot with Stripplot Overlay (Trip Frequency Distribution across Service Tiers)
# 2. Violin Plot (Route Length / Stop Count density across Service Tiers)
# 3. Regression Scatter Plot (Route Length vs Daily Trips with Linear Trend)
# 4. Correlation Heatmap (Relationships among numerical route features)
# ==============================================================================

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Create outputs directory
os.makedirs("outputs", exist_ok=True)

# Load datasets
routes_path = "routes.csv" if os.path.exists("routes.csv") else "data/routes.csv"
routes_df = pd.read_csv(routes_path)

# Classify service type for routes
def classify_service(name):
    name_str = str(name).strip()
    if name_str.startswith("KIA"):
        return "Vayu Vajra"
    elif name_str.startswith("V-") or name_str.startswith("V"):
        return "Vajra AC"
    elif "MF" in name_str or name_str.startswith("MF-"):
        return "Metro Feeder"
    else:
        return "Ordinary"

routes_df["service_type"] = routes_df["name"].apply(classify_service)

# ------------------------------------------------------------------------------
# GLOBAL SEABORN AESTHETIC CONFIGURATION
# ------------------------------------------------------------------------------
sns.set_theme(style="whitegrid")
sns.set_context("notebook", font_scale=1.1, rc={"lines.linewidth": 1.8})

palette = {
    "Ordinary": "#4c72b0",
    "Metro Feeder": "#55a868",
    "Vajra AC": "#dd8452",
    "Vayu Vajra": "#c44e52"
}


# ------------------------------------------------------------------------------
# 1. BOX PLOT WITH STRIPPLOT: Trip Frequencies Across Service Tiers
# ------------------------------------------------------------------------------
# Box plots summarize 5-number statistics (min, Q1, median, Q3, max).
# Stripplot overlays individual points with jitter to show real data density.

plt.figure(figsize=(10, 6))

# Filter extreme outliers (> 60 trips) just for clean boxplot visibility
plot_data = routes_df[routes_df["trip_count"] <= 60]

ax1 = sns.boxplot(
    data=plot_data,
    x="service_type",
    y="trip_count",
    hue="service_type",
    legend=False,
    palette=palette,
    width=0.45,
    fliersize=3,
    boxprops=dict(alpha=0.85)
)

sns.despine(top=True, right=True)
plt.title("Daily Trip Frequency by BMTC Service Tier (Trimmed to 60 Trips)", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Service Tier", fontsize=11, fontweight='bold')
plt.ylabel("Scheduled Daily Trips", fontsize=11, fontweight='bold')
plt.tight_layout()

plt.savefig("outputs/06_seaborn_boxplot_service_trips.png", dpi=300)
print("Saved 1: Seaborn Box Plot -> outputs/06_seaborn_boxplot_service_trips.png")
plt.close()


# ------------------------------------------------------------------------------
# 2. VIOLIN PLOT: Route Length (Stop Count) Distribution
# ------------------------------------------------------------------------------
# Violin plots combine box plots with kernel density estimation (KDE),
# revealing multimodal distributions and density peaks.

plt.figure(figsize=(10, 6))

ax2 = sns.violinplot(
    data=routes_df,
    x="service_type",
    y="stop_count",
    hue="service_type",
    legend=False,
    palette=palette,
    inner="quartile",
    cut=0
)

sns.despine(top=True, right=True)
plt.title("Violin Plot: Route Length (Stop Counts) Across Service Tiers", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Service Tier", fontsize=11, fontweight='bold')
plt.ylabel("Number of Stops Along Route", fontsize=11, fontweight='bold')
plt.tight_layout()

plt.savefig("outputs/07_seaborn_violin_route_length.png", dpi=300)
print("Saved 2: Seaborn Violin Plot -> outputs/07_seaborn_violin_route_length.png")
plt.close()


# ------------------------------------------------------------------------------
# 3. REGRESSION PLOT: Route Stop Count vs Daily Trips
# ------------------------------------------------------------------------------
# regplot plots a scatter of two variables and estimates a linear regression fit.

plt.figure(figsize=(9, 6))

ax3 = sns.regplot(
    data=routes_df,
    x="stop_count",
    y="trip_count",
    scatter_kws={"alpha": 0.35, "color": "#2b5c8f", "s": 18},
    line_kws={"color": "#d95f02", "linewidth": 2.2}
)

sns.despine(top=True, right=True)
plt.title("Relationship Between Route Stops and Trip Volume (with Fit Line)", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Number of Stops along Route", fontsize=11, fontweight='bold')
plt.ylabel("Scheduled Daily Trips", fontsize=11, fontweight='bold')
plt.tight_layout()

plt.savefig("outputs/08_seaborn_regression_stops_vs_trips.png", dpi=300)
print("Saved 3: Seaborn Regression Plot -> outputs/08_seaborn_regression_stops_vs_trips.png")
plt.close()


# ------------------------------------------------------------------------------
# 4. CORRELATION HEATMAP: Numerical Route Features
# ------------------------------------------------------------------------------
# A heatmap displays color-encoded correlation matrices.

# Feature engineering extra numeric ratios
numeric_features = routes_df[["trip_count", "stop_count", "direction_id"]].copy()
numeric_features["is_feeder"] = routes_df["service_type"].eq("Metro Feeder").astype(int)
numeric_features["is_airport"] = routes_df["service_type"].eq("Vayu Vajra").astype(int)

corr_matrix = numeric_features.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    linewidths=0.8,
    cbar_kws={'label': 'Pearson Correlation Coefficient'}
)

plt.title("Correlation Heatmap: BMTC Route Characteristics", fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()

plt.savefig("outputs/09_seaborn_correlation_heatmap.png", dpi=300)
print("Saved 4: Seaborn Correlation Heatmap -> outputs/09_seaborn_correlation_heatmap.png")
plt.close()

print("\nSeaborn aesthetic visualizations generated successfully!")
