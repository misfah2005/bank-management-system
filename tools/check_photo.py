import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute(
    "SELECT photo FROM accounts WHERE account_no=?",
    (1001,)
)

print(cursor.fetchone())

conn.close()