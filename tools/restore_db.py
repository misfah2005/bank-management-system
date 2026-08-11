import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(loans)")

for column in cursor.fetchall():
    print(column)

# Create accounts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts(
    account_no INTEGER PRIMARY KEY,
    name TEXT,
    balance REAL,
    pin INTEGER
)
""")

# Create admins table
cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(
    username TEXT,
    password TEXT
)
""")

# Insert accounts
accounts = [
    (1001, "mohamed", 15000, 1234),
    (1002, "ali", 25500, 1111)
]

cursor.executemany(
    "INSERT INTO accounts VALUES(?,?,?,?)",
    accounts
)

# Insert admin
cursor.execute(
    "INSERT INTO admins VALUES(?,?)",
    ("admin", "admin123")
)

conn.commit()
conn.close()

print("Database restored successfully")