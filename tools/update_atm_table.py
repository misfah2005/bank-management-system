import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

try:
    cursor.execute("""
    ALTER TABLE atm_cards
    ADD COLUMN failed_attempts INTEGER DEFAULT 0
    """)
    conn.commit()
    print("failed_attempts column added.")
except Exception:
    print("Column already exists.")

conn.close()