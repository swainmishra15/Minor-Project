from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
from datetime import datetime
import uvicorn
from pydantic import BaseModel

# Prometheus imports
from prometheus_fastapi_instrumentator import Instrumentator
import psutil
from prometheus_client import Gauge

app = FastAPI(title="Site Monitoring API")

# Initialize Prometheus
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# System metrics
cpu_metric = Gauge('system_cpu_percent', 'CPU usage percentage')
memory_metric = Gauge('system_memory_percent', 'Memory usage percentage')
disk_metric = Gauge('system_disk_percent', 'Disk usage percentage')

# CORS middleware (FastAPI way)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
def init_database():
    if not os.path.exists('site_monitoring.db'):
        conn = sqlite3.connect('site_monitoring.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            message TEXT NOT NULL,
            source TEXT NOT NULL,
            classification TEXT
        );''')
        conn.commit()
        conn.close()
        print("✅ Database created successfully!")

init_database()

# AI classifier
def classify_log(log_message: str) -> str:
    """Enhanced AI classifier with more comprehensive rules"""
    message_lower = log_message.lower()
    
    # Critical/Error patterns
    error_keywords = [
        'error', 'failed', 'failure', 'exception', 'crash', 'critical', 'fatal', 
        'panic', 'abort', 'timeout', 'refused', 'denied', 'forbidden', 'unauthorized',
        'not found', '404', '500', '503', 'internal server error', 'database error',
        'connection failed', 'out of memory', 'disk full', 'permission denied',
        'authentication failed', 'ssl error', 'certificate error', 'syntax error'
    ]
    
    # Warning patterns  
    warning_keywords = [
        'warning', 'warn', 'deprecated', 'slow', 'retry', 'fallback', 'backup',
        'high usage', 'low disk', 'memory usage', 'cpu usage', 'performance',
        'certificate expires', 'ssl expires', 'quota exceeded', 'rate limit',
        'unusual activity', 'suspicious', 'outdated', 'upgrade required',
        'maintenance', 'restart required', 'configuration change'
    ]
    
    # Success/Info patterns
    success_keywords = [
        'success', 'successful', 'completed', 'finished', 'done', 'ok', 'ready',
        'started', 'initialized', 'connected', 'authenticated', 'authorized',
        'login', 'logout', 'registered', 'created', 'updated', 'saved',
        'backup completed', 'sync completed', 'deployment successful',
        'healthy', 'online', 'available', 'operational'
    ]
    
    # Security patterns
    security_keywords = [
        'security', 'breach', 'attack', 'intrusion', 'malware', 'virus',
        'phishing', 'suspicious login', 'multiple failed logins', 'brute force',
        'ddos', 'injection', 'xss', 'csrf', 'vulnerability', 'exploit'
    ]
    
    # Performance patterns
    performance_keywords = [
        'slow query', 'high latency', 'response time', 'throughput', 'load balancer',
        'scaling', 'auto-scale', 'performance degradation', 'optimization',
        'cache hit', 'cache miss', 'memory leak', 'cpu spike'
    ]
    
    # Check patterns in priority order
    if any(keyword in message_lower for keyword in security_keywords):
        return "security"
    elif any(keyword in message_lower for keyword in error_keywords):
        return "error"
    elif any(keyword in message_lower for keyword in warning_keywords):
        return "warning"
    elif any(keyword in message_lower for keyword in performance_keywords):
        return "performance"
    elif any(keyword in message_lower for keyword in success_keywords):
        return "info"
    else:
        return "other"

# Pydantic models
class LogRequest(BaseModel):
    message: str
    source: str

# API Routes
@app.get("/")
def read_root():
    return {
        "message": "🚀 TechCorp Monitoring API is running!",
        "status": "active",
        "endpoints": {
            "logs": "/logs/",
            "metrics": "/metrics",
            "docs": "/docs"
        }
    }

@app.post("/logs/")
def create_log(log: LogRequest):
    """Create a new log entry with AI classification + Prometheus metrics"""
    try:
        conn = sqlite3.connect('site_monitoring.db')
        cursor = conn.cursor()
        
        classification = classify_log(log.message)
        timestamp = datetime.now().isoformat()
        
        cursor.execute(
            "INSERT INTO logs (timestamp, message, source, classification) VALUES (?, ?, ?, ?)",
            (timestamp, log.message, log.source, classification)
        )
        
        conn.commit()
        log_id = cursor.lastrowid
        conn.close()
        
        # Update system metrics
        try:
            cpu_metric.set(psutil.cpu_percent(interval=0.1))
            memory_metric.set(psutil.virtual_memory().percent)
            disk_metric.set(psutil.disk_usage('C:\\' if os.name == 'nt' else '/').percent)
        except Exception as metric_error:
            print(f"⚠️ Metrics update failed: {metric_error}")
        
        print(f"✅ Log created: {classification} - {log.message[:50]}...")
        
        return {
            "id": log_id,
            "timestamp": timestamp,
            "message": log.message,
            "source": log.source,
            "classification": classification,
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ Error creating log: {e}")
        return {"error": str(e), "status": "failed"}

@app.get("/logs/")
def get_logs():
    """Get all logs from database"""
    try:
        conn = sqlite3.connect('site_monitoring.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, message, source, classification
            FROM logs
            ORDER BY id DESC
            LIMIT 50
        """)
        logs = cursor.fetchall()
        conn.close()

        log_list = []
        for log in logs:
            log_list.append({
                "id": log[0],
                "timestamp": log[1],
                "message": log[2],
                "source": log[3],
                "classification": log[4]
            })

        return {
            "logs": log_list, 
            "count": len(log_list),
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ Error getting logs: {e}")
        return {"error": str(e), "status": "failed"}

@app.get("/stats/")
def get_stats():
    """Get statistics for dashboard"""
    try:
        conn = sqlite3.connect('site_monitoring.db')
        cursor = conn.cursor()
        
        # Get classification counts
        cursor.execute("""
            SELECT classification, COUNT(*) as count
            FROM logs 
            GROUP BY classification
        """)
        classifications = dict(cursor.fetchall())
        
        # Get source counts
        cursor.execute("""
            SELECT source, COUNT(*) as count
            FROM logs 
            GROUP BY source
            ORDER BY count DESC
            LIMIT 10
        """)
        sources = dict(cursor.fetchall())
        
        # Get recent activity
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM logs 
            WHERE datetime(timestamp) >= datetime('now', '-1 hour')
        """)
        recent_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "classifications": classifications,
            "sources": sources,
            "total_logs": sum(classifications.values()),
            "recent_hour": recent_count,
            "status": "success"
        }
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return {"error": str(e), "status": "failed"}

@app.get("/health/")
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        conn = sqlite3.connect('site_monitoring.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM logs")
        log_count = cursor.fetchone()[0]
        conn.close()
        
        # Get system info
        system_info = {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('C:\\' if os.name == 'nt' else '/').percent
        }
        
        return {
            "status": "healthy",
            "database": "connected",
            "total_logs": log_count,
            "system": system_info
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    print("🚀 Starting TechCorp Monitoring API...")
    print("📊 Prometheus metrics available at: http://localhost:8000/metrics")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("🔍 Health check at: http://localhost:8000/health/")
    uvicorn.run(app, host="0.0.0.0", port=8000)
