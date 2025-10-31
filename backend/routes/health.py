from fastapi import APIRouter
import psutil
import os

from database import get_db_connection

router = APIRouter()

@router.get("/health/")
def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        conn = get_db_connection()
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