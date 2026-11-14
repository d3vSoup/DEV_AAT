# Public Transportation Usage Analysis — BMTC & Metro (Topic #2)

Empirical data analysis and operational profiling of the Bengaluru Metropolitan Transport Corporation (BMTC) public bus network using Python, Pandas, Matplotlib, Seaborn, and Plotly.

---

## 📖 Comprehensive Documentation
For in-depth project documentation, research motivation, methodology, and visualization specifications, see **[`usecase.md`](usecase.md)**.

---

## 📂 Project Structure

```text
DEV_AAT/
├── routes.csv                     # 7,475 route directions, trip frequencies, stop lists
├── stops.csv                      # 9,960 individual bus stops across Bengaluru
├── aggregated.csv                 # 5,211 merged transit junctions and bus hubs
├── usecase.md                     # Complete project explanation, objectives, & chart specs
│
├── 01_Data_Manipulation.py        # Pandas loading, filtering, feature engineering, & exports
├── 02_Matplotlib_Visualizations.py# Horizontal bar, histogram, scatter, pie, & grouped bar
├── 03_Seaborn_Aesthetics.py       # Boxplot, violin plot, regplot, & correlation heatmap
├── 04_Time_Series_Data.py         # 24-hour departure profile, rolling average, & hourly heatmap
├── 05_Plotly_Interactive.py       # Interactive Plotly charts exported to browser HTML
│
└── outputs/                       # Generated PNG charts, HTML files, & summary CSVs
    ├── 01_matplotlib_top_hubs.png
    ├── 02_matplotlib_route_length_hist.png
    ├── 03_matplotlib_scatter_stops_vs_trips.png
    ├── 04_matplotlib_service_tier_pie.png
    ├── 05_matplotlib_grouped_corridors.png
    ├── 06_seaborn_boxplot_service_trips.png
    ├── 07_seaborn_violin_route_length.png
    ├── 08_seaborn_regression_stops_vs_trips.png
    ├── 09_seaborn_correlation_heatmap.png
    ├── 10_time_series_24h_departures.png
    ├── 11_time_series_tier_heatmap.png
    ├── bmtc_top_corridors_interactive.html
    ├── bmtc_service_hierarchy_sunburst.html
    ├── bmtc_24h_profile_interactive.html
    ├── top_10_transit_hubs.csv
    ├── service_tier_summary.csv
    ├── metro_connected_stops.csv
    ├── top_50_high_freq_routes.csv
    ├── hourly_trip_departures.csv
    └── hourly_by_service_tier.csv
```

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3 and the required libraries installed:
```bash
pip install pandas numpy matplotlib seaborn plotly
```

### Running the Analysis
Execute the modular scripts sequentially:

```bash
# 1. Core data manipulation, feature engineering, and summary exports
python3 01_Data_Manipulation.py

# 2. Matplotlib statistical plots
python3 02_Matplotlib_Visualizations.py

# 3. Seaborn styled statistical visualizations
python3 03_Seaborn_Aesthetics.py

# 4. 24-Hour transit supply and departure time-series analysis
python3 04_Time_Series_Data.py

# 5. Plotly interactive charts (generates standalone HTML viewers in outputs/)
python3 05_Plotly_Interactive.py
```

---

## 📊 Key Findings
- **Transit Hub Concentration:** Kempegowda Bus Station (Majestic) is the central bottleneck with over **10,500** daily scheduled trips, followed by Corporation with **8,200+** trips.
- **Top Arterial Corridors:** Outer ring-road corridors like `375-D` (Kengeri $\leftrightarrow$ Banashankari) and `378` (Kengeri $\rightarrow$ Electronic City) have the highest trip frequencies ($170\text{--}200+$ trips/day).
- **24-Hour Commute Profile:** Citywide bus departures peak at **08:00 AM** ($4,504$ departures/hour) and maintain high throughput through the afternoon ($4,029/\text{hr}$ at 3:00 PM).
- **Multimodal Feeder Network:** **228** dedicated Metro Feeder (`MF-`) routes interface across **97** bus stops directly adjacent to Namma Metro stations.
