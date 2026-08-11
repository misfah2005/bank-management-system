import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()


print("=== TRANSACTIONS TABLE ===")

cursor.execute("""
PRAGMA table_info(transactions)
""")

for row in cursor.fetchall():
    print(row)



print("\n=== ATM CARDS ===")

cursor.execute("""
SELECT account_no, card_number, status, failed_attempts
FROM atm_cards
""")

for row in cursor.fetchall():
    print(row)



print("\n=== DATABASE CHECK ===")

cursor.execute("""
PRAGMA integrity_check;
""")

print(cursor.fetchone())


conn.close()