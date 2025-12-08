"""
Data cleaning and feature engineering for Formula 1 analysis
"""

import pandas as pd
import sqlite3
from pathlib import Path

YEARS = [2022, 2023, 2024]

def filter_by_years(data, years=YEARS):
    """Filter race data to specific years"""
    races = data["races"]
    races_filtered = races[races["year"].isin(years)]
    print(f"Filtered to {len(races_filtered)} races from {years}")
    return races_filtered

def calculate_positions_gained(results_df):
    """Calculate how many positions each driver gained/lost"""
    # grid position - final position (positive = gained positions)
    results_df["positions_gained"] = (
        results_df["grid"].fillna(0) - results_df["positionOrder"].fillna(0)
    )
    return results_df

def calculate_avg_pit_time(pit_stops_df):
    """Calculate average pit stop time per driver per race"""
    pit_avg = pit_stops_df.groupby(["raceId", "driverId"])["milliseconds"].mean()
    pit_avg = pit_avg.reset_index()
    pit_avg = pit_avg.rename(columns={"milliseconds": "avg_pit_ms"})
    return pit_avg

def calculate_lap_variance(lap_times_df):
    """
    Calculate lap time variance for each driver in each race
    Lower variance = more consistent
    """
    lap_var = lap_times_df.groupby(["raceId", "driverId"])["milliseconds"].var()
    lap_var = lap_var.reset_index()
    lap_var = lap_var.rename(columns={"milliseconds": "lap_var_ms"})
    return lap_var

def merge_all_data(data, years=YEARS):
    """
    Main preprocessing function that combines everything
    """
    # Get filtered races
    races_filtered = filter_by_years(data, years)
    races_subset = races_filtered[["raceId", "year", "name"]]
    
    # Merge results with race info
    results = data["results"]
    df = results.merge(races_subset, on="raceId")
    
    # Add positions gained
    df = calculate_positions_gained(df)
    
    # Add pit stop metrics
    pit_avg = calculate_avg_pit_time(data["pit_stops"])
    df = df.merge(pit_avg, on=["raceId", "driverId"], how="left")
    
    # Add lap time variance
    lap_var = calculate_lap_variance(data["lap_times"])
    df = df.merge(lap_var, on=["raceId", "driverId"], how="left")
    
    # Add driver names
    drivers = data["drivers"].copy()
    drivers["driver_name"] = drivers["forename"] + " " + drivers["surname"]
    df = df.merge(
        drivers[["driverId", "code", "driver_name"]], 
        on="driverId", 
        how="left"
    )
    
    # Add team names
    constructors = data["constructors"].copy()
    constructors = constructors.rename(columns={"name": "team_name"})
    df = df.merge(
        constructors[["constructorId", "team_name"]], 
        on="constructorId", 
        how="left"
    )
    
    print(f"✓ Final dataset: {len(df)} rows")
    return df

def save_to_sqlite(df, db_file="f1_analysis.db"):
    """
    Save data to SQLite database
    (following the SQL concepts from class)
    """
    conn = sqlite3.connect(db_file)
    df.to_sql("race_metrics", conn, if_exists="replace", index=False)
    
    # Test with a sample query
    test_query = """
    SELECT team_name, AVG(avg_pit_ms) as avg_pit_time
    FROM race_metrics
    WHERE avg_pit_ms IS NOT NULL
    GROUP BY team_name
    ORDER BY avg_pit_time
    LIMIT 5
    """
    
    result = pd.read_sql_query(test_query, conn)
    print("\nTop 5 fastest pit stop teams:")
    print(result)
    
    conn.close()
    print(f"✓ Data saved to {db_file}")
