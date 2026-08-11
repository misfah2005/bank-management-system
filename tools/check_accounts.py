import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(accounts)")

for row in cursor.fetchall():
    print(row)

conn.close()