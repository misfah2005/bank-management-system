import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE atm_cards
SET status='Approved',
    failed_attempts=0
WHERE account_no=1001
""")

conn.commit()
conn.close()

print("ATM Card Unblocked Successfully")