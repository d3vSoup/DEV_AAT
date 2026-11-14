# ==============================================================================
# INTERACTIVE DATA VISUALIZATION WITH PLOTLY EXPRESS: BMTC TRANSIT
# ==============================================================================
# Plotly Express (px) is a high-level Python visualization library designed for
# creating interactive, publication-quality figures with simple syntax.
#
# Unlike static charts (Matplotlib/Seaborn), Plotly figures allow users to:
# - Zoom and Pan dynamically across routes and stops
# - Hover to reveal rich tooltips (terminals, trip count, service tier)
# - Toggle traces and categories on/off interactively in the legend
# - Save interactive standalone HTML files for presentation in any web browser
#
# Visualizations covered in this file:
# 1. Interactive Bar Chart: Top 25 High-Frequency Bus Corridors in Bengaluru
# 2. Interactive Sunburst Hierarchy: Service Tier -> Route Breakdown
# 3. Interactive Time-Series Line Plot: 24-Hour Departure Trends by Tier
# ==============================================================================

import pandas as pd
import plotly.express as px
import re
import os

# Create outputs directory
os.makedirs("outputs", exist_ok=True)

# Load routes dataset
routes_path = "routes.csv" if os.path.exists("routes.csv") else "data/routes.csv"
routes_df = pd.read_csv(routes_path)

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
# 1. INTERACTIVE BAR CHART: Top 25 High-Frequency Bus Corridors
# ------------------------------------------------------------------------------
print("Generating 1: Interactive Bar Chart of Top 25 Corridors...")

top_25 = routes_df.sort_values("trip_count", ascending=False).head(25)

fig_bar = px.bar(
    top_25,
    x="trip_count",
    y="full_name",
    color="service_type",
    orientation="h",
    hover_data={
        "name": True,
        "trip_count": True,
        "stop_count": True,
        "direction_id": True,
        "full_name": False
    },
    labels={
        "trip_count": "Scheduled Daily Trips",
        "full_name": "Bus Corridor (Origin → Destination)",
        "service_type": "Service Tier"
    },
    title="Top 25 Highest-Frequency BMTC Bus Corridors in Bengaluru",
    color_discrete_map={
        "Ordinary": "#3366cc",
        "Metro Feeder": "#109618",
        "Vajra AC": "#ff9900",
        "Vayu Vajra (Airport)": "#dc3912"
    }
)

fig_bar.update_layout(
    yaxis={'categoryorder': 'total ascending'},
    height=750,
    margin=dict(l=20, r=20, t=50, b=20),
    template="plotly_white"
)

fig_bar.write_html("outputs/bmtc_top_corridors_interactive.html")
print("Saved HTML: outputs/bmtc_top_corridors_interactive.html")


# ------------------------------------------------------------------------------
# 2. INTERACTIVE SUNBURST CHART: Service Tier Hierarchy
# ------------------------------------------------------------------------------
# Sunburst charts visualize hierarchical data radiating outwards from root to leaves.

print("\nGenerating 2: Interactive Sunburst Chart of Service Tiers & Top Routes...")

# Filter top 8 routes per service tier for a clean hierarchy
top_routes_by_tier = routes_df.sort_values("trip_count", ascending=False).groupby("service_type").head(8).reset_index(drop=True)

fig_sunburst = px.sunburst(
    top_routes_by_tier,
    path=["service_type", "name"],
    values="trip_count",
    color="trip_count",
    color_continuous_scale="Viridis",
    title="BMTC Service Hierarchy: Service Tiers -> Top Route Daily Trips",
    hover_data=["stop_count"]
)

fig_sunburst.update_layout(
    height=650,
    margin=dict(l=10, r=10, t=50, b=10),
    template="plotly_white"
)

fig_sunburst.write_html("outputs/bmtc_service_hierarchy_sunburst.html")
print("Saved HTML: outputs/bmtc_service_hierarchy_sunburst.html")


# ------------------------------------------------------------------------------
# 3. INTERACTIVE 24-HOUR DEPARTURE TIME SERIES
# ------------------------------------------------------------------------------
print("\nGenerating 3: Interactive 24-Hour Time Series by Service Tier...")

records = []
for _, row in routes_df.iterrows():
    stype = row["service_type"]
    trip_str = str(row["trip_list"])
    hours = re.findall(r"'(\d{2}):\d{2}:\d{2}'", trip_str)
    for h in hours:
        records.append({"hour": int(h), "service_type": stype})

time_df = pd.DataFrame(records)
hourly_tier = time_df.groupby(["hour", "service_type"]).size().reset_index(name="departures")

fig_time = px.line(
    hourly_tier,
    x="hour",
    y="departures",
    color="service_type",
    markers=True,
    labels={
        "hour": "Hour of Day (00:00 to 23:00)",
        "departures": "Scheduled Departures / Hour",
        "service_type": "Service Tier"
    },
    title="Interactive 24-Hour Service Profile by BMTC Tier (Hover to inspect)",
    color_discrete_map={
        "Ordinary": "#3366cc",
        "Metro Feeder": "#109618",
        "Vajra AC": "#ff9900",
        "Vayu Vajra (Airport)": "#dc3912"
    }
)

fig_time.update_layout(
    xaxis=dict(tickmode='linear', tick0=0, dtick=1),
    template="plotly_white",
    hovermode="x unified"
)

fig_time.write_html("outputs/bmtc_24h_profile_interactive.html")
print("Saved HTML: outputs/bmtc_24h_profile_interactive.html")

print("\nPlotly interactive visualizations generated successfully!")
print("Open any generated .html file in your browser to interact with the visualizations.")
