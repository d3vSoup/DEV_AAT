# Topic #2: Public Transportation Usage Analysis — BMTC & Metro

## Recommended Project Titles
- **Academic / Formal (Recommended for Project Report & Viva):**  
  *Public Transportation Usage & Network Analysis: Empirical Study of BMTC Bus Operations in Bengaluru*
- **Data-Centric / Technical (Best for GitHub or Portfolio):**  
  *Bengaluru Transit Analytics: Exploratory Data Analysis & 24-Hour Operational Profiling of BMTC Network*
- **Short & Impactful (Best for a Presentation Title Slide):**  
  *Decoding Bengaluru's Transit: BMTC Route Utilization, Hub Density, & Commuter Patterns*

---

## 1. What is this Dataset?

This dataset captures the operational structure, schedules, and spatial layout of the **Bengaluru Metropolitan Transport Corporation (BMTC)**—one of India’s largest urban bus transit networks, serving over 3.5 to 4 million daily commuters across Bengaluru.

The data is split into three clean, complementary CSV files:

| File | Rows × Columns | What Each Row Represents | Key Columns |
| :--- | :---: | :--- | :--- |
| **`routes.csv`** | **7,475 × 8** | A single **directional route** (e.g., Kengeri $\rightarrow$ Banashankari). | `name` (Route code, e.g., 375-D), `full_name` (Origin $\rightarrow$ Destination), `trip_count` (total daily trips), `stop_count` (number of stops), `trip_list` (timestamps of all departures), `direction_id` (0 for outbound, 1 for return). |
| **`stops.csv`** | **9,960 × 6** | An individual **bus stop platform** in the city. | `name` (Stop name), `trip_count` (total buses passing this platform per day), `route_count` (number of distinct routes serving it), `id` (Stop ID). |
| **`aggregated.csv`** | **5,211 × 5** | A **merged transit junction/hub** (combines both directions and multiple platforms of the same physical stop). | `name` (Junction name like Majestic, Silk Board, Corporation), `trip_count` (total daily buses through the junction), `route_count` (total unique routes passing through). |

---

## 2. Where Did We Get This Dataset From?

1. **Primary Origin:** The raw data originates from the official **Namma BMTC** mobile application APIs operated by BMTC and the Government of Karnataka (`nammabmtcapp.karnataka.gov.in`).
2. **Open-Data Conversion:** Transit researchers and developers reverse-engineered the API responses and structured them into the globally standardized **General Transit Feed Specification (GTFS)** format (available under the Open Database License - ODbL).
3. **Extraction & Processing:** The raw GTFS files (`trips.txt`, `stops.txt`, `routes.txt`, `stop_times.txt`) were compiled into clean CSVs (`routes.csv`, `stops.csv`, `aggregated.csv`) by parsing timetable arrays and mapping terminal connections.

---

## 3. What Are We Supposed to Do With This Dataset?

The objective of analyzing this dataset is **Urban Transit Intelligence and Network Optimization**:

1. **Identify Transit Super-Hubs:** Locate major congestion and passenger transfer points across Bengaluru to understand where infrastructure and terminal capacity are most critical.
2. **Analyze Route Utilization & Frequency:** Determine which corridors are high-frequency arteries (running every 5–10 minutes) versus low-frequency suburban/rural feeders.
3. **Commuter Rush Hour Profiling:** Discover the exact citywide peak departure hours (morning vs. afternoon/evening peaks).
4. **Service Tier Comparison:** Compare regular non-AC buses (`Ordinary`), IT/AC corridor buses (`Vajra AC`), 24/7 Airport shuttles (`Vayu Vajra`), and Metro Feeder buses (`MF-`).
5. **Metro-Bus Multimodal Integration:** Quantify how effectively the bus network feeds into Namma Metro stations.

---

## 4. How Are We Supposed to Work on This Dataset?

Follow a standard 5-step data science workflow:

