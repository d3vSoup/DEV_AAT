# Public Transportation Usage Analysis — BMTC & Metro (Topic #2)

Empirical data analysis and operational profiling of the Bengaluru Metropolitan Transport Corporation (BMTC) public bus network using Python, Pandas, Matplotlib, and Seaborn.

---

## 📖 Project Documentation
Detailed explanations of the dataset, data source, objectives, and chart mappings can be found in **[`usecase.md`](usecase.md)**.

---

## 📂 Project Structure

```text
DEV_AAT/
├── routes.csv                     # 7,475 route directions, trip frequencies, stop lists
├── stops.csv                      # 9,960 individual bus stops across Bengaluru
├── aggregated.csv                 # 5,211 merged transit junctions and bus hubs
├── usecase.md                     # Comprehensive project guide and viva notes
│
├── 01_Data_Manipulation.py        # Pandas inspection, filtering, and groupby operations
├── 02_Matplotlib_Visualizations.py# Bar, histogram, scatter, and pie charts
├── 03_Seaborn_Aesthetics.py       # Boxplot, violin plot, and correlation heatmap
└── 04_Time_Series_Data.py         # 24-hour departure time-series plot
```

---

## 🚀 How to Run

Run any of the Python files directly to display the outputs on screen:

```bash
python3 01_Data_Manipulation.py
python3 02_Matplotlib_Visualizations.py
python3 03_Seaborn_Aesthetics.py
python3 04_Time_Series_Data.py
```
