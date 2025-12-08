Load F1 data from Kaggle CSVs and OpenF1 API
"""

from pathlib import Path
import pandas as pd
import requests

DATA_DIR = Path("data")

def load_csv(filename):
    """Load a CSV file from the data folder"""
    filepath = DATA_DIR / filename
    try:
        df = pd.read_csv(filepath)
        print(f"✓ Loaded {filename}: {len(df)} rows")
        return df
    except FileNotFoundError:
        print(f"✗ Error: {filename} not found in data/ folder")
        return None

def load_all_kaggle_data():
    """Load all the F1 CSV files we need"""
    print("Loading Kaggle F1 data...")
    
    files = {
        "races": "races.csv",
        "results": "results.csv",
        "pit_stops": "pit_stops.csv",
        "lap_times": "lap_times.csv",
        "drivers": "drivers.csv",
        "constructors": "constructors.csv"
    }
    
    data = {}
    for key, filename in files.items():
        data[key] = load_csv(filename)
    
    return data

def fetch_openf1_drivers(year=2023):
    """
    Fetch driver info from OpenF1 API
    Returns DataFrame with driver metadata
    """
    url = f"https://api.openf1.org/v1/drivers?year={year}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            drivers_data = response.json()
            df = pd.DataFrame(drivers_data)
            print(f"✓ Fetched {len(df)} drivers from OpenF1 API")
            return df
        else:
            print(f"API request failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching API data: {e}")
        return None
