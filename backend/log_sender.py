import requests
import time
import random
from transformers import pipeline

# 🔗 FastAPI endpoint (adjust port if needed)
API_URL = "http://127.0.0.1:8000/logs/"

# Load the same Hugging Face model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
labels = ["error", "warning", "info", "performance", "security", "other"]

# Sample raw logs (without explicit labels)
RAW_LOGS = [
    "Database connection failed due to timeout",
    "Disk space full on server node-1",
    "Failed to write data to PostgreSQL database",
    "Out of memory exception in process scheduler",
    "High CPU utilization detected in backend worker",
    "Memory usage exceeds 85% on node-3",
    "SSL certificate expires in 3 days",
    "Disk space running low on /var partition",
    "User login completed successfully",
    "Server started and ready to accept requests",
    "Backup operation finished successfully",
    "API endpoint /health returned 200 OK",
    "Slow response from database during query execution",
    "API latency increased to 2.5 seconds",
    "Load balancer redistributed requests evenly",
    "Optimized caching mechanism activated",
    "Unauthorized access attempt detected from IP 192.168.1.10",
    "Multiple failed login attempts detected for user admin",
    "Firewall rule updated successfully",
    "SSL certificate renewed successfully"
]


def send_single_log(message, source="system"):
    """Send one raw log entry to the backend"""
    try:
        response = requests.post(API_URL, json={"message": message, "source": source})
        if response.status_code == 200:
            print(f"✅ Sent log → {message}")
        else:
            print(f"⚠️ Failed ({response.status_code}) → {response.text[:60]}")
    except Exception as e:
        print(f"❌ Error sending log: {e}")

def generate_and_send_logs():
    """Generate logs using the classifier to mix semantics but send only raw text"""
    print("\n🚀 Smart Log Sender Started...\n")

    for _ in range(10):  # send 10 logs for test
        # Pick a random base log
        log_message = random.choice(RAW_LOGS)

        # Use classifier just to vary internal processing (simulate contextual load)
        _ = classifier(log_message, labels)

        # Send the original message (no label prefixes)
        send_single_log(log_message)

        time.sleep(1)  # small delay between sends

    print("\n🎯 All smart logs sent! Check your dashboard for AI classification results.\n")

if __name__ == "__main__":
    generate_and_send_logs()
