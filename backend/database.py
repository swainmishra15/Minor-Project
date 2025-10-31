import sqlite3
import os

def init_database():
    """Initialize the SQLite database"""
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
        print("✅ Database created successfully!")

def get_db_connection():
    """Get a database connection"""
    return sqlite3.connect('site_monitoring.db')