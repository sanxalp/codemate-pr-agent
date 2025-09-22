import requests
import json

# Test the backend directly
backend_url = "http://127.0.0.1:8000/analyze"

# Test data - using a real GitHub PR URL for testing
test_data = {
    "prUrl": "https://github.com/microsoft/vscode/pull/123456"
}

try:
    response = requests.post(backend_url, json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error connecting to backend: {e}")