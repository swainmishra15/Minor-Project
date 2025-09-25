from fastapi import FastAPI
from .db import engine, Base, SessionLocal
from .models import Log, Metric
from .ai_classifier import classify_log
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the site monitoring dashboard API!"}

# Create database tables
Base.metadata.create_all(bind=engine)

@app.post("/metrics/")
def create_metric(timestamp: str, name: str, value: float, tags: dict = None):
    # This is a simplified example. In a real app, you would
    # validate data and save to the database.
    return {"status": "success", "metric": {"name": name, "value": value}}

@app.post("/logs/")
def create_log(timestamp: str, message: str, source: str):
    log_class = classify_log(message)
    # Save log to DB with its classification
    return {"status": "success", "log": {"message": message, "class": log_class}}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)