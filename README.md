# 📊 India Unemployment Rate Analysis (2020)

A data analysis project exploring India's unemployment trends during 2020, with a focus on the COVID-19 pandemic's impact on employment across regions.

---

## 📁 Project Structure

```
├── Unemployment analysis.py           # Main analysis script
├── Unemployment_Rate_upto_11_2020.csv # Primary dataset (monthly, by region)
├── Unemployment in India.csv          # Secondary dataset (urban vs rural)
├── Unemployment_analysis_report.pdf   # Analysis and insight report
├── output/
│   ├── unemployment_trend.png         # Line chart of unemployment over time
│   ├── urban_rural_comparison.png     # Urban vs rural boxplot
│   ├── statistical_impact.png         # Lockdown vs recovery bar chart
│   ├── sna_correlation_network.png    # Regional correlation network graph
│   └── animated_unemployment_map.html # Animated geospatial heatmap
```

---

## 📌 Features

- **Unemployment Trend Analysis** — Line chart of national unemployment rate across 2020, with the initial COVID-19 lockdown period highlighted
- **Urban vs Rural Comparison** — Boxplot comparing unemployment distribution between urban and rural areas
- **Statistical Impact Analysis** — T-test comparing lockdown (Apr–Jun) vs recovery (Jul–Nov) unemployment rates
- **Social Network Analysis (SNA)** — Bipartite and correlation networks revealing which regions had similar unemployment patterns
- **Animated Geospatial Map** — Interactive, month-by-month animated map of regional unemployment rates across India

---

## 🛠️ Requirements

Install dependencies with:

```bash
pip install pandas matplotlib seaborn plotly networkx scipy
```

| Library | Purpose |
|---|---|
| `pandas` | Data loading and preprocessing |
| `matplotlib` / `seaborn` | Static charts and visualizations |
| `plotly` | Animated interactive geospatial map |
| `networkx` | Social Network Analysis (SNA) |
| `scipy` | Statistical t-test |

---

## 🚀 Usage

1. Clone the repository and navigate to the project folder:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Install dependencies:

```bash
pip install pandas matplotlib seaborn plotly networkx scipy
```

3. Run the analysis:

```bash
python analysis.py
```

4. All output files will be saved to the `output/` folder. Open `animated_unemployment_map.html` in a browser to view the interactive map.

---

## 📂 Datasets

| File | Description |
|---|---|
| `Unemployment_Rate_upto_11_2020.csv` | Monthly unemployment rate by Indian state/region (Jan–Nov 2020), includes latitude/longitude |
| `Unemployment in India.csv` | Unemployment data segmented by urban and rural areas |

> **Note:** The latitude and longitude columns in `Unemployment_Rate_upto_11_2020.csv` are stored in swapped order in the raw CSV. This is corrected automatically in the `plot_animated_map()` function.

---

## 📈 Key Findings

- Unemployment spiked sharply during the **initial lockdown period (April–June 2020)**, with some regions exceeding 70%
- A statistically significant difference was found between lockdown and recovery periods (p < 0.05)
- Urban areas showed higher unemployment volatility compared to rural areas
- Regional SNA revealed clusters of states with strongly correlated unemployment trajectories

---

## ⚠️ Known Issues & Fixes

- **Swapped lat/lon in CSV** — The raw dataset has latitude and longitude values in reversed columns. The `plot_animated_map()` function swaps them back automatically before plotting.
- **Animation frame ordering** — Animation frames use `YYYY-MM` format internally to ensure chronological ordering, then display human-readable month names on hover.

---

## 📄 License

This project is for educational and analytical purposes. Dataset sourced from public domain unemployment records.
