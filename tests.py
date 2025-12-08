"""
Tests for the Formula 1 analysis functions
"""

import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).parent / "src"))

from load_data import load_csv
import importlib

# Import the preprocessing module
data_preprocessing = importlib.import_module('data preprocessing')
calculate_positions_gained = data_preprocessing.calculate_positions_gained
calculate_avg_pit_time = data_preprocessing.calculate_avg_pit_time
calculate_lap_variance = data_preprocessing.calculate_lap_variance


def test_load_csv():
    """Test loading CSV files"""
    print("\n[Test 1] Testing load_csv()...")
    try:
        df = load_csv("races.csv")
        assert df is not None, "races.csv didn't load"
        assert len(df) > 0, "races.csv is empty"
        assert "year" in df.columns, "missing year column"
        print("✓ CSV loading works")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


def test_positions_gained():
    """Test the positions gained calculation"""
    print("\n[Test 2] Testing calculate_positions_gained()...")
    try:
        # Make some test data
        test_df = pd.DataFrame({
            "grid": [1, 5, 10, 15],
            "positionOrder": [1, 3, 15, 12]
        })
        
        result = calculate_positions_gained(test_df)
        
        # Check if calculation is correct
        # Starting 1st, finishing 1st = 0 positions gained
        # Starting 5th, finishing 3rd = 2 positions gained
        # Starting 10th, finishing 15th = -5 (lost 5)
        # Starting 15th, finishing 12th = 3 positions gained
        expected = [0, 2, -5, 3]
        
        assert "positions_gained" in result.columns
        assert result["positions_gained"].tolist() == expected
        
        print("✓ Position calculation works")
        return True
    except AssertionError as e:
        print(f"✗ Failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_avg_pit_time():
    """Test pit stop average calculation"""
    print("\n[Test 3] Testing calculate_avg_pit_time()...")
    try:
        # Test data: driver 10 has 2 stops, driver 20 has 1
        test_df = pd.DataFrame({
            "raceId": [1, 1, 2],
            "driverId": [10, 10, 20],
            "milliseconds": [22000, 24000, 21000]
        })
        
        result = calculate_avg_pit_time(test_df)
        
        # Driver 10: avg of 22000 and 24000 should be 23000
        driver_10_avg = result[result["driverId"] == 10]["avg_pit_ms"].values[0]
        assert driver_10_avg == 23000
        
        # Driver 20: should be 21000
        driver_20_avg = result[result["driverId"] == 20]["avg_pit_ms"].values[0]
        assert driver_20_avg == 21000
        
        print("✓ Pit stop average works")
        return True
    except AssertionError as e:
        print(f"✗ Failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_lap_variance():
    """Test lap time variance calculation"""
    print("\n[Test 4] Testing calculate_lap_variance()...")
    try:
        # Test data with known variance
        test_df = pd.DataFrame({
            "raceId": [1, 1, 1, 2, 2],
            "driverId": [10, 10, 10, 20, 20],
            "milliseconds": [90000, 91000, 89000, 85000, 85000]
        })
        
        result = calculate_lap_variance(test_df)
        
        # Check structure
        assert "lap_var_ms" in result.columns
        assert len(result) == 2
        
        # Driver 10 should have some variance (different lap times)
        driver_10_var = result[result["driverId"] == 10]["lap_var_ms"].values[0]
        assert driver_10_var > 0
        
        # Driver 20 should have zero variance (same lap times)
        driver_20_var = result[result["driverId"] == 20]["lap_var_ms"].values[0]
        assert driver_20_var == 0
        
        print("✓ Lap variance calculation works")
        return True
    except AssertionError as e:
        print(f"✗ Failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_api_connection():
    """Test that the OpenF1 API is working"""
    print("\n[Test 5] Testing OpenF1 API connection...")
    try:
        import requests
        url = "https://api.openf1.org/v1/drivers"
        response = requests.get(url)
        assert response.status_code == 200
        print("✓ API connection works")
        return True
    except Exception as e:
        print(f"✗ API test failed: {e}")
        return False


def run_all_tests():
    """Run all tests and show results"""
    print("\n" + "="*60)
    print("Running Tests")
    print("="*60)
    
    tests = [
        test_load_csv,
        test_positions_gained,
        test_avg_pit_time,
        test_lap_variance,
        test_api_connection
    ]
    
    results = []
    for test in tests:
        try:
            passed = test()
            results.append(passed)
        except Exception as e:
            print(f"\n✗ Unexpected error in {test.__name__}: {e}")
            results.append(False)
    
    # Summary
    print("\n" + "="*60)
    print("Results")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed!")
        print("="*60 + "\n")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        print("="*60 + "\n")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
