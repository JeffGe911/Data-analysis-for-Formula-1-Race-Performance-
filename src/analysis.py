"""
Analysis and visualization part for Formula 1 race Project
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)


def plot_grid_vs_finish(df):
    """
    Scatter plot: starting grid position vs finishing position
    Shows if qualifying position predicts race result
    """
    # Only look at drivers who finished (positionOrder > 0)
    df_finished = df[df["positionOrder"] > 0].copy()
    
    plt.figure(figsize=(10, 8))
    plt.scatter(
        df_finished["grid"], 
        df_finished["positionOrder"],
        alpha=0.4,
        s=50,
        color='steelblue'
    )
    
    # Add diagonal reference line (perfect correlation)
    max_pos = max(df_finished["grid"].max(), df_finished["positionOrder"].max())
    plt.plot([0, max_pos], [0, max_pos], 'r--', alpha=0.5, label="Perfect correlation")
    
    plt.xlabel("Starting Grid Position", fontsize=12)
    plt.ylabel("Finishing Position", fontsize=12)
    plt.title("Qualifying vs Finishing Position (2022-2024)", fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = RESULTS_DIR / "grid_vs_finish.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_pit_stops_by_team(df):
    """
    Bar chart of average pit stop times by team
    Lower is better (faster pit crew)
    """
    # Calculate average pit time per team
    team_pit = df.groupby("team_name")["avg_pit_ms"].mean().sort_values()
    
    # Remove NaN values
    team_pit = team_pit.dropna()
    
    plt.figure(figsize=(12, 6))
    team_pit.plot(kind="bar", color="slateblue")
    plt.title("Average Pit Stop Duration by Team (2022-2024)", fontsize=14, fontweight='bold')
    plt.xlabel("Team", fontsize=12)
    plt.ylabel("Avg Pit Stop Time (ms)", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    output_path = RESULTS_DIR / "pit_stops_by_team.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_lap_variance_by_driver(df, min_races=10, top_n=20):
    """
    Bar chart showing lap time consistency for drivers
    Lower variance = more consistent driver
    """
    # Filter drivers with enough data
    driver_race_counts = df.groupby("driver_name").size()
    valid_drivers = driver_race_counts[driver_race_counts >= min_races].index
    
    df_filtered = df[df["driver_name"].isin(valid_drivers)]
    
    # Calculate average lap variance per driver
    lap_var = df_filtered.groupby("driver_name")["lap_var_ms"].mean().sort_values()
    lap_var = lap_var.dropna().head(top_n)
    
    plt.figure(figsize=(12, 8))
    lap_var.plot(kind="barh", color="orange")
    plt.title(f"Lap Time Variance by Driver (Top {top_n}, Lower = More Consistent)", 
              fontsize=14, fontweight='bold')
    plt.xlabel("Lap Time Variance (ms²)", fontsize=12)
    plt.ylabel("Driver", fontsize=12)
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    
    output_path = RESULTS_DIR / "lap_variance_by_driver.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_correlation_heatmap(df):
    """
    Correlation heatmap of performance metrics
    Shows relationships between different race factors
    """
    # Select numeric columns for correlation
    metric_cols = ["grid", "positionOrder", "positions_gained", "avg_pit_ms", "lap_var_ms"]
    
    df_corr = df[metric_cols].dropna()
    corr_matrix = df_corr.corr()
    
    # Rename columns for better readability
    labels = {
        "grid": "Grid Position",
        "positionOrder": "Finish Position", 
        "positions_gained": "Positions Gained",
        "avg_pit_ms": "Avg Pit Time",
        "lap_var_ms": "Lap Variance"
    }
    corr_matrix = corr_matrix.rename(columns=labels, index=labels)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix, 
        annot=True, 
        cmap="coolwarm", 
        center=0,
        fmt=".2f",
        square=True, 
        linewidths=1,
        cbar_kws={"shrink": 0.8}
    )
    plt.title("Correlation Between Performance Metrics (2022-2024)", 
              fontsize=14, fontweight='bold', pad=20)
    
    # Rotate labels to be horizontal
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    
    plt.tight_layout()
    
    output_path = RESULTS_DIR / "correlation_heatmap.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path}")
    plt.close()


def plot_positions_gained_distribution(df):
    """
    Histogram showing distribution of positions gained/lost
    Positive = gained positions, Negative = lost positions
    """
    df_finished = df[df["positionOrder"] > 0].copy()
    
    plt.figure(figsize=(10, 6))
    plt.hist(df_finished["positions_gained"], bins=30, color="teal", alpha=0.7, edgecolor='black')
    plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='No change')
    plt.xlabel("Positions Gained/Lost", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.title("Distribution of Position Changes During Race (2022-2024)", 
              fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    output_path = RESULTS_DIR / "positions_gained_distribution.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"✓ Saved: {output_path}")
    plt.close()


def generate_summary_stats(df):
    """
    Generate and print summary statistics
    Returns a dict with key metrics
    """
    stats = {}
    
    # Basic counts
    stats["total_races"] = df["raceId"].nunique()
    stats["total_drivers"] = df["driverId"].nunique()
    stats["total_teams"] = df["team_name"].nunique()
    
    # Average pit stop time
    stats["avg_pit_time"] = df["avg_pit_ms"].mean()
    
    # Team with fastest average pit stops
    team_pit = df.groupby("team_name")["avg_pit_ms"].mean().sort_values()
    if len(team_pit) > 0:
        stats["fastest_pit_team"] = team_pit.index[0]
        stats["fastest_pit_time"] = team_pit.iloc[0]
    
    # Most consistent driver (lowest lap variance)
    driver_counts = df.groupby("driver_name").size()
    valid_drivers = driver_counts[driver_counts >= 10].index
    df_valid = df[df["driver_name"].isin(valid_drivers)]
    
    driver_var = df_valid.groupby("driver_name")["lap_var_ms"].mean().sort_values()
    if len(driver_var) > 0:
        stats["most_consistent_driver"] = driver_var.index[0]
        stats["lowest_variance"] = driver_var.iloc[0]
    
    print("\n" + "="*50)
    print("SUMMARY STATISTICS (2022-2024)")
    print("="*50)
    print(f"Total Races Analyzed: {stats['total_races']}")
    print(f"Total Drivers: {stats['total_drivers']}")
    print(f"Total Teams: {stats['total_teams']}")
    print(f"\nAverage Pit Stop Time: {stats['avg_pit_time']:.0f} ms")
    
    if "fastest_pit_team" in stats:
        print(f"Fastest Pit Team: {stats['fastest_pit_team']} ({stats['fastest_pit_time']:.0f} ms)")
    
    if "most_consistent_driver" in stats:
        print(f"Most Consistent Driver: {stats['most_consistent_driver']}")
    
    print("="*50 + "\n")
    
    return stats


def generate_all_plots(df):
    """
    Generate all visualizations and summary statistics
    This is the main function to call from notebooks or main.py
    """
    print("\n" + "="*50)
    print("GENERATING VISUALIZATIONS")
    print("="*50 + "\n")
    
    # Generate plots
    plot_grid_vs_finish(df)
    plot_pit_stops_by_team(df)
    plot_lap_variance_by_driver(df)
    plot_correlation_heatmap(df)
    plot_positions_gained_distribution(df)
    
    # Generate summary stats
    stats = generate_summary_stats(df)
    
    print("✓ All visualizations generated successfully!")
    print(f"✓ Check the '{RESULTS_DIR}/' folder for output files\n")
    
    return stats


if __name__ == "__main__":
    # For testing - load data and generate plots
    import sys
    sys.path.append('..')
    from src.load_data import load_all_kaggle_data
    from src.preprocessing import merge_all_data
    
    print("Loading data for testing...")
    data = load_all_kaggle_data()
    df_clean = merge_all_data(data)
    
    print("\nGenerating plots...")
    generate_all_plots(df_clean)
