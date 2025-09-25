import sqlite3

conn = sqlite3.connect('site_monitoring.db')
cursor = conn.cursor()

print("=== AVAILABLE TABLES ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
for table in tables:
    print(f"Table: {table[0]}")

conn.close()
