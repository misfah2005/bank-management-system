import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()


# Approve ATM Card
cursor.execute("""
UPDATE atm_cards
SET status='Approved'
WHERE account_no=1001
""")

conn.commit()

print("ATM Card Approved Successfully")


# Check ATM Card Details
cursor.execute("""
SELECT account_no, card_number, pin, status
FROM atm_cards
WHERE account_no=1001
""")

row = cursor.fetchone()

print("ATM Details:")
print(row)


conn.close()