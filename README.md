# RouteOptimizer360 🚚📍

**RouteOptimizer360** is a real-time vehicle routing and delivery optimization platform built using Python and Streamlit. It enables users to upload delivery locations, visualize them on a map, compute optimal delivery routes using heuristics/metaheuristics, and analyze KPIs like total distance, time, and cost.

## 🚀 Features

- Upload delivery location datasets (CSV format)
- Geocode addresses to coordinates
- Visualize delivery points on an interactive map
- Run optimization algorithms (e.g., Greedy, Genetic Algorithm)
- View optimized routes and key performance indicators (KPIs)
- Export results and download reports

## 🛠 Tech Stack

- **Python**: Core programming
- **Streamlit**: Frontend UI
- **Pandas**: Data manipulation
- **Geopy**: Geocoding
- **Folium**: Map visualization
- **NetworkX / OR-Tools**: Optimization algorithms

## 📂 How to Run Locally

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/routeoptimizer360.git
cd routeoptimizer360
```
# 2. Create Virtual Environment (Optional)

```
python -m venv venv
source venv/bin/activate
```
# 3. Install Dependencies

```
pip install -r requirements.txt
```

# 4. Run the Streamlit app
```
streamlit run app.py
```
## 📦 Sample Data Format
| Address               | Latitude | Longitude |
| --------------------- | -------- | --------- |
| 123 Main St, Boston   | 42.3601  | -71.0589  |
| 456 Elm St, Cambridge | 42.3736  | -71.1097  |

## 📈 KPIs Tracked
Total distance covered

Time and cost estimates

Number of deliveries per route
