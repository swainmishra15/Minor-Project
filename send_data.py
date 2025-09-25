import requests
import datetime
import random
import time

BASE_URL = "http://127.0.0.1:8000"

def send_metric():
    """Sends a sample metric to the API."""
    timestamp = datetime.datetime.now().isoformat()
    # Simulate a random API response time
    value = random.uniform(50, 500)
    data = {
        "timestamp": timestamp,
        "name": "api_response_time",
        "value": value,
        "tags": {"endpoint": "/api/v1/data"}
    }
    try:
        response = requests.post(f"{BASE_URL}/metrics/", json=data)
        response.raise_for_status() # Raise an error for bad status codes
        print(f"Metric sent successfully. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send metric: {e}")

def send_log():
    """Sends a sample log entry to the API."""
    timestamp = datetime.datetime.now().isoformat()
    messages = [
        "User logged in successfully.",
        "An unexpected error occurred in the database connection.",
        "Warning: High memory usage detected.",
        "API request received and processed."
    ]
    data = {
        "timestamp": timestamp,
        "message": random.choice(messages),
        "source": "backend-service"
    }
    try:
        response = requests.post(f"{BASE_URL}/logs/", json=data)
        response.raise_for_status()
        print(f"Log sent successfully. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send log: {e}")

if __name__ == "__main__":
    while True:
        send_metric()
        send_log()
        # Wait for a few seconds before sending the next batch of data
        time.sleep(5)