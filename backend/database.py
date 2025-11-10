import psycopg2
from psycopg2 import sql

# PostgreSQL connection details
DB_NAME = "site_monitoring"
DB_USER = "postgres"          # change if you use a different username
DB_PASSWORD = "uday@123"  # use your actual pgAdmin password
DB_HOST = "localhost"
DB_PORT = "5432"

def init_database():
    """Initialize PostgreSQL database and ensure logs table exists"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        # Create logs table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                message TEXT NOT NULL,
                source TEXT NOT NULL,
                classification TEXT
            );
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ PostgreSQL connected and logs table verified!")

    except Exception as e:
        print(f"❌ Database initialization error: {e}")

def get_db_connection():
    """Return a new PostgreSQL database connection"""
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
