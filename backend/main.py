from fastapi import FastAPI
import sqlite3
from datetime import datetime
from ai_classifier import classify_log
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="Site Monitoring API")

class LogRequest(BaseModel):
    message: str
    source: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the site monitoring dashboard API!"}

@app.post("/logs/")
def create_log(log: LogRequest):
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
        "classification": classification
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
