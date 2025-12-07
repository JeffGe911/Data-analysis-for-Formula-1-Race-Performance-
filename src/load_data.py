import pandas as pd
import requests

def load_kaggle_data(filepath):
    """Load and return local Kaggle CSV data."""
    df = pd.read_csv(filepath)
    return df

def load_openf1_api(endpoint="drivers"):
    """Webscrap OpenF1 API data."""
    url = f"https://api.openf1.org/v1/{endpoint}"
    response = requests.get(url)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        raise Exception("API fetch failed.")

def clean_data(df):
    """Example cleaning: drop nulls, parse types."""
    df = df.dropna()
    # add more cleaning steps as needed
    return df
