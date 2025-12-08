"""
Main script to run the complete my Formula 1 analysis pipeline
Usage: python main.py
"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.append(str(Path(__file__).parent / "src"))
import importlib
data_preprocessing = importlib.import_module('data preprocessing')
from load_data import load_all_kaggle_data, fetch_openf1_drivers
from analysis import generate_all_plots

merge_all_data = data_preprocessing.merge_all_data
save_to_sqlite = data_preprocessing.save_to_sqlite


def main():
    """
    Run the full F1 analysis pipeline:
    1. Load data from CSVs and API
    2. Clean and merge data
    3. Save to SQLite database
    4. Generate visualizations and statistics
    """
    print("\n" + "="*60)
    print("F1 Pit Stop and Lap Time Analysis (2022-2024)")
    print("="*60)
    
    # Step 1: Load data
    print("\n[Step 1/4] Loading data from CSV files...")
    data = load_all_kaggle_data()
    
    # Check if data loaded successfully
    if any(df is None for df in data.values()):
        print("\n✗ Error: Failed to load some data files")
        print("Make sure all CSV files are in the data/ folder")
        sys.exit(1)
    
    # Optional: get additional driver info from API
    print("\n[Step 1b] Fetching driver info from OpenF1 API...")
    api_drivers = fetch_openf1_drivers(year=2023)
    if api_drivers is not None:
        print(f"✓ Retrieved info for {len(api_drivers)} drivers")
    
    # Step 2: Clean and merge data
    print("\n[Step 2/4] Preprocessing and merging data...")
    try:
        df_clean = merge_all_data(data)
    except Exception as e:
        print(f"\n✗ Error during preprocessing: {e}")
        sys.exit(1)
    
    # Step 3: Save to database
    print("\n[Step 3/4] Saving data to SQLite database...")
    try:
        save_to_sqlite(df_clean)
    except Exception as e:
        print(f"\n✗ Error saving to database: {e}")
    
    # Step 4: Generate visualizations
    print("\n[Step 4/4] Creating visualizations...")
    try:
        stats = generate_all_plots(df_clean)
    except Exception as e:
        print(f"\n✗ Error generating plots: {e}")
        sys.exit(1)
    
    # Done!
    print("\n" + "="*60)
    print("✓ Analysis complete!")
    print("="*60)
    print("\nOutput files:")
    print("  - results/ folder contains all visualizations")
    print("  - f1_analysis.db contains the processed data")
    print("\nYou can also run the analysis in results.ipynb")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nAnalysis interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
