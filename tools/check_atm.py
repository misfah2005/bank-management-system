import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()


# Check ATM table structure
cursor.execute("""
PRAGMA table_info(atm_cards)
""")

print("ATM TABLE COLUMNS:")

for row in cursor.fetchall():
    print(row)


print("\nATM CARD DETAILS:")


cursor.execute("""
SELECT 
account_no,
card_number,
pin,
status,
failed_attempts
FROM atm_cards
""")

rows = cursor.fetchall()

print("Total ATM Cards:", len(rows))


for row in rows:
    print(row)


conn.close()