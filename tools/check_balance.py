import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

account_no = 1001

# ==========================
# CHECK ACCOUNT BALANCE
# ==========================

cursor.execute("""
SELECT account_no, name, balance
FROM accounts
WHERE account_no = ?
""", (account_no,))

row = cursor.fetchone()

print("================================")
print("ACCOUNT DETAILS")
print("================================")

if row:
    print("Account No :", row[0])
    print("Name       :", row[1])
    print("Balance    : Rs.", row[2])
else:
    print("Account 1001 Not Found")


# ==========================
# CHECK LOANS
# ==========================

cursor.execute("""
SELECT loan_id, loan_type, amount, emi, months, status
FROM loans
WHERE account_no = ?
""", (account_no,))

loans = cursor.fetchall()

print("\n================================")
print("LOANS")
print("================================")

if loans:
    for loan in loans:
        print(
            "Loan ID :", loan[0],
            "| Type :", loan[1],
            "| Amount :", loan[2],
            "| EMI :", loan[3],
            "| Months :", loan[4],
            "| Status :", loan[5]
        )
else:
    print("No loans found")


# ==========================
# CLOSE DATABASE
# ==========================

conn.close()