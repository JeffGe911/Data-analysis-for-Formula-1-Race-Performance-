# F1 Pit Stop and Lap Time Analysis (2022–2024)

## Introduction
My project looks at Formula 1 pit stop efficiency and lap time consistency from 2022 to 2024. As an F1 fan, I've always wondered: do faster pit stops actually help drivers perform better on track? I wanted to see if teams with quick pit crews also have drivers with more consistent lap times. Basically, does having a great pit crew = better driver consistency? Let's find out.

## Data Sources

| Source | Link | Format | Description |
|--------|------|--------|-------------|
| Formula 1 World Championship (1950–2024) | [Kaggle Dataset](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020) | CSV | Official F1 race data including races, results, drivers, lap times, and pit stops |
| Formula 1 Pit Stop Dataset (2022–2024) | [Kaggle Link](https://www.kaggle.com/datasets/akashrane2609/formula-1-pit-stop-dataset) | CSV | Detailed pit-stop events, tire info, lap numbers, weather conditions |
| OpenF1 API | https://api.openf1.org | JSON (REST API) | Driver and team metadata (broadcast names, team info, etc.) |

The Kaggle dataset includes:
- `races.csv` – race metadata (season, circuit, date)
- `results.csv` – finishing positions, points, grid positions
- `lap_times.csv` – every lap time for every driver
- `pit_stops.csv` – pit stop lap numbers and durations
- `drivers.csv` – driver names and codes
- /drivers, /races, /laps - Supplement CSVs from API with team/driver metadata, enrich with real-time identifiers

I preprocessed everything for the 2022-2024 races only.

### API Integration
I also grabbed driver info from the OpenF1 API since it has cleaner team names and broadcast names; it played a key role in ensuring consistency across merged datasets.
```python
import requests
response = requests.get("https://api.openf1.org/v1/drivers?year=?")
if response.status_code == 200:
    drivers_data = response.json()
    # extract team names and driver info
```


## Analysis
Metrics Analyzed
1. Average Pit Stop Time – Measured per team and per driver, from all race stops between 2022–2024.
2. Lap Time Variance – Standard deviation of lap times for each driver, reflecting consistency.
3. Grid-to-Finish Correlation – Comparison of starting position vs finishing result.
4. Position Gains – Difference between grid and final position.
5. Operational Performance Consistency – Variability across races for top teams.
6. Correlation Heatmap – Relationship between performance metrics.
Methods Used
SQL-based data filtering and joins for structured event data (following relational database design discussed in class on Nov 4).
API integration (via requests) to get external driver info and validate data sources.
Group-by aggregation and pandas EDA pipelines for metric calculation.
Standard deviation and correlation coefficient are used to analyze trends.
Matplotlib and seaborn are used for clean, labeled charts.
## Visualizations
Bubble plot: Qualifying Position vs Finishing Position
Bar chart: Average Pit Stop Duration by Team
Bar chart: Lap Time Variance by Driver
Correlation heatmap of metrics
(optionally) Pit Stop Over Time Line Charts or Driver Comparison Over Years

SQL Statement used:
SELECT driver_id, AVG(pit_time_ms) 
FROM pit_stops 
WHERE year BETWEEN 2022 AND 2024 
GROUP BY driver_id;

## Summary of Results
Drivers with faster pit stops generally showed more consistent lap times, and starting grid position strongly influenced final race results.

## How to Run

### Setup
1. Download the F1 dataset from the Kaggle link above
2. Extract the CSV files into a `data/` folder in the project root
3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Analysis
Option 1 - Run the Jupyter notebook:
```bash
jupyter notebook notebooks/results.ipynb
```

Option 2 - Run from command line:
```bash
python main.py
```

The code is organized into modules in the `src/` folder and needs to run from 1 to 2 to 3 in order
1- `load_data.py` – loads CSVs and filters for 2022-2024 
2- `preprocessing.py` – calculates pit stop averages and lap time variance
3- `analysis.py` – creates all the visualizations

Results get saved to the `results/` folder.

### Notes
- The OpenF1 API is public
- Make sure you download the data yourself – it's not in the repo
- If you get any errors about missing data files, double-check that all the CSVs are in the `data/` folder
