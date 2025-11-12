from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

from database import init_database
from routes import logs, health, stats
from metrics import setup_metrics
app = FastAPI(title="Site Monitoring API")

# Initialize Prometheus
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

# Setup custom metrics
setup_metrics()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_database()

# Include routers
app.include_router(logs.router)
app.include_router(health.router)
app.include_router(stats.router)

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

if __name__ == "__main__":
    print("🚀 Starting TechCorp Monitoring API...")
    print("📊 Prometheus metrics available at: http://localhost:8000/metrics")
    print("📖 API documentation at: http://localhost:8000/docs")
    print("🔍 Health check at: http://localhost:8000/health/")
    uvicorn.run(app, host="0.0.0.0", port=8000)