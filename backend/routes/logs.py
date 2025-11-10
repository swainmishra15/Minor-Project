from fastapi import APIRouter, Request
from database import get_db_connection
from classifier import classify_log   # your Hugging Face classifier function
from datetime import datetime

router = APIRouter(prefix="/logs", tags=["Logs"])

# -------------------------------
# 🟢 POST /logs/ → Receive & Classify Logs
# -------------------------------
@router.post("/")
async def receive_log(request: Request):
    """
    Receive incoming logs, classify them with AI, and store in PostgreSQL.
    """
    try:
        # Get incoming JSON data
        data = await request.json()
        message = data.get("message")
        source = data.get("source", "unknown")

        if not message:
            return {"error": "Missing 'message' field in request"}

        # AI classification (Hugging Face model)
        classification = classify_log(message)

        # Store in PostgreSQL
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logs (timestamp, message, source, classification) VALUES (%s, %s, %s, %s)",
            (datetime.now(), message, source, classification)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return {
            "status": "success",
            "message": message,
            "source": source,
            "classification": classification
        }

    except Exception as e:
        print(f"❌ Error in /logs/: {e}")
        return {"error": str(e)}


# -------------------------------
# 🔵 GET /logs/ → Fetch Latest Logs
# -------------------------------
@router.get("/")
def get_logs():
    """
    Fetch the latest 50 logs from PostgreSQL.
    Useful for monitoring dashboards or API testing.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, message, source, classification
            FROM logs
            ORDER BY id DESC
            LIMIT 50;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        logs = [
            {
                "id": r[0],
                "timestamp": r[1],
                "message": r[2],
                "source": r[3],
                "classification": r[4]
            }
            for r in rows
        ]

        return {"logs": logs}

    except Exception as e:
        print(f"❌ Error in GET /logs/: {e}")
        return {"error": str(e)}


# -------------------------------
# 🟣 GET /logs/latest → Fetch Last 10 Logs
# -------------------------------
@router.get("/latest")
def get_latest_logs():
    """
    Fetch the 10 most recent logs for quick view.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, timestamp, message, source, classification
            FROM logs
            ORDER BY id DESC
            LIMIT 10;
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        logs = [
            {
                "id": r[0],
                "timestamp": r[1],
                "message": r[2],
                "source": r[3],
                "classification": r[4]
            }
            for r in rows
        ]

        return {"latest_logs": logs}

    except Exception as e:
        print(f"❌ Error in /logs/latest: {e}")
        return {"error": str(e)}
