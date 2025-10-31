from fastapi import APIRouter
from datetime import datetime

from database import get_db_connection
from models import LogRequest
from classifier import classify_log
from metrics import update_system_metrics

router = APIRouter()

@router.post("/logs/")
def create_log(log: LogRequest):
    """Create a new log entry with AI classification + Prometheus metrics"""
    try:
        conn = get_db_connection()
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
        update_system_metrics()
        
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

@router.get("/logs/")
def get_logs():
    """Get all logs from database"""
    try:
        conn = get_db_connection()
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