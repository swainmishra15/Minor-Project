from fastapi import APIRouter
from database import get_db_connection

router = APIRouter()

@router.get("/stats/")
def get_stats():
    """Return all statistics for dashboard charts"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Classification counts
        cursor.execute("""
            SELECT classification, COUNT(*) 
            FROM logs 
            GROUP BY classification
        """)
        classifications = dict(cursor.fetchall())

        # Logs per source
        cursor.execute("""
            SELECT source, COUNT(*) 
            FROM logs 
            GROUP BY source
            ORDER BY COUNT(*) DESC 
            LIMIT 10
        """)
        sources = dict(cursor.fetchall())

        # Trend (last few intervals)
        cursor.execute("""
            SELECT strftime('%H:%M', timestamp) AS time_label, COUNT(*) 
            FROM logs
            WHERE timestamp >= datetime('now', '-25 minutes')
            GROUP BY time_label
            ORDER BY time_label ASC
        """)
        trend_data = cursor.fetchall()
        log_labels = [row[0] for row in trend_data]
        log_trend = [row[1] for row in trend_data]

        conn.close()

        return {
            "log_labels": log_labels,
            "log_trend": log_trend,
            "log_classification": classifications,
            "log_per_source": sources,
            "total_logs": sum(classifications.values()) if classifications else 0,
            "status": "success"
        }

    except Exception as e:
        print(f"❌ Error generating stats: {e}")
        return {"error": str(e), "status": "failed"}
