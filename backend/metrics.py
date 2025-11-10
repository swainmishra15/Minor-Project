import psutil
import os
import threading
import time
from prometheus_client import Gauge

# Define system metric gauges
cpu_metric = Gauge('system_cpu_percent', 'CPU usage percentage')
memory_metric = Gauge('system_memory_percent', 'Memory usage percentage')
disk_metric = Gauge('system_disk_percent', 'Disk usage percentage')

def update_system_metrics():
    """Continuously update system metrics every few seconds"""
    while True:
        try:
            # Collect system stats
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage('C:\\' if os.name == 'nt' else '/').percent

            # Update Prometheus metrics
            cpu_metric.set(cpu)
            memory_metric.set(mem)
            disk_metric.set(disk)

            # Debug print (optional)
            # print(f"Updated metrics: CPU={cpu}%, Mem={mem}%, Disk={disk}%")

        except Exception as metric_error:
            print(f"⚠️ Metrics update failed: {metric_error}")

        # Sleep for 5 seconds before updating again
        time.sleep(5)

def start_metrics_thread():
    """Start a background thread that continuously updates metrics"""
    thread = threading.Thread(target=update_system_metrics, daemon=True)
    thread.start()
    print("✅ System metrics background updater started.")

def setup_metrics():
    """Initialize metrics (kept for compatibility)"""
    start_metrics_thread()
