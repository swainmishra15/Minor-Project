import requests
import json
import time
import random
from datetime import datetime

# Your API endpoint
API_URL = "http://127.0.0.1:8000/logs/"

def send_single_log(message, source):
    """Send one log to your main.py API"""
    
    # Data to send
    log_data = {
        "message": message,
        "source": source
    }
    
    print(f"📤 Sending: {message}")
    print(f"   Source: {source}")
    
    try:
        # Send POST request to your main.py
        response = requests.post(API_URL, json=log_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS!")
            print(f"   Response: {result}")
            print("-" * 60)
            return True
        else:
            print(f"❌ FAILED: Status code {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def send_test_logs():
    """Send multiple test logs automatically"""
    
    print("🚀 STARTING LOG SENDER")
    print("=" * 60)
    
    # Test logs with different types
    test_logs = [
        ("Error: Database connection failed", "backend"),
        ("Warning: High memory usage detected", "system"),
        ("User login successful", "frontend"),
        ("Error: File not found in storage", "backend"),
        ("Warning: Disk space running low", "system"),
        ("API request completed successfully", "backend"),
        ("Random system event occurred", "monitoring"),
        ("Error: Authentication failed", "frontend")
    ]
    
    for i, (message, source) in enumerate(test_logs, 1):
        print(f"🔄 Log {i}/{len(test_logs)}")
        send_single_log(message, source)
        time.sleep(2)  # Wait 2 seconds between logs
    
    print("🎉 ALL LOGS SENT! Check your database now!")

def send_custom_logs():
    """Interactive mode - type your own logs"""
    
    print("🎯 CUSTOM LOG MODE")
    print("Type your logs manually. Type 'quit' to exit.")
    print("-" * 60)
    
    while True:
        print("\n📝 Enter new log:")
        message = input("Message: ")
        if message.lower() == 'quit':
            break
            
        source = input("Source: ")
        if source.lower() == 'quit':
            break
        
        send_single_log(message, source)

def send_realistic_logs():
    """Send realistic server logs"""
    
    realistic_logs = [
        ("Error: Connection timeout to database server", "database"),
        ("Warning: CPU usage at 87%", "system"),
        ("User johndoe logged in successfully", "auth"),
        ("Error: Failed to write to log file", "filesystem"),
        ("API endpoint /users responded in 1.2s", "api"),
        ("Warning: SSL certificate expires in 30 days", "security"),
        ("Backup completed successfully", "backup"),
        ("Error: Out of memory exception in worker process", "backend")
    ]
    
    print("🏢 SENDING REALISTIC SERVER LOGS")
    print("=" * 60)
    
    for message, source in realistic_logs:
        send_single_log(message, source)
        time.sleep(1)

if __name__ == "__main__":
    print("LOG SENDER SCRIPT")
    print("Choose an option:")
    print("1. Send sample test logs")
    print("2. Send realistic server logs") 
    print("3. Send custom logs (interactive)")
    print("4. Send single test log")
    
    choice = input("\nEnter choice (1-4): ")
    
    if choice == "1":
        send_test_logs()
    elif choice == "2":
        send_realistic_logs()
    elif choice == "3":
        send_custom_logs()
    elif choice == "4":
        send_single_log("Error: Test message from log sender", "test")
    else:
        print("Invalid choice!")
        
    print("\n💡 TIP: Check your database with:")
    print("   sqlite3 site_monitoring.db")
    print("   SELECT * FROM logs;")
