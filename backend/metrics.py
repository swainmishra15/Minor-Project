import psutil
import os
from prometheus_client import Gauge

# System metrics
cpu_metric = Gauge('system_cpu_percent', 'CPU usage percentage')
memory_metric = Gauge('system_memory_percent', 'Memory usage percentage')
disk_metric = Gauge('system_disk_percent', 'Disk usage percentage')

def setup_metrics():
    """Setup Prometheus metrics"""
    pass

def update_system_metrics():
    """Update system metrics for Prometheus"""
    try:
        cpu_metric.set(psutil.cpu_percent(interval=0.1))
        memory_metric.set(psutil.virtual_memory().percent)
        disk_metric.set(psutil.disk_usage('C:\\' if os.name == 'nt' else '/').percent)
    except Exception as metric_error:
        print(f"⚠️ Metrics update failed: {metric_error}")