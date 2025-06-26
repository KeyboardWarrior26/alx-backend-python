import requests

# Replace with your actual local server URL
BASE_URL = "http://127.0.0.1:8000"

# List of endpoints to hit
endpoints = [
    "/",  # You can replace this with your actual endpoints like "/conversations/"
    "/admin/",
    "/login/",
]

for endpoint in endpoints:
    try:
        url = BASE_URL + endpoint
        response = requests.get(url)
        print(f"GET {url} - Status: {response.status_code}")
    except Exception as e:
        print(f"Failed to GET {url}: {e}")
