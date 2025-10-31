from fastapi import APIRouter

from database import get_db_connection

router = APIRouter()

@router.get("/stats/")
def get_stats():
    """Get statistics for dashboard"""
    try:
        conn = get_db_connection()
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