```text
1. Data Ingestion & Audit
   └─ Load CSVs using Pandas (pd.read_csv). Inspect shapes, data types, and check null counts.

2. Feature Engineering
   ├─ Classify 'service_type' using route naming conventions:
   │  ('KIA' → Vayu Vajra, 'V-' → Vajra AC, 'MF' → Metro Feeder, else → Ordinary)
   ├─ Extract 'origin' and 'destination' by splitting 'full_name' on the arrow ('→').
   └─ Parse timestamps from 'trip_list' to extract the departure hour of the day (0 to 23).

3. Aggregation & Grouping
   ├─ Group by 'service_type' to calculate total routes, average stops, and total daily trips.
   └─ Sort and filter for top hubs, busy corridors (≥ 100 trips/day), and Metro-interchange stops.

4. Statistical Analysis
   └─ Compute mean, median, IQR, and correlations between route length and trip frequencies.

5. Visual Storytelling
   └─ Generate focused charts with Matplotlib, Seaborn, and Plotly, saving PNGs and interactive HTMLs.
```

---

## 5. Visualizations, Rationale, and Exact X & Y Axis Mappings

### Chart 1: Top 12 Transit Super-Hubs
- **Plot Type:** **Horizontal Bar Chart** (`plt.barh` or `px.bar`)
- **Dataset:** `aggregated.csv`
- **X-axis:** `trip_count` (Continuous: Total scheduled trips per day through that junction)
- **Y-axis:** `name` (Categorical: Hub name like Kempegowda Bus Station, Corporation, Town Hall)
- **Why use it:** Horizontal bars prevent label overlap and cleanly rank the highest-traffic hubs in descending order.
- **Key Insight:** Kempegowda Bus Station (Majestic) is the central bottleneck with over 10,500 daily trips, followed by Corporation with 8,200+.

---

### Chart 2: Route Length Distribution (Stop Counts)
- **Plot Type:** **Histogram with KDE / Vertical Markers** (`plt.hist`)
- **Dataset:** `routes.csv`
- **X-axis:** `stop_count` (Continuous: Number of bus stops on that route direction)
- **Y-axis:** Frequency / Number of Routes (Count of routes having that length)
- **Why use it:** Shows whether BMTC designs short local connector routes or long cross-city lines.
- **Key Insight:** Most routes have between 20 and 40 stops (median = 28), with long suburban routes stretching up to 96 stops.

---

### Chart 3: Route Length vs. Daily Trip Frequency
- **Plot Type:** **Scatter Plot with Color Mapping** (`plt.scatter` or `sns.regplot`)
- **Dataset:** `routes.csv`
- **X-axis:** `stop_count` (Continuous: Route length)
- **Y-axis:** `trip_count` (Continuous: Daily trip volume)
- **Color Scale (C or Hue):** `trip_count` intensity or `service_type`
- **Why use it:** Investigates whether longer routes run less frequently or if short routes get high frequency.
- **Key Insight:** High-frequency routes ($\ge 150\text{ trips}$) are concentrated in medium-length corridors (25–40 stops), such as the Kengeri-Banashankari Ring Road corridor.

---

### Chart 4: Service Tier Fleet Proportion
- **Plot Type:** **Pie Chart with Explode & Shadow** (`plt.pie`)
- **Dataset:** `routes.csv`
- **Values / Slice Size:** Route count per `service_type` (`Ordinary`, `Vajra AC`, `Metro Feeder`, `Vayu Vajra`)
- **Labels:** Service tier names
- **Why use it:** Demonstrates the composition of Bengaluru's bus network at a single glance.
- **Key Insight:** Over 94% of all routes are Ordinary/General commuter buses, while AC Vajra, Airport, and Metro Feeders make up specialized high-frequency niches.

---

### Chart 5: Corridor Directional Balance (Forward vs. Return)
- **Plot Type:** **Grouped Bar Plot** (`plt.bar` with offset X)
- **Dataset:** `routes.csv` (filtered to top 5 corridors: `375-D`, `401-M`, `410-FA`, `226-N`, `600-F`)
- **X-axis:** Route Name (`name`)
- **Y-axis:** `trip_count`
- **Grouping Category (Hue):** `direction_id` (0 = Forward, 1 = Return)
- **Why use it:** Compares symmetry of service—checking whether buses return with equal frequency or deadhead back.
- **Key Insight:** Routes like `226-N` (Bidadi $\leftrightarrow$ Majestic) are perfectly balanced (155 trips each way), whereas ring-road routes show minor directional variation during peak shifts.

---

### Chart 6: Statistical Trip Distribution Across Service Tiers
- **Plot Type:** **Box Plot / Violin Plot** (`sns.boxplot` / `sns.violinplot`)
- **Dataset:** `routes.csv`
- **X-axis:** `service_type` (Categorical: Ordinary, Metro Feeder, Vajra AC, Vayu Vajra)
- **Y-axis:** `trip_count` or `stop_count` (Continuous)
- **Why use it:** Box and violin plots display medians, interquartile ranges (IQR), and data spread without being distorted by extreme outliers.
- **Key Insight:** Vayu Vajra (Airport) routes have the highest median trip count (25.4 trips/route) because they run around the clock, whereas Ordinary routes have a lower median but contain extreme high-frequency outliers.

---

### Chart 7: 24-Hour Departure Frequency (Transit Supply Curve)
- **Plot Type:** **Time-Series Line Plot with Shaded Fill** (`plt.plot` + `plt.fill_between`)
- **Dataset:** Derived from `trip_list` in `routes.csv` (57,836 parsed timestamps)
- **X-axis:** `Hour` (00:00 to 23:00 across the day)
- **Y-axis:** `Departures` (Total citywide bus departures during that hour)
- **Why use it:** Identifies peak commuter pressure and service valleys over a 24-hour cycle.
- **Key Insight:**
  - **Morning Peak:** **08:00 AM** with **4,504 bus departures/hour**.
  - **Afternoon/Evening Peaks:** **03:00 PM** (4,029/hr) and **05:00 PM** (3,696/hr).
  - **Night Operations:** Drops after 10 PM down to 30–70 departures/hour, operated primarily by airport shuttles.

---

### Chart 8: Hourly Service Density Heatmap
- **Plot Type:** **Heatmap** (`sns.heatmap`)
- **Dataset:** Crosstab of `service_type` vs. `Hour`
- **X-axis:** `Hour of Day` (0 to 23)
- **Y-axis:** `Service Tier` (Ordinary, Vajra AC, Metro Feeder, Vayu Vajra)
- **Color Intensity (Z):** Scheduled departure count in that specific hour
- **Why use it:** Instantly reveals operational differences between services across time.
- **Key Insight:** Vayu Vajra maintains a consistent color across all 24 hours (24/7 service), while Metro Feeders and Ordinary lines light up sharply during work-commute hours (7–10 AM and 4–8 PM).

---

### Chart 9: Interactive Corridor Explorer & Sunburst Diagram
- **Plot Type:** **Interactive Sunburst & Hover Bar** (`px.sunburst`, `px.bar`)
- **Dataset:** `routes.csv`
- **Hierarchy:** `service_type` $\rightarrow$ `name`
- **Values:** `trip_count`
- **Why use it:** Allows an audience or examiner to click, zoom in, and hover over specific routes to inspect terminal endpoints and stops interactively.

---

## 6. Summary Checklist for Viva / Presentation

1. *"We analyzed the complete operational GTFS transit network of BMTC Bengaluru, encompassing 9,960 bus stops and 7,475 route directions across the city."*
2. *"Using Pandas, Matplotlib, Seaborn, and Plotly, we engineered features for service categories and extracted over 57,000 scheduled departure timestamps to evaluate network density, hub congestion, and hourly rush-hour trends."*
3. *"Our findings highlight significant traffic concentration at central junctions like Majestic and Corporation, identify major ring-road corridors as the highest-frequency transit arteries, and chart the citywide commute profile peaking at 8:00 AM and 3:00–5:00 PM."*
