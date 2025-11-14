# tests
import requests

def test_f1_api():
    url = "https://api.openf1.org/v1/drivers?session_key=9158"
    res = requests.get(url)
    assert res.status_code == 200
    print("API test successful! Retrieved driver data.")

if __name__ == "__main__":
    test_f1_api()
