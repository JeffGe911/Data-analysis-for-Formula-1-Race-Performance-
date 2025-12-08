# Formula 1 Pit Stop and Lap Time Analysis (2022–2024)

## Introduction
My project looks at Formula 1 pit stop efficiency and lap time consistency from 2022 to 2024. As an F1 fan, I've always wondered: do faster pit stops actually help drivers perform better on track? I wanted to see if teams with quick pit crews also have drivers with more consistent lap times. Basically, does having a great pit crew = better driver consistency? Let's find out.

## Data Sources

| Source | Link | Format | Description |
|--------|------|--------|-------------|
| Formula 1 World Championship (1950–2024) | [Kaggle Dataset](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020) | CSV | Official F1 race data including races, results, drivers, lap times, and pit stops |
| Formula 1 Pit Stop Dataset (2022–2024) | [Kaggle Link](https://www.kaggle.com/datasets/akashrane2609/formula-1-pit-stop-dataset) | CSV | Detailed pit-stop events, tire info, lap numbers, |
| OpenF1 API | https://api.openf1.org | JSON (REST API) | Driver and team metadata (broadcast names, team info, etc.) OpenF1 API is public and doesn't require authentication |

The main Kaggle dataset includes:
- `races.csv` – race metadata (season, circuit, date)
- `results.csv` – finishing positions, points, grid positions
- `lap_times.csv` – every lap time for every driver
- `pit_stops.csv` – pit stop lap numbers and durations
- `drivers.csv` – driver names and codes
- `constructors.csv` – team names

I preprocessed everything for the 2022-2024 races only.

### API Integration
I also grabbed driver info from the OpenF1 API since it has cleaner team names and broadcast names, which helped match drivers across datasets:
```python
import requests
response = requests.get("https://api.openf1.org/v1/drivers?year=2023")
if response.status_code == 200:
    drivers_data = response.json()
    # extract team names and driver info
```

## Analysis

### Metrics Analyzed
1. Average Pit Stop Time – per team and per driver from 2022-2024
2. Lap Time Variance – standard deviation of lap times (consistency measure)
3. Grid-to-Finish Correlation – starting position vs finish position
4. Position Gains – positions gained or lost during the race
5. Correlation Heatmap – relationships between metrics

### Methods Used
- SQL queries to filter and join data (following concepts from class on Nov 4)
- API integration via `requests` library
- Pandas for data aggregation and metric calculation
- Standard deviation and correlation coefficients
- Matplotlib and seaborn for visualizations

### Visualizations
- Scatter plot: Qualifying vs Finishing Position
- Bar chart: Average Pit Stop Duration by Team
- Bar chart: Lap Time Variance by Driver
- Correlation heatmap
- Histogram: Position Changes Distribution

Example SQL used:
```sql
SELECT driver_id, AVG(pit_time_ms) 
FROM pit_stops 
WHERE year BETWEEN 2022 AND 2024 
GROUP BY driver_id;
```

## Summary of Results
The analysis results that pit stop times vary significantly between teams, with top teams averaging 22-23 seconds. Driver consistency (measured by lap variance) also differs across the grid. Starting grid position has a strong influence on final results, though about 30% of drivers gain or lose 3+ positions during races.

## How to Run

### Setup
1. Download the F1 dataset from the Kaggle link above
2. Extract the CSV files into a `data/` folder in the project root
3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Analysis
Option 1 - Run from command line:
```bash
python main.py
```

Option 2 - Run the Jupyter notebook (optional):
```bash
jupyter notebook results.ipynb
```

The code is organized into modules in the `src/` folder:
- `load_data.py` – loads CSVs and API data
- `data preprocessing.py` – calculates metrics and merges data
- `analysis.py` – creates all visualizations

main.py runs everything automatically in the correct order.

Results get saved to the `results/` folder and `f1_analysis.db` database.

### Notes
- OpenF1 API is public
- Data files are not in the repo - download them yourself
- If you get errors about missing files, check that all CSVs are in `data/` folder
