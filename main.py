import sqlite3
import shutil
from datetime import datetime
    

accounts = []

current_user = None



# ---------------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------------
connection = sqlite3.connect("bank.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    balance REAL NOT NULL,
    pin TEXT NOT NULL
)
""")
connection.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no INTEGER,
    transaction_type TEXT,
    amount REAL,
    date_time TEXT
)
""")
connection.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admins (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
""")
connection.commit()

cursor.execute("""
SELECT * FROM admins
WHERE username = ?
""", ("admin",))
admin = cursor.fetchone()

if admin is None:
    cursor.execute("""
    INSERT INTO admins
    VALUES (?, ?)
    """, ("admin", "admin123"))
    connection.commit()

# Load accounts from SQLite Database




cursor.execute("""
SELECT account_no, name, balance, pin
FROM accounts
""")
rows = cursor.fetchall()

accounts.clear()

for row in rows:
    account = {
        "account_no": row[0],
        "name": row[1],
        "balance": row[2],
        "pin": row[3]
    }
    accounts.append(account)

print("Accounts Loaded From SQLite :", len(accounts))
 


def add_admin_log(action):
    """Log admin actions."""
    current_time = datetime.now()
    date_time = current_time.strftime("%d-%m-%Y %I:%M:%S %p")
    cursor.execute("""
    INSERT INTO transactions
    (account_no, transaction_type, amount, date_time)
    VALUES (?, ?, ?, ?)
    """, (0, "Admin: " + action, 0, date_time))
    connection.commit()


def admin_logout():
    print("\nAdmin Logged out Successfully")

def admin_login():

    username = input("Enter Admin Username: ")
    password = input("Enter Admin Password: ")

    cursor.execute("""
    SELECT *
    FROM admins
    WHERE username = ? AND password = ?
    """, (username, password))

    admin = cursor.fetchone()

    if admin:
        add_admin_log("Admin Login")
        print("\nAdmin Login Successful")
        return True

    print("Invalid Username or Password")
    return False    


def admin_dashboard():
    print("\n========= ADMIN DASHBOARD ============")
    print("Total Accounts        :", len(accounts))
    total_balance = sum(account["balance"] for account in accounts)
    print("Total Bank Balance  : Rs.", total_balance)
    print("==================================")


def admin_total_bank_balance():
    """Print total bank balance."""
    total_balance = sum(account["balance"] for account in accounts)
    print("\nTotal Bank Balance  : Rs.", total_balance)

def admin_total_accounts():

    print("\n========= TOTAL ACCOUNTS =========")

    cursor.execute("""
    SELECT COUNT(*)
    FROM accounts
    """)

    total = cursor.fetchone()[0]

    print("Total Accounts :", total)


def admin_view_all_accounts():

    print("\n========== ALL ACCOUNTS ==========")

    cursor.execute("""
    SELECT account_no, name, balance
    FROM accounts
    ORDER BY account_no
    """)

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No Accounts Found")
        return
    
    else:
        print("-" * 50)

    for row in rows:
        print("Account No :", row[0])
        print("Name       :", row[1])
        print("Balance    : Rs.", row[2])
        print("-" * 50)
                                               

def admin_search_account():

    print("\n========= SEARCH ACCOUNT =========")

    try:
        account_no = int(input("Enter Account Number: "))
    except ValueError:
        print("Invalid Account Number")
        return

    cursor.execute("""
    SELECT account_no, name, balance,pin
    FROM accounts
    WHERE account_no = ?
    """, (account_no,))

    row = cursor.fetchone()

    if row is None:
        print("Account Not Found")
    else:
        print("\n========= ACCOUNT DETAILS =========")
        print("Account Number :", row[0])
        print("Account Holder :", row[1])
        print("Balance        : Rs.", row[2])
        print("PIN            :", row[3])

def admin_view_all_transactions():

    print("\n====== ALL TRANSACTIONS ======")

    cursor.execute("""
    SELECT account_no, transaction_type, amount, date_time
    FROM transactions
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No Transactions Found")
        return

    print("-" * 50)

    for row in rows:
        print("Account No :", row[0])
        print("Type       :", row[1])
        print("Amount     : Rs.", row[2])
        print("Date & Time:", row[3])
        print("-" * 50)

    print("-------------------------------------------")


def admin_delete_any_account():

    print("\n========= DELETE ACCOUNT =========")

    try:
        account_no = int(input("Enter Account Number to Delete: "))
    except ValueError:
        print("Invalid Account Number")
        return

    cursor.execute("""
    SELECT *
    FROM accounts
    WHERE account_no = ?
    """, (account_no,))

    row = cursor.fetchone()

    if row is None:
        print("Account Not Found")
        return

    confirm = input("Are you sure? (Y/N): ").strip().lower()

    if confirm != "y":
        print("Deletion Cancelled")
        return

    cursor.execute("""
    DELETE FROM accounts
    WHERE account_no = ?
    """, (account_no,))

    connection.commit()

    for account in accounts:
        if account["account_no"] == account_no:
            accounts.remove(account)
            break

    save_transactions(
        account_no,
        "Account Deleted Successfully",
        0
    )

    print("Account Deleted Successfully")

    
        

def admin_total_bank_balance():

    print("\n========= TOTAL BANK BALANCE =========")

    cursor.execute("""
    SELECT SUM(balance)
    FROM accounts
    """)

    total = cursor.fetchone()[0]

    if total is None:
        total = 0

    print("Total Bank Balance : Rs.", total)

def interest_calculator():

    print("\n========= INTEREST CALCULATOR =========")

    try:
        account_no = int(input("Enter Account Number: "))
    except ValueError:
        print("Invalid Account Number")
        return

    found = False

    for account in accounts:

        if account["account_no"] == account_no:

            found = True

            balance = account["balance"]

            print("Current Balance : Rs.", balance)

            try:
                rate = float(input("Enter Interest Rate (%) : "))
                years = float(input("Enter Number of Years : "))
            except ValueError:
                print("Invalid Input")
                return

            interest = (balance * rate * years) / 100
            final_amount = balance + interest

            print("\nInterest Earned : Rs.", interest)
            print("Final Amount    : Rs.", final_amount)

            break

    if not found:
        print("Account Not Found") 


def loan_calculator():

    print("\n========= LOAN CALCULATOR =========")

    try:
        loan_amount = float(input("Enter Loan Amount : Rs. "))
        annual_rate = float(input("Enter Annual Interest Rate (%) : "))
        years = int(input("Enter Loan Period (Years) : "))
    except ValueError:
        print("Invalid Input")
        return

    total_interest = (loan_amount * annual_rate * years) / 100
    total_payment = loan_amount + total_interest
    monthly_payment = total_payment / (years * 12)

    print("\nLoan Amount      : Rs.", loan_amount)
    print("Total Interest   : Rs.", total_interest)
    print("Total Payment    : Rs.", total_payment)
    print("Monthly Payment  : Rs.", round(monthly_payment, 2))  



def restore_accounts():

    print("\n========= RESTORE DATABASE =========")

    try:
        connection.close()

        shutil.copy("bank_backup.db", "bank.db")

        print("Database Restored Successfully")

    except FileNotFoundError:
        print("Backup File Not Found")
           


# ---------------------------------------------------------------
# Save accounts to file
# ---------------------------------------------------------------



def save_transactions(account_no, transaction_type, amount):

    current_time = datetime.now()
    date_time = current_time.strftime("%d-%m-%Y %I:%M:%S %p")

    cursor.execute("""
    INSERT INTO transactions
    (account_no, transaction_type, amount, date_time)
    VALUES (?, ?, ?, ?)
    """, (
        account_no,
        transaction_type,
        amount,
        date_time
    ))

    connection.commit()


    

def login():
    global current_user

    try:
        account_no = int(input("Enter Account Number: "))
    except ValueError:
        print("Invalid Account Number")
        return False

    attempts = 3

    while attempts > 0:

        pin = input("Enter PIN: ")

        for account in accounts:

            if account["account_no"] == account_no and account["pin"] == pin:

                current_user = account

                print("\nLogin Successful")
                print("Welcome,", current_user["name"])

                return True

        attempts -= 1

        if attempts > 0:
            print("Invalid Account Number or PIN")
            print("Attempts Remaining :", attempts)

    print("Too many failed attempts.")
    return False

def logout():
    global current_user
    current_user = None 
    print("Logged out Successfully")

def customer_menu():

    while True:

        print("\n========= CUSTOMER MENU =========")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Mini Statement")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":

           print("\n========= YOUR BALANCE =========")
           print("Account Number :", current_user["account_no"])
           print("Account Holder :", current_user["name"])
           print("Balance        : Rs.", current_user["balance"])

        elif choice == "6":
            logout()
            break   

        elif choice == "2":

            try:
                deposit_no = int(input("Enter Account Number: "))
                deposit_amount = float(input("Enter Deposit Amount: "))
            except ValueError:
                print("Invalid Input")
                continue

            if deposit_amount <= 0:
                print("Deposit Amount must be greater than zero")
                continue

            found = False

            for account in accounts:

                if account["account_no"] == deposit_no:

                    found = True

                    account["balance"] += deposit_amount
                    current_user["balance"] = account["balance"]

                    cursor.execute("""
                    UPDATE accounts
                    SET balance = ?
                    WHERE account_no = ?
                    """, (
                        account["balance"],
                        account["account_no"]
                    ))

                    connection.commit()

                    save_transactions(
                        account["account_no"],
                        "Customer Deposit",
                        deposit_amount
                    )

                    print("Money Deposited Successfully")
                    print("Current Balance :", account["balance"])

                    break

            if not found:
                print("Account Not Found")

        elif choice == "3":

            amount = float(input("Enter Withdrawal Amount: "))

            if amount <= 0:
                print("Invalid Amount")
                continue

            if current_user["balance"] < amount:
                print("Insufficient Balance")
                continue

            current_user["balance"] -= amount

            cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE account_no = ?
            """, (
                current_user["balance"],
                current_user["account_no"]
            ))

            connection.commit()

            save_transactions(
                current_user["account_no"],
                "Customer Withdraw",
                amount
            )

            print("Money Withdrawn Successfully")
            print("Current Balance :", current_user["balance"])    


        elif choice == "4":

            try:
                to_account_no = int(input("Enter Recipient Account Number: "))
                amount = float(input("Enter Transfer Amount: "))
            except ValueError:
                print("Invalid Input")
                continue

            if amount <= 0:
                print("Invalid Amount")
                continue

            if current_user["account_no"] == to_account_no:
                print("Cannot transfer to your own account")
                continue

            receiver = None

            for account in accounts:
                if account["account_no"] == to_account_no:
                    receiver = account
                    break

            if receiver is None:
                print("Recipient Account Not Found")
                continue

            if current_user["balance"] < amount:
                print("Insufficient Balance")
                continue

            current_user["balance"] -= amount
            receiver["balance"] += amount

            cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE account_no = ?
            """, (
                current_user["balance"],
                current_user["account_no"]
            ))

            cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE account_no = ?
            """, (
                receiver["balance"],
                receiver["account_no"]
            ))

            connection.commit()

            save_transactions(
                current_user["account_no"],
                "Transfer To " + str(receiver["account_no"]),
                amount
            )

            save_transactions(
                receiver["account_no"],
                "Received From " + str(current_user["account_no"]),
                amount
            )

            print("Money Transferred Successfully")
            print("Your Balance :", current_user["balance"])   

        elif choice == "5":

            cursor.execute("""
            SELECT transaction_type, amount, date_time
            FROM transactions
            WHERE account_no = ?
            ORDER BY id DESC
            LIMIT 5
            """, (current_user["account_no"],))

            rows = cursor.fetchall()

            print("\n========= MINI STATEMENT =========")

            if len(rows) == 0:
                print("No Transactions Found")
            else:
                for row in rows:
                    print("---------------------------------")
                    print("Transaction :", row[0])
                    print("Amount      : Rs.", row[1])
                    print("Date & Time :", row[2])

                print("---------------------------------")        

# ADD HERE
def backup_accounts():

    print("\n========= BACKUP DATABASE =========")

    try:
        connection.commit()
        shutil.copy("bank.db", "bank_backup.db")
        print("Database Backup Created Successfully")

    except Exception as e:
        print("Backup Failed:", e)


def restore_accounts():

    global connection
    global cursor

    print("\n========= RESTORE DATABASE =========")

    try:

        connection.close()

        shutil.copy("bank_backup.db", "bank.db")

        # Re-open database
        connection = sqlite3.connect("bank.db")
        cursor = connection.cursor()

        print("Database Restored Successfully")

    except FileNotFoundError:
        print("Backup File Not Found")

    

while True:
    print("\n====== BANK MANAGEMENT SYSTEM ======")
    print("1. Create Account")
    print("2. Customaer Login")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Check Balance")
    print("6. View Account Details")
    print("7. Transfer Money")
    print("8. View Transaction History")
    print("9. Delete Account")
    print("10. Change Pin")
    print("11. Mini Statement")
    print("12. Interest Calculator")
    print("13. Loan Calculator")
    print("14. Backup Accounts")
    print("15. Restore Accounts")
    print("16. Admin Login")
    print("17. Exit")
    print("18. Bank Reports")

    choice = input("Enter your choice: ")

    if choice == "1":
        print("\nCreate Account")

        name = input("Enter account holder name: ")
        if name.strip() == "":
            print("Name cannot be empty")
            continue

        try:
            balance = float(input("Enter Opening Balance: "))
        except ValueError:
            print("Invalid Amount")
            continue

        if balance < 1000:
            print("Minimum Opening Balance is Rs.1000")
            continue

        duplicate = False

        for account in accounts:
            if account["name"].lower() == name.lower():
               duplicate = True
               break

        if duplicate:
            print("An account with this name already exists")
            continue

        pin = input("Create a 4-digit PIN: ")
        if len(pin) != 4 or not pin.isdigit():
            print("PIN must be exactly 4 digits")
            continue

        account = {
            "account_no": len(accounts) + 1001,
            "name": name,
            "balance": balance,
            "pin": pin
        }

        accounts.append(account)

        cursor.execute("""
        INSERT INTO accounts
        (account_no, name, balance, pin)
        VALUES (?, ?, ?, ?)
        """, (
            account["account_no"],
            account["name"],
            account["balance"],
            account["pin"]
        ))

        connection.commit()

        print("Account Created Successfully")
        print("Account Number :", account["account_no"])
        print("Account Holder :", account["name"])
        print("Balance        :", account["balance"])

    elif choice == "2":
        print("\nCustomer Login")

        if login():
            customer_menu()

    elif choice == "3":
        print("\nDeposit Money")

        deposit_no = int(input("Enter Account Number: "))

        for account in accounts:
            if account["account_no"] == deposit_no:

                try:
                   deposit_amount = float(input("Enter Deposit Amount: "))
                except ValueError:
                   print("Invalid Amount")
                   break

                if deposit_amount <= 0:
                   print("Deposit Amount must be greater than zero")
                   break

                account["balance"] += deposit_amount

                cursor.execute("""
                UPDATE accounts
                SET balance = ?
                WHERE account_no = ?
                """, (
                    account["balance"],
                    account["account_no"]
                ))

                connection.commit()

                save_transactions(account["account_no"], "deposit", deposit_amount)

                print("Money Deposited Successfully")
                print("New Balance :", account["balance"])
                break
        else:
            print("Account Not Found")

    elif choice == "4":
        print("\nWithdraw Money")

        withdraw_no = int(input("Enter Account Number: "))

        try:
            entered_pin = input("Enter PIN: ")
        except ValueError:
            print("Invalid PIN")
            continue

        for account in accounts:
            if account["account_no"] == withdraw_no:

                if account["pin"] != entered_pin:
                    print("Invalid PIN")
                    break

                print("Current Balance :", account["balance"])

                try:
                    withdraw_amount = float(input("Enter Withdrawal Amount: "))
                except ValueError:
                    print("Invalid Amount")
                    break

                if withdraw_amount <= 0:
                    print("Withdrawal Amount must be greater than zero")
                    break

                if account["balance"] >= withdraw_amount:
                    account["balance"] -= withdraw_amount

                    cursor.execute("""
                    UPDATE accounts
                    SET balance = ?
                    WHERE account_no = ?
                    """, (
                        account["balance"],
                        account["account_no"]
                    ))

                    connection.commit()

                    save_transactions(
                        account["account_no"],
                        "withdraw",
                        withdraw_amount
                    )

                    print("Money Withdrawn Successfully")
                    print("Remaining Balance :", account["balance"])

                else:
                    print("Insufficient Balance")

                break    


    elif choice == "5":
        print("\n========= CHECK BALANCE =========")

        try:
            balance_no = int(input("Enter Account Number: "))
        except ValueError:
            print("Invalid Account Number")
            continue

        entered_pin = input("Enter PIN: ")

        for account in accounts:
            if account["account_no"] == balance_no:

                if account["pin"] != entered_pin:
                    print("Invalid PIN")
                    break

                print("\n========= ACCOUNT BALANCE =========")
                print("Account Number :", account["account_no"])
                print("Account Holder :", account["name"])
                print("Balance        : Rs.", account["balance"])
                break

        else:
            print("Account Not Found")
    
    elif choice == "6":
        print("\n========= ACCOUNT DETAILS =========")

        try:
            account_no= int(input("Enter Account Number: "))
        except ValueError:
            print("Invalid Account Number")
            continue

        entered_pin = int(input("Enter PIN: "))

        for account in accounts:

            if account["account_no"] == account_no:

                if account["pin"] != entered_pin:
                    print("Invalid PIN")
                    break

                print("\n========= ACCOUNT INFORMATION =========")
                print("Account Number :", account["account_no"])
                print("Account Holder :", account["name"])
                print("Balance        : Rs.", account["balance"])
                print("PIN            :", account["pin"])
                break

        else:
            print("Account Not Found")

    elif choice == "7":
        print("\n========= TRANSFER MONEY =========")

        try:
            from_account_no = int(input("Enter Your Account Number: "))
        except ValueError:
            print("Invalid Account Number")
            continue

        entered_pin = input("Enter PIN: ")

        try:
            to_account_no = int(input("Enter Receiver Account Number: "))
        except ValueError:
            print("Invalid Receiver Account Number")
            continue 
        if from_account_no == to_account_no:
           print("You cannot transfer money to the same account")
           continue

        try:
            transfer_amount = float(input("Enter Transfer Amount: "))
        except ValueError:
            print("Invalid Transfer Amount")
            continue

        # invalid amount check
        if transfer_amount <= 0:
            print("invalid transfer amount")
            continue

        from_account = None
        to_account = None

        for account in accounts:
            if account["account_no"] == from_account_no:
                from_account = account

            if account["account_no"] == to_account_no:
                to_account = account

        if from_account is None:
            print("sender account not found")

        elif to_account is None:
            print("recipient account not found")

        elif from_account["pin"] != entered_pin:
            print("Invalid PIN")

        elif from_account["balance"] < transfer_amount:
            print("Insufficient Balance")
            
        else:
            from_account["balance"] -= transfer_amount
            to_account["balance"] += transfer_amount

            cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE account_no = ?
            """, (
                from_account["balance"],
                from_account["account_no"]
            ))
            
            cursor.execute("""
            UPDATE accounts
            SET balance = ?
            WHERE account_no = ?
            """, (
                to_account["balance"],
                to_account["account_no"]
            ))

            connection.commit()

            save_transactions(from_account["account_no"],
                  "Transfer To " + str(to_account["account_no"]),
                  transfer_amount)

            save_transactions(to_account["account_no"],
                  "Received From " + str(from_account["account_no"]),
                  transfer_amount)



            print("\nMoney Transferred Successfully")
            print("Sender Balance :", from_account["balance"])
            print("Recipient Balance :", to_account["balance"])

    elif choice == "8":
        print("\n========= TRANSACTION HISTORY =========")

        try:
            account_no = int(input("Enter Account Number: "))
        except ValueError:
            print("Invalid Account Number")
            continue

        cursor.execute("""
            SELECT transaction_type, amount, date_time
            FROM transactions
            WHERE account_no = ?
            """, (account_no,))

        rows = cursor.fetchall()

        if len(rows) == 0:
            print("No Transactions Found")
        else:
            print("\n====== TRANSACTION HISTORY ======")

            for row in rows:
                print("---------------------------------")
                print("Transaction :", row[0])
                print("Amount      : Rs.", row[1])
                print("Date & Time :", row[2])

                print("---------------------------------")

    elif choice == "9":
        print("\nDelete Account")

        try:
            account_no = int(input("Enter Account Number: "))
        except ValueError:
            print("Invalid Account Number")
            continue

        entered_pin = input("Enter pin: ")

        found = False 

        for account in accounts:

            if account["account_no"] ==  account_no:
                found = True

                if account["pin"] != entered_pin:
                    print("Invalid pin")
                    break

                confirm = input("Are you sure you want to delete this account? (Y/N): ").strip().upper()

                if confirm == "Y":
                    cursor.execute("""
                    DELETE FROM accounts
                    WHERE account_no = ?
                    """, (account_no,))

                    connection.commit()

                    accounts.remove(account)

                    save_transactions(
                        account_no,
                        "Account Deleted",
                        0
                    )

                    print("Account Deleted Successfully")
                else:
                    print("Account Deletion Cancelled")

                break

        if not found:
            print("Account Not Found")       


    elif choice == "10":
        print("\nChange PIN")

        account_no = int(input("Enter Account Number: "))
        current_pin = input("Enter Current PIN: ")

        found = False

        for account in accounts:

            if account["account_no"] == account_no:

                found = True

                if account["pin"] != current_pin:
                  print("Invalid PIN")
                  break

                new_pin = input("Enter New PIN: ")
                confirm_pin = input("Confirm New PIN: ")

                if new_pin != confirm_pin:
                   print("PINs do not match")
                   break

                if len(new_pin) != 4 or not new_pin.isdigit():
                   print("PIN must be exactly 4 digits")
                   break

                cursor.execute("""
                UPDATE accounts
                SET pin = ?
                WHERE account_no = ?
                """, (
                    new_pin,
                    account_no
                ))

                connection.commit()

                # Update memory list
                account["pin"] = new_pin

                save_transactions(
                    account_no,
                    "PIN Changed",
                    0
               )

                print("PIN Changed Successfully")

                break

        if not found:
           print("Account Not Found")    

    elif choice == "11":
        print("\n========= MINI STATEMENT =========")

        try:
            account_no = int(input("Enter Account Number: "))
        except ValueError:
            print("Invalid Account Number")
            continue

        entered_pin = input("Enter PIN: ")

        found = False

        for account in accounts:

            if account["account_no"] == account_no:

                found = True

                if account["pin"] != entered_pin:
                   print("Invalid PIN")
                   break

                cursor.execute("""
                SELECT transaction_type, amount, date_time
                FROM transactions
                WHERE account_no = ?
                ORDER BY id DESC
                LIMIT 5
                """, (account_no,))

                rows = cursor.fetchall()

                if len(rows) == 0:
                   print("No Transactions Found")
                else:
                    print("\n========= MINI STATEMENT =========")
 
                    for row in rows:
                        print("---------------------------------")
                        print("Transaction :", row[0])
                        print("Amount      : Rs.", row[1])
                        print("Date & Time :", row[2])

                    print("---------------------------------")

                break

        if not found:
           print("Account Not Found")

    elif choice == "12":
        interest_calculator()   


    elif choice == "13":
        loan_calculator()


    elif choice == "14":
        backup_accounts()


    elif choice == "15":
        restore_accounts()     


    elif choice == "16":
        if admin_login():




            admin_dashboard()

            while True:

                print("\n========= ADMIN PANEL =========")
                print("1. View All Accounts")
                print("2. Search Account")
                print("3. View All Transactions")
                print("4. Delete Any Account")
                print("5. Total Bank Balance")
                print("6. Total Accounts")
                print("7. Logout")

                admin_choice = input("Enter your choice:")


                if admin_choice == "1":
                    admin_view_all_accounts()

                elif admin_choice == "2":
                    admin_search_account()

                elif admin_choice == "3":
                    admin_view_all_transactions()

                elif admin_choice == "4":
                    admin_delete_any_account()

                elif admin_choice == "5":
                    admin_total_bank_balance()

                elif admin_choice == "6":
                    admin_total_accounts()

                elif admin_choice == "7":
                    admin_logout()
                    break

                else:
                    print("Invalid Choice")

    elif choice == "18":

        while True:
      
            print("\n========= BANK REPORTS =========")
            print("1. Total Accounts")
            print("2. Total Bank Balance")
            print("3. Highest Balance Account")
            print("4. Lowest Balance Account")
            print("5. Today's Transactions")
            print("6. Back")

            report_choice = input("Enter your choice: ")

            if report_choice == "6":
                break

            elif report_choice == "1":

                cursor.execute("""
                SELECT COUNT(*)
                FROM accounts
                """)

                total_accounts = cursor.fetchone()[0]

                print("\n========= TOTAL ACCOUNTS REPORT =========")
                print("Total Accounts :", total_accounts)
            elif report_choice == "2":

                cursor.execute("""
                SELECT SUM(balance)
                FROM accounts
                """)

                total_balance = cursor.fetchone()[0]

                if total_balance is None:
                    total_balance = 0

                print("\n========= TOTAL BANK BALANCE REPORT =========")
                print("Total Bank Balance : Rs.", total_balance)

            elif report_choice == "3":

                cursor.execute("""
                SELECT account_no, name, balance
                FROM accounts
                ORDER BY balance DESC
                LIMIT 1
                """)

                row = cursor.fetchone()

                if row:
                    print("\n========= HIGHEST BALANCE ACCOUNT =========")
                    print("Account Number :", row[0])
                    print("Account Holder :", row[1])
                    print("Balance        : Rs.", row[2])
                else:
                    print("No Accounts Found")


            elif report_choice == "4":

                cursor.execute("""
                SELECT account_no, name, balance
                FROM accounts
                ORDER BY balance ASC
                LIMIT 1
                """)

                row = cursor.fetchone()

                if row:
                    print("\n========= LOWEST BALANCE ACCOUNT =========")
                    print("Account Number :", row[0])
                    print("Account Holder :", row[1])
                    print("Balance        : Rs.", row[2])
                else:
                    print("No Accounts Found")


            elif report_choice == "5":

                print("\n========= TODAY'S TRANSACTIONS =========")

                today = datetime.now().strftime("%d-%m-%Y")

                cursor.execute("""
                SELECT account_no, transaction_type, amount, date_time
                FROM transactions
                WHERE date_time LIKE ?
                ORDER BY id DESC
                """, (today + "%",))

                rows = cursor.fetchall()

                if len(rows) == 0:
                    print("No Transactions Today")

                else:
                    print("-" * 55)

                    for row in rows:
                        print("Account No :", row[0])
                        print("Type       :", row[1])
                        print("Amount     : Rs.", row[2])
                        print("Date & Time:", row[3])
                        print("-" * 55)

           

            else:
                print("Invalid Choice")               

    elif choice == "17":
        print("Thank You 👋")
        break

    else:
        print("Invalid Choice")


