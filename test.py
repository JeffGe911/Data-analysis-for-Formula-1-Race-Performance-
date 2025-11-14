# tests
import requests

url = "https://api.openf1.org/v1/drivers?session_key=9158"
response = requests.get(url)

if response.status_code == 200:
    print("API works!")
    print(response.json()[:3])
else:
    print("API request failed")




