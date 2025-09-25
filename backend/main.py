from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
from datetime import datetime
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="Site Monitoring API")

# Add CORS middleware - THIS IS CRUCIAL!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create database if it doesn't exist
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

init_database()

def classify_log(log_message: str) -> str:
    """AI classifier for log importance"""
    if "error" in log_message.lower() or "failed" in log_message.lower():
        return "error"
    elif "warning" in log_message.lower():
        return "warning"
    elif "info" in log_message.lower() or "success" in log_message.lower():
        return "info"
    else:
        return "other"

class LogRequest(BaseModel):
    message: str
    source: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the site monitoring dashboard API!"}

@app.post("/logs/")
def create_log(log: LogRequest):
    """Create a new log entry with AI classification"""
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
        
        return {
            "id": log_id,
            "timestamp": timestamp,
            "message": log.message,
            "source": log.source,
            "classification": classification,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/logs/")
def get_logs():
    """Get all logs from database for displaying on website"""
    try:
        conn = sqlite3.connect('site_monitoring.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, message, source, classification 
            FROM logs 
            ORDER BY id DESC 
            LIMIT 20
        """)
        logs = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries for JSON response
        log_list = []
        for log in logs:
            log_list.append({
                "id": log[0],
                "timestamp": log[1],
                "message": log[2], 
                "source": log[3],
                "classification": log[4]
            })
        
        return {"logs": log_list, "count": len(log_list)}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
