import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

print("\n========== FIXED DEPOSITS ==========")

cursor.execute("""
SELECT
    fd_id,
    account_no,
    amount,
    years,
    interest_rate,
    maturity_amount,
    status
FROM fixed_deposits
""")

rows = cursor.fetchall()

if not rows:
    print("NO FIXED DEPOSIT RECORDS FOUND")
else:
    for row in rows:
        print(row)

print("\n========== ACCOUNT 1001 FD ==========")

cursor.execute("""
SELECT
    fd_id,
    account_no,
    amount,
    years,
    interest_rate,
    maturity_amount,
    status
FROM fixed_deposits
WHERE account_no = ?
""", (1001,))

rows = cursor.fetchall()

if not rows:
    print("NO FD FOR ACCOUNT 1001")
else:
    for row in rows:
        print(row)

conn.close()