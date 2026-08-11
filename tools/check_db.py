import sqlite3

conn = sqlite3.connect("bank_backup.db")
cursor = conn.cursor()

cursor.execute("""
PRAGMA integrity_check;
""")

print(cursor.fetchone())

conn.close()