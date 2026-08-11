
from tkinter import (
    Tk,
    Toplevel,
    Label,
    Entry,
    Button,
    Text,
    Frame,
    Canvas,
    Scrollbar,
    Listbox,
    END,
    LEFT,
    StringVar,
    OptionMenu,
    messagebox,
    filedialog
)
from tkinter import simpledialog
from builtins import Exception, ValueError, print, int, float, str, len
import sqlite3
import shutil
from datetime import date, datetime
import random
import os
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
from reportlab.pdfgen import canvas

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

print("GUI FILE:", __file__)

conn = sqlite3.connect("bank.db")

print(os.getcwd())
cursor = conn.cursor()


conn.commit()

# Add extra profile columns if they don't exist

try:
    cursor.execute("ALTER TABLE accounts ADD COLUMN phone TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE accounts ADD COLUMN email TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE accounts ADD COLUMN address TEXT")
except:
    pass

try:
    cursor.execute("ALTER TABLE accounts ADD COLUMN photo TEXT")
except:
    pass

conn.commit()


cursor.execute("""
CREATE TABLE IF NOT EXISTS fixed_deposits(

    fd_id INTEGER PRIMARY KEY AUTOINCREMENT,

    account_no INTEGER,

    amount REAL,

    years INTEGER,

    interest_rate REAL,

    maturity_amount REAL,

    status TEXT

)
""")

conn.commit()


cursor.execute("""
CREATE TABLE IF NOT EXISTS loans(
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no INTEGER,
    loan_type TEXT,
    amount REAL,
    interest REAL,
    months INTEGER,
    emi REAL,
    status TEXT,
    date TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS atm_cards(

    card_id INTEGER PRIMARY KEY AUTOINCREMENT,

    account_no INTEGER,

    card_number TEXT,

    card_type TEXT,

    expiry_date TEXT,

    status TEXT,

    pin TEXT,

    failed_attempts INTEGER DEFAULT 0

)
""")


conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no INTEGER,
    transaction_type TEXT,
    amount REAL,
    date_time TEXT
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_no INTEGER,
    message TEXT,
    date_time TEXT,
    status TEXT DEFAULT 'Unread'
)
""")

conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin_logs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    activity TEXT,
    date_time TEXT
)
""")

conn.commit()

def add_notification(account_no, message):

    cursor.execute("""
    INSERT INTO notifications(
        account_no,
        message,
        date_time,
        status
    )
    VALUES(?,?,?,?)
    """, (
        account_no,
        message,
        datetime.now().strftime("%d-%m-%Y %I:%M:%S %p"),
        "Unread"
    ))

    conn.commit()

def add_admin_log(activity):

    cursor.execute("""
    INSERT INTO admin_logs(
        activity,
        date_time
    )
    VALUES(?,?)
    """,(
        activity,
        datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    ))

    conn.commit()    


class Command:
    """Simple command base class with default useful implementations.

    Provides two methods commonly used by command patterns: execute and undo.
    Subclasses may override these, but sensible defaults are provided so code
    depending on a Command can call them without checking for implementation.
    """

    def execute(self, *args, **kwargs):
        """Execute the command.

        Default implementation does nothing and returns a success tuple.
        Subclasses should perform their action and return (True, result) on
        success or (False, error_message) on failure.
        """
        return True, None

    def undo(self, *args, **kwargs):
        """Undo the command's effect.

        Default implementation performs no-op and returns (True, None).
        Subclasses that modify state should override this to provide a
        compensating action.
        """
        return True, None
    

def apply_atm_card(account_no):

    cursor.execute("""
    SELECT *
    FROM atm_cards
    WHERE account_no=?
    """,(account_no,))

    if cursor.fetchone():
        messagebox.showinfo(
            "ATM",
            "ATM Card Already Applied"
        )
        return

    card_number = str(random.randint(4000000000000000,4999999999999999))

    atm_pin = str(random.randint(1000,9999))
    
    expiry_date = "08/2031"

    cursor.execute("""
    INSERT INTO atm_cards(
    account_no,
    card_number,
    card_type,
    expiry_date,
    status,
    pin
    )
    VALUES(?,?,?,?,?,?)
    """,(
        account_no,
        card_number,
        "Debit Card",
        expiry_date,
        "Approved",
        atm_pin
    ))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "ATM Card Request Sent Successfully"
    )

def atm_withdraw(account_no):

    window = Toplevel(root)
    window.title("ATM Withdrawal")
    window.geometry("400x400")
    window.configure(bg="white")

    Label(window,
          text="ATM CASH WITHDRAWAL",
          font=("Arial",16,"bold"),
          bg="white",
          fg="blue").pack(pady=10)

    Label(window, text="Card Number", bg="white").pack()
    card_entry = Entry(window, width=30)
    card_entry.pack(pady=5)

    Label(window, text="ATM PIN", bg="white").pack()
    pin_entry = Entry(window, show="*", width=30)
    pin_entry.pack(pady=5)

    Label(window, text="Amount", bg="white").pack()
    amount_entry = Entry(window, width=30)
    amount_entry.pack(pady=5)    

    Label(
        window,
        text="FAST CASH",
        bg="white",
        font=("Arial", 11, "bold")
    ).pack(pady=5)

    fast_frame = Frame(window, bg="white")
    fast_frame.pack()

    Button(
        fast_frame,
        text="500",
        width=8,
        command=lambda: (
            amount_entry.delete(0, END),
            amount_entry.insert(0, "500")
        )
    ).grid(row=0, column=0, padx=5, pady=5)

    Button(
        fast_frame,
        text="1000",
        width=8,
        command=lambda: (
            amount_entry.delete(0, END),
            amount_entry.insert(0, "1000")
        )
    ).grid(row=0, column=1, padx=5, pady=5)

    Button(
        fast_frame,
        text="2000",
        width=8,
        command=lambda: (
            amount_entry.delete(0, END),
            amount_entry.insert(0, "2000")
        )
    ).grid(row=1, column=0, padx=5, pady=5)

    Button(
        fast_frame,
        text="5000",
        width=8,
        command=lambda: (
            amount_entry.delete(0, END),
            amount_entry.insert(0, "5000")
        )
    ).grid(row=1, column=1, padx=5, pady=5)

    Button(
        fast_frame,
        text="10000",
        width=8,
        command=lambda: (
            amount_entry.delete(0, END),
            amount_entry.insert(0, "10000")
        )
    ).grid(row=2, column=0, columnspan=2, pady=5)

    def withdraw():

        card_no = card_entry.get()
        pin = pin_entry.get()

        if amount_entry.get() == "":
            messagebox.showerror("Error", "Enter Amount")
            return

        amount = float(amount_entry.get())


        # Get ATM card details
        cursor.execute("""
        SELECT status, pin, failed_attempts
        FROM atm_cards
        WHERE account_no=? AND card_number=?
        """, (account_no, card_no))

        card = cursor.fetchone()

        if card is None:
            messagebox.showerror(
                "Error",
                "Invalid Card Number"
            )
            return

        status, db_pin, failed_attempts = card

        # Check if card is blocked
        if status == "Blocked":
            messagebox.showerror(
                "Blocked",
                "Your ATM Card is Blocked"
            )
            return

        # Check PIN
        if str(pin) != str(db_pin):

            failed_attempts += 1

            if failed_attempts >= 3:

                cursor.execute("""
                UPDATE atm_cards
                SET failed_attempts=3,
                    status='Blocked'
                WHERE account_no=? AND card_number=?
                """, (account_no, card_no))

                conn.commit()

                messagebox.showerror(
                    "Blocked",
                    "3 Wrong PIN Attempts\nATM Card Blocked"
                )

                return

            else:

                remaining = 3 - failed_attempts

                cursor.execute("""
                UPDATE atm_cards
                SET failed_attempts=?
                WHERE account_no=? AND card_number=?
                """, (
                    failed_attempts,
                    account_no,
                    card_no))

                conn.commit()

                messagebox.showerror(
                    "Wrong PIN",
                    f"Invalid PIN\n{remaining} Attempts Remaining"
                )

                return

        # Correct PIN → Reset failed attempts
        cursor.execute("""
        UPDATE atm_cards
        SET failed_attempts=0
        WHERE account_no=? AND card_number=?
        """, (account_no, card_no))

        conn.commit()

        print("Card Status =", status)

        if status not in ("Approved", "Active"):
            messagebox.showerror(
                "Error",
                "ATM Card Not Approved"
            )
            return

        # Daily Withdrawal Limit Check
        daily_limit = 50000

        today = datetime.now().strftime("%d-%m-%Y")

        cursor.execute("""
        SELECT SUM(amount)
        FROM transactions
        WHERE account_no=?
        AND transaction_type='ATM Withdrawal'
        AND date_time LIKE ?
        """, (
            account_no,
            today + "%"
        ))

        daily_withdrawn = cursor.fetchone()[0]

        if daily_withdrawn is None:
            daily_withdrawn = 0

        if daily_withdrawn + amount > daily_limit:
            remaining = daily_limit - daily_withdrawn
            messagebox.showerror(
                "Daily Limit Exceeded",
                f"Daily ATM Limit : Rs.{daily_limit}\n"
                f"Already Withdrawn : Rs.{daily_withdrawn}\n"
                f"Remaining : Rs.{remaining}"
            )
            return

        # Balance Check
        cursor.execute("""
        SELECT balance
        FROM accounts
        WHERE account_no=?
        """, (account_no,))

        balance = cursor.fetchone()[0]

        if balance < amount:
            messagebox.showerror(
                "Error",
                "Insufficient Balance"
            )
            return

        # Withdraw Money
        cursor.execute("""
        UPDATE accounts
        SET balance = balance - ?
        WHERE account_no=?
        """, (amount, account_no))

        conn.commit()

        # Transaction Save
        cursor.execute("""
        INSERT INTO transactions
        (account_no, transaction_type, amount, date_time)
        VALUES (?, ?, ?, ?)
        """, (
            account_no,
            "ATM Withdrawal",
            amount,
            datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        ))

        

        conn.commit()

        # Get New Balance
        cursor.execute("""
        SELECT balance
        FROM accounts
        WHERE account_no=?
        """, (account_no,))
        
        new_balance = cursor.fetchone()[0]

        

        generate_atm_receipt(
            account_no,
            "Withdrawal",
            amount,
            new_balance
        )

        generate_pdf_receipt(
            account_no,
            "Withdrawal",
            amount,
            new_balance
        )
        

        add_notification(
            account_no,
            f"Rs.{amount} ATM Withdrawn Successfully"
        )

        messagebox.showinfo(
            "Success",
            f"Rs.{amount} Withdrawn Successfully"
        )

        window.destroy()

    Button(
        window,
        text="Withdraw",
        font=("Arial",12,"bold"),
        bg="green",
        fg="white",
        width=15,
        command=withdraw
    ).pack(pady=20)

def change_atm_pin(account_no):

    window = Toplevel(root)
    window.title("ATM Change PIN")
    window.geometry("400x350")
    window.configure(bg="white")

    Label(
        window,
        text="CHANGE ATM PIN",
        font=("Arial",16,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=10)

    Label(window, text="Card Number", bg="white").pack()
    card_entry = Entry(window, width=30)
    card_entry.pack(pady=5)

    Label(window, text="Current PIN", bg="white").pack()
    old_pin_entry = Entry(window, show="*", width=30)
    old_pin_entry.pack(pady=5)

    Label(window, text="New PIN", bg="white").pack()
    new_pin_entry = Entry(window, show="*", width=30)
    new_pin_entry.pack(pady=5)

    Label(window, text="Confirm PIN", bg="white").pack()
    confirm_pin_entry = Entry(window, show="*", width=30)
    confirm_pin_entry.pack(pady=5)



    def change():

        old_pin = old_pin_entry.get()
        new_pin = new_pin_entry.get()
        confirm_pin = confirm_pin_entry.get()

        if old_pin == "" or new_pin == "" or confirm_pin == "":
            messagebox.showerror(
                "Error",
                "Fill all fields"
            )
            return

        if new_pin != confirm_pin:
            messagebox.showerror(
                "Error",
                "New PIN and Confirm PIN do not match"
            )
            return

        if len(new_pin) != 4 or not new_pin.isdigit():
            messagebox.showerror(
                "Error",
                "PIN must be exactly 4 digits"
            )
            return

        cursor.execute("""
        SELECT pin
        FROM atm_cards
        WHERE account_no=?
        """, (account_no,))

        row = cursor.fetchone()

        if row is None:
            messagebox.showerror(
                "Error",
                "ATM Card Not Found"
            )
            return

        if row[0] != old_pin:
            messagebox.showerror(
                "Error",
                "Old PIN Incorrect"
            )
            return

        cursor.execute("""
        UPDATE atm_cards
        SET pin=?
        WHERE account_no=?
        """, (new_pin, account_no))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "ATM PIN Changed Successfully"
       )

        window.destroy()

    
    def update_pin():

        card_no = card_entry.get()
        old_pin = old_pin_entry.get()
        new_pin = new_pin_entry.get()
        confirm_pin = confirm_pin_entry.get()

        if card_no == "" or old_pin == "" or new_pin == "" or confirm_pin == "":
            messagebox.showerror("Error", "Fill all fields")
            return

        if new_pin != confirm_pin:
            messagebox.showerror(
                "Error",
                "New PIN and Confirm PIN do not match"
            )
            return

        if len(new_pin) != 4 or not new_pin.isdigit():
            messagebox.showerror(
                "Error",
                "PIN must be exactly 4 digits"
            )
            return

        cursor.execute("""
        SELECT *
        FROM atm_cards
        WHERE account_no=? AND card_number=? AND pin=?
        """, (account_no, card_no, old_pin))

        if cursor.fetchone() is None:
            messagebox.showerror(
                "Error",
                "Invalid Card Number or PIN"
            )
            return

        cursor.execute("""
        UPDATE atm_cards
        SET pin=?
        WHERE account_no=? AND card_number=?
        """, (new_pin, account_no, card_no))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "ATM PIN Changed Successfully"
        )

        window.destroy()

    Button(
        window,
        text="Change PIN",
        bg="green",
        fg="white",
        font=("Arial",12,"bold"),
        command=update_pin
    ).pack(pady=20)    
    

def block_atm_card(account_no):

    cursor.execute("""
    UPDATE atm_cards
    SET status='Blocked'
    WHERE account_no=?
    """, (account_no,))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "ATM Card Blocked Successfully"
    )        

def unblock_atm_card(account_no):

    cursor.execute("""
    UPDATE atm_cards
    SET status='Approved',
        failed_attempts=0
    WHERE account_no=?
    """, (account_no,))

    conn.commit()

    messagebox.showinfo(
        "Success",
        "ATM Card Unblocked Successfully"
    )

def atm_balance_inquiry(account_no):

    cursor.execute("""
    SELECT balance
    FROM accounts
    WHERE account_no=?
    """, (account_no,))

    result = cursor.fetchone()

    if result:
        balance = result[0]

        messagebox.showinfo(
            "ATM Balance",
            f"Available Balance : Rs.{balance}"
        )

    else:
        messagebox.showerror(
            "Error",
            "Account Not Found"
        )  

def admin_atm_dashboard():

    window = Toplevel(root)
    window.title("Admin ATM Management")
    window.geometry("700x500")
    window.configure(bg="white")


    Label(
        window,
        text="ADMIN ATM MANAGEMENT DASHBOARD",
        font=("Arial",16,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=10)


    text = Text(
        window,
        width=80,
        height=20
    )
    text.pack(pady=10)

    Label(
        window,
        text="Account Number",
        bg="white"
    ).pack()

    account_entry = Entry(
        window,
        width=25
    )

    account_entry.pack(pady=5)


    def load_cards():

        text.delete("1.0", END)

        cursor.execute("""
        SELECT 
        card_id,
        account_no,
        card_number,
        card_type,
        status
        FROM atm_cards
        """)

        cards = cursor.fetchall()


        if not cards:
            text.insert(
                END,
                "No ATM Cards Found"
            )
            return


        for card in cards:

            text.insert(
                END,
                f"""
Card ID      : {card[0]}
Account No   : {card[1]}
Card Number  : {card[2]}
Type         : {card[3]}
Status       : {card[4]}
------------------------------
"""
            )

    def block_card():
    
            account_no = account_entry.get()
    
            cursor.execute("""
            UPDATE atm_cards
            SET status='Blocked'
            WHERE account_no=?
            """,(account_no,))
    
            conn.commit()
    
            messagebox.showinfo(
                "Success",
                "ATM Card Blocked Successfully"
            )
    
            load_cards()      
    
    def unblock_card():
    
        account_no = account_entry.get()
    
        cursor.execute("""
        UPDATE atm_cards
        SET status='Approved',
            failed_attempts=0
        WHERE account_no=?
        """,(account_no,))
    
        conn.commit()
    
        messagebox.showinfo(
            "Success",
            "ATM Card Unblocked Successfully"
        )
    
        load_cards()        


    Button(
        window,
        text="View ATM Cards",
        bg="green",
        fg="white",
        width=20,
        command=load_cards
    ).pack(pady=5)    

    Button(
        window,
        text="Block ATM Card",
        bg="red",
        fg="white",
        width=20,
        command=block_card
    ).pack(pady=5)


    Button(
        window,
        text="Unblock ATM Card",
        bg="green",
        fg="white",
        width=20,
        command=unblock_card
    ).pack(pady=5)

def search_atm_card(account_no):

    cursor.execute("""
    SELECT
        card_id,
        account_no,
        card_number,
        card_type,
        expiry_date,
        status,
        IFNULL(failed_attempts,0)
    FROM atm_cards
    WHERE account_no=?
    """, (account_no,))

    card = cursor.fetchone()

    if card is None:
        messagebox.showerror(
            "Error",
            "ATM Card Not Found"
        )
        return

    messagebox.showinfo(
        "ATM CARD DETAILS",
        f"""
Card ID          : {card[0]}
Account Number   : {card[1]}
Card Number      : {card[2]}
Card Type        : {card[3]}
Expiry Date      : {card[4]}
Status           : {card[5]}
Failed Attempts  : {card[6]}
"""
    )


def atm_mini_statement(account_no):

    cursor.execute("""
    SELECT date_time, transaction_type, amount
    FROM transactions
    WHERE account_no=?
    ORDER BY id DESC
    LIMIT 5
    """, (account_no,))

    rows = cursor.fetchall()

    if rows:

        statement = "ATM MINI STATEMENT\n\n"

        for row in rows:
            statement += f"""
Date : {row[0]}
Type : {row[1]}
Amount : Rs.{row[2]}
------------------------
"""

        messagebox.showinfo(
            "ATM Mini Statement",
            statement
        )

    else:
        messagebox.showinfo(
            "ATM Mini Statement",
            "No Transactions Found"
        )

def atm_transaction_history(account_no):

    window = Toplevel(root)
    window.title("ATM Transaction History")
    window.geometry("600x400")
    window.configure(bg="white")


    Label(
        window,
        text="ATM TRANSACTION HISTORY",
        font=("Arial",16,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=10)


    text = Text(
        window,
        width=70,
        height=18,
        font=("Arial",11)
    )

    text.pack(padx=10,pady=10)


    cursor.execute("""
    SELECT date_time, transaction_type, amount
    FROM transactions
    WHERE account_no=?
    ORDER BY id DESC
    """,(account_no,))


    rows = cursor.fetchall()


    if rows:

        for row in rows:

            text.insert(
                END,
                f"""
Date : {row[0]}
Type : {row[1]}
Amount : Rs.{row[2]}
-----------------------------
"""
            )

    else:

        text.insert(
            END,
            "No Transactions Found"
        )


    text.config(state="disabled")        

def generate_atm_receipt(account_no, transaction_type, amount, balance):

    now = datetime.now()

    receipt = f"""
================================
       BANK MANAGEMENT SYSTEM
          ATM RECEIPT
================================

Account Number : {account_no}

Transaction    : {transaction_type}
Amount         : Rs.{amount}

Date           : {now.strftime("%d-%m-%Y")}
Time           : {now.strftime("%I:%M %p")}

Available Balance : Rs.{balance}

================================
        THANK YOU
     VISIT AGAIN
================================
"""

    file_name = f"ATM_Receipt_{account_no}.txt"

    with open(file_name, "w") as file:
        file.write(receipt)


    messagebox.showinfo(
        "ATM Receipt",
        f"Receipt Generated Successfully\n\nSaved as {file_name}"
    )

def stat_box(parent, title, value, color, row, col):

    frame = Frame(
        parent,
        bg=color,
        width=180,
        height=90,
        relief="raised",
        bd=3
    )

    frame.grid(
        row=row,
        column=col,
        padx=12,
        pady=12
    )

    frame.grid_propagate(False)

    Label(
        frame,
        text=value,
        font=("Arial",20,"bold"),
        bg=color,
        fg="white"
    ).pack(pady=8)

    Label(
        frame,
        text=title,
        font=("Arial",11,"bold"),
        bg=color,
        fg="white"
    ).pack()


def admin_dashboard():

    window = Toplevel(root)
    window.title("Admin Dashboard")
    window.geometry("700x750")
    window.configure(bg="white")


    Label(
        window,
        text="BANK ADMIN DASHBOARD",
        font=("Arial",18,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=20)


    # Total Customers
    cursor.execute("""
    SELECT COUNT(*)
    FROM accounts
    """)

    customers = cursor.fetchone()[0]


    # Total Balance
    cursor.execute("""
    SELECT SUM(balance)
    FROM accounts
    """)

    balance = cursor.fetchone()[0]

    if balance is None:
        balance = 0


    # ATM Cards
    cursor.execute("""
    SELECT COUNT(*)
    FROM atm_cards
    """)

    cards = cursor.fetchone()[0]


    # Blocked Cards
    cursor.execute("""
    SELECT COUNT(*)
    FROM atm_cards
    WHERE status='Blocked'
    """)

    blocked = cursor.fetchone()[0]

    # Active ATM Cards
    cursor.execute(""" 
    SELECT COUNT(*)
    FROM atm_cards
    WHERE status='Approved'
    """)

    active_cards = cursor.fetchone()[0]

    # Fixed Deposits
    cursor.execute("""
    SELECT COUNT(*)
    FROM fixed_deposits
    """)

    fixed_deposits = cursor.fetchone()[0]


    # Active Loans
    cursor.execute("""
    SELECT COUNT(*)
    FROM loans
    WHERE status='Active'
    """)

    active_loans = cursor.fetchone()[0]


    # Transactions
    cursor.execute("""
    SELECT COUNT(*)
    FROM transactions
    """)

    transactions = cursor.fetchone()[0]

    stats_frame = Frame(window, bg="white")
    stats_frame.pack(pady=10)
    stat_box(stats_frame, "Customers", customers, "#2E8B57", 0, 0)
    stat_box(stats_frame, "ATM Cards", cards, "#1E90FF", 0, 1)
    stat_box(stats_frame, "Blocked Cards", blocked, "#DC143C", 1, 0)
    stat_box(stats_frame, "Transactions", transactions, "#FF8C00", 1, 1)

    Label(
        window,
        text="Recent Transactions",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="blue"
    ).pack(pady=(10, 5))

    recent_box = Listbox(
        window,
        width=60,
        height=8,
        font=("Consolas", 10)
    )
    recent_box.pack(padx=10, pady=5)

    Label(
       window,
       text="TRANSACTION ANALYTICS",
       font=("Arial", 14, "bold"),
       bg="white",
       fg="darkgreen"
    ).pack(pady=(15, 5))

    analytics_frame = Frame(window, bg="white")
    analytics_frame.pack(pady=10)

    # Deposit Count
    cursor.execute("""
    SELECT COUNT(*)
    FROM transactions
    WHERE transaction_type='Deposit'
    """)
    deposits = cursor.fetchone()[0]

    # Withdraw Count
    cursor.execute("""
    SELECT COUNT(*)
    FROM transactions
    WHERE transaction_type='Withdraw'
    """)
    withdrawals = cursor.fetchone()[0]

    # Transfer Count
    cursor.execute("""
    SELECT COUNT(*)
    FROM transactions
    WHERE transaction_type LIKE '%Transfer%'
    """)
    transfers = cursor.fetchone()[0]

    # ATM Withdrawals
    cursor.execute("""
    SELECT COUNT(*)
    FROM transactions
    WHERE transaction_type='ATM Withdrawal'
    """)
    atm_withdrawals = cursor.fetchone()[0]

    # EMI Payments
    cursor.execute("""
    SELECT COUNT(*)
    FROM transactions
    WHERE transaction_type='EMI Payment'
    """)
    emi = cursor.fetchone()[0]

    stat_box(analytics_frame, "Deposits", deposits, "#228B22", 0, 0)
    stat_box(analytics_frame, "Withdrawals", withdrawals, "#FF8C00", 0, 1)

    stat_box(analytics_frame, "Transfers", transfers, "#1E90FF", 1, 0)
    stat_box(analytics_frame, "ATM Withdraw", atm_withdrawals, "#8A2BE2", 1, 1)

    stat_box(analytics_frame, "EMI Payments", emi, "#DC143C", 2, 0)

    cursor.execute("""
    SELECT account_no,
           transaction_type,
           amount,
           date_time
    FROM transactions
    ORDER BY id DESC
    LIMIT 5
    """)

    rows = cursor.fetchall()

    for row in rows:
        recent_box.insert(
            END,
            f"{row[0]} | {row[1]} | Rs.{row[2]} | {row[3]}"
        )

    recent_box.config(state="disabled")

def generate_admin_report():

    file_name = "Bank_Admin_Report.pdf"

    doc = SimpleDocTemplate(file_name)

    styles = getSampleStyleSheet()

    content = []


    cursor.execute("SELECT COUNT(*) FROM accounts")
    customers = cursor.fetchone()[0]


    cursor.execute("SELECT SUM(balance) FROM accounts")
    balance = cursor.fetchone()[0]

    if balance is None:
        balance = 0


    cursor.execute("SELECT COUNT(*) FROM atm_cards")
    cards = cursor.fetchone()[0]


    cursor.execute("""
    SELECT COUNT(*)
    FROM atm_cards
    WHERE status='Blocked'
    """)

    blocked = cursor.fetchone()[0]


    cursor.execute("SELECT COUNT(*) FROM transactions")
    transactions = cursor.fetchone()[0]


    report = f"""
    BANK MANAGEMENT SYSTEM<br/><br/>

    ADMIN REPORT<br/><br/>

    Total Customers : {customers}<br/><br/>

    Total Bank Balance : Rs.{balance}<br/><br/>

    Total ATM Cards : {cards}<br/><br/>

    Blocked ATM Cards : {blocked}<br/><br/>

    Total Transactions : {transactions}<br/><br/>

    Generated Date : {datetime.now()}
    """


    content.append(
        Paragraph(report, styles["Normal"])
    )

    doc.build(content)


    messagebox.showinfo(
        "Report",
        "Admin PDF Report Generated Successfully"
    )      

def generate_pdf_receipt(account_no, transaction_type, amount, balance):

    now = datetime.now()

    file_name = f"ATM_Receipt_{account_no}.pdf"

    doc = SimpleDocTemplate(file_name)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>BANK MANAGEMENT SYSTEM</b>", styles["Title"]))
    story.append(Paragraph("<b>ATM RECEIPT</b>", styles["Heading2"]))
    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"Account Number : {account_no}", styles["Normal"]))
    story.append(Paragraph(f"Transaction : {transaction_type}", styles["Normal"]))
    story.append(Paragraph(f"Amount : Rs.{amount:.2f}", styles["Normal"]))
    story.append(Paragraph(f"Date : {now.strftime('%d-%m-%Y')}", styles["Normal"]))
    story.append(Paragraph(f"Time : {now.strftime('%I:%M %p')}", styles["Normal"]))
    story.append(Paragraph(f"Available Balance : Rs.{balance:.2f}", styles["Normal"]))

    story.append(Paragraph("<br/>", styles["Normal"]))
    story.append(Paragraph("<b>THANK YOU - VISIT AGAIN</b>", styles["Heading3"]))

    doc.build(story)

    messagebox.showinfo(
        "PDF Receipt",
        f"PDF Receipt Saved as\n{file_name}"
    )    


def atm_receipt(account_no=None):

    acc_no = account_no

    if acc_no is None:
        acc_no = simpledialog.askinteger(
            "Account No",
            "Enter Account Number"
        )

        if not acc_no:
            messagebox.showerror(
                "Error",
                "Account number not provided"
            )
            return

    # ==========================================
    # CHECK ACCOUNT
    # ==========================================

    cursor.execute("""
        SELECT name, balance
        FROM accounts
        WHERE account_no=?
    """, (acc_no,))

    account = cursor.fetchone()

    if account is None:
        messagebox.showerror(
            "Error",
            "Account not found"
        )
        return

    balance = account[1]

    # ==========================================
    # GET LAST TRANSACTION
    # ==========================================

    cursor.execute("""
        SELECT transaction_type, amount, date_time
        FROM transactions
        WHERE account_no=?
        ORDER BY id DESC
        LIMIT 1
    """, (acc_no,))

    transaction = cursor.fetchone()

    if transaction is None:

        messagebox.showinfo(
            "ATM Receipt",
            "No transactions found for this account."
        )

        return

    transaction_type = transaction[0]
    amount = transaction[1]
    date_time = transaction[2]

    # ==========================================
    # GENERATE PDF
    # ==========================================

    generate_pdf_receipt(
        acc_no,
        transaction_type,
        amount,
        balance
    )

def search_account():

    window = Toplevel(root)
    window.title("Search Account")
    window.geometry("400x350")
    window.configure(bg="white")

    Label(
        window,
        text="SEARCH ACCOUNT",
        font=("Arial",16,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=10)

    Label(
        window,
        text="Enter Account Number",
        bg="white"
    ).pack()

    account_entry = Entry(window, width=30)
    account_entry.pack(pady=5)

    result_label = Label(
        window,
        text="",
        bg="white",
        justify=LEFT,
        font=("Arial",11)
    )
    result_label.pack(pady=15)

    atm_button = None

    def search():

        nonlocal atm_button

        if account_entry.get() == "":
            messagebox.showerror(
                "Error",
                "Enter Account Number"
            )
            return

        account_no = int(account_entry.get())

        cursor.execute("""
        SELECT account_no, name, balance,pin
        FROM accounts
        WHERE account_no=?
        """, (account_no,))

        row = cursor.fetchone()

        if row:

            atm_status = "No ATM Card"

            result_label.config(
                text=f"""
Account Number : {row[0]}

Name : {row[1]}

Balance : Rs.{row[2]}

PIN : {"*" * len(str(row[3]))}

ATM Status : {atm_status}
"""
            )

            if atm_button:
                atm_button.destroy()

            atm_button =Button(
                window,
                text="Search ATM Card",
                bg="blue",
                fg="white",
                font=("Arial",12,"bold"),
                command=lambda: search_atm_card(account_no)
            )

            atm_button.pack(pady=5)

        else:

            result_label.config(
                text="Account Not Found"
            )

    Button(
        window,
        text="Search",
        bg="green",
        fg="white",
        font=("Arial",12,"bold"),
        command=search
    ).pack(pady=10)  
         

def view_notifications(account_no):

    window = Toplevel(root)
    window.title("Notifications")
    window.geometry("550x450")
    window.configure(bg="white")

    Label(
        window,
        text="🔔 Notifications",
        font=("Arial",16,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=10)

    text = Text(window, width=65, height=18)
    text.pack(padx=10, pady=10)

    cursor.execute("""
    SELECT message, date_time
    FROM notifications
    WHERE account_no=?
    ORDER BY id DESC
    """, (account_no,))

    rows = cursor.fetchall()

    if rows:
        for row in rows:
            text.insert(
                END,
                f"{row[1]}\n{row[0]}\n"
                "--------------------------------------\n"
            )
    else:
        text.insert(END, "No Notifications Found")

    text.config(state="disabled")

    cursor.execute("""
    UPDATE notifications
    SET status='Read'
    WHERE account_no=?
    """, (account_no,))
    conn.commit()    

def atm_deposit(account_no):

    window = Toplevel(root)
    window.title("ATM Cash Deposit")
    window.geometry("400x350")
    window.configure(bg="white")

    Label(
        window,
        text="ATM CASH DEPOSIT",
        font=("Arial",16,"bold"),
        bg="white",
        fg="green"
    ).pack(pady=10)

    Label(window, text="Card Number", bg="white").pack()
    card_entry = Entry(window, width=30)
    card_entry.pack(pady=5)

    Label(window, text="ATM PIN", bg="white").pack()
    pin_entry = Entry(window, show="*", width=30)
    pin_entry.pack(pady=5)

    Label(window, text="Deposit Amount", bg="white").pack()
    amount_entry = Entry(window, width=30)
    amount_entry.pack(pady=5)   

    def deposit():
        card_no = card_entry.get()
        pin = pin_entry.get()

        if amount_entry.get() == "":
            messagebox.showerror("Error", "Enter Deposit Amount")
            return

        amount = float(amount_entry.get())

        cursor.execute("""
        SELECT status, pin
        FROM atm_cards
        WHERE account_no=? AND card_number=?
        """, (account_no, card_no))

        card = cursor.fetchone()

        if card is None:
            messagebox.showerror(
                "Error",
                "Invalid Card Number"
            )
            return

        status, db_pin = card

        if status == "Blocked":
            messagebox.showerror(
                "Blocked",
                "ATM Card is Blocked"
            )
            return

        if str(pin) != str(db_pin):
            messagebox.showerror(
                "Error",
                "Invalid ATM PIN"
            )
            return

        # Deposit Money
        cursor.execute("""
        UPDATE accounts
        SET balance = balance + ?
        WHERE account_no=?
        """, (amount, account_no))

        conn.commit()

        # Save Transaction
        cursor.execute("""
        INSERT INTO transactions
        (account_no, transaction_type, amount, date_time)
        VALUES (?, ?, ?, ?)
        """, (
            account_no,
            "ATM Deposit",
            amount,
            datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        ))

        conn.commit()

        # New Balance
        cursor.execute("""
        SELECT balance
        FROM accounts
        WHERE account_no=?
        """, (account_no,))

        new_balance = cursor.fetchone()[0]

        # Generate Receipts
        generate_atm_receipt(
            account_no,
            "ATM Deposit",
            amount,
            new_balance
        )

        generate_pdf_receipt(
            account_no,
            "ATM Deposit",
            amount,
            new_balance
        )

        messagebox.showinfo(
            "Success",
            f"Rs.{amount} Deposited Successfully"
        )

        window.destroy()  

    Button(
        window,
        text="Deposit",
        bg="green",
        fg="white",
        font=("Arial", 12, "bold"),
        width=15,
        command=deposit
    ).pack(pady=20)    


def customer_login(acc_entry, pin_entry):

    account_no = acc_entry.get()
    pin = pin_entry.get()

    if account_no == "" or pin == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    try:
        account_no = int(account_no)
    except ValueError:
        messagebox.showerror("Error", "Invalid Account Number")
        return

    cursor.execute("""
    SELECT account_no, name, balance, pin
    FROM accounts
    WHERE account_no = ? AND pin = ?
    """, (account_no, pin))

    account = cursor.fetchone()

    if account:
        open_customer_dashboard(account)
    else:
        messagebox.showerror("Login Failed", "Invalid Account Number or PIN")


def admin_login(username_entry, password_entry, admin_window):
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please fill all fields")
        return

    if username == "admin" and password == "admin123":
        admin_window.destroy()
        open_admin_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def view_all_accounts():

    window = Toplevel(root)
    window.title("All Accounts")
    window.geometry("700x450")
    window.configure(bg="white")

    Label(
        window,
        text="ALL CUSTOMER ACCOUNTS",
        font=("Arial",18,"bold"),
        bg="white",
        fg="green"
    ).pack(pady=15)

    text = Text(window, width=90, height=18)
    text.pack()

    cursor.execute("""
    SELECT account_no, name, balance
    FROM accounts
    ORDER BY account_no
    """)

    records = cursor.fetchall()

    if not records:
        text.insert(END, "No Accounts Found")
        return

    text.insert(
        END,
        "Account No\tName\t\tBalance\n"
    )
    text.insert(
        END,
        "="*60 + "\n"
    )

    for account in records:
        text.insert(
            END,
            f"{account[0]}\t{account[1]}\t\tRs. {account[2]}\n"
        )

    text.config(state="disabled")   

def delete_account():

    window = Toplevel(root)
    window.title("Delete Account")
    window.geometry("400x250")
    window.configure(bg="white")

    Label(
        window,
        text="Delete Account",
        font=("Arial",16,"bold"),
        bg="white",
        fg="red"
    ).pack(pady=15)

    Label(
        window,
        text="Enter Account Number",
        bg="white",
        font=("Arial",12)
    ).pack()

    account_entry = Entry(
        window,
        font=("Arial",12),
        width=25
    )
    account_entry.pack(pady=10)

    def delete():

        acc = account_entry.get()

        if acc == "":
            messagebox.showerror("Error", "Enter Account Number")
            return

        cursor.execute(
            "SELECT * FROM accounts WHERE account_no=?",
            (acc,)
        )

        if cursor.fetchone() is None:
            messagebox.showerror("Error", "Account Not Found")
            return

        confirm = messagebox.askyesno(
            "Confirm",
            "Are you sure you want to delete this account?"
        )

        if confirm:

            cursor.execute(
                "DELETE FROM accounts WHERE account_no=?",
                (acc,)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                "Account Deleted Successfully"
            )

            window.destroy()

    Button(
        window,
        text="Delete",
        bg="red",
        fg="white",
        font=("Arial",12,"bold"),
        command=delete
    ).pack(pady=20)  

def view_all_transactions():

    window = Toplevel(root)
    window.title("All Transactions")
    window.geometry("900x550")
    window.configure(bg="white")


    # ==========================================
    # TITLE
    # ==========================================

    Label(
        window,
        text="📜 ALL TRANSACTIONS",
        font=("Arial",18,"bold"),
        bg="white",
        fg="purple"
    ).pack(pady=10)


    # ==========================================
    # FRAME
    # ==========================================

    table_frame = Frame(
        window,
        bg="white"
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=5
    )


    # ==========================================
    # TEXT AREA
    # ==========================================

    text = Text(
        table_frame,
        width=110,
        height=25,
        font=("Consolas",10),
        wrap="none"
    )

    text.pack(
        side="left",
        fill="both",
        expand=True
    )


    # ==========================================
    # SCROLLBAR
    # ==========================================

    scrollbar = Scrollbar(
        table_frame,
        orient="vertical",
        command=text.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    text.config(
        yscrollcommand=scrollbar.set
    )


    # ==========================================
    # GET TRANSACTIONS
    # ==========================================

    cursor.execute("""
        SELECT
            account_no,
            transaction_type,
            amount,
            date_time
        FROM transactions
        ORDER BY id DESC
    """)

    records = cursor.fetchall()


    # ==========================================
    # NO RECORDS
    # ==========================================

    if not records:

        text.insert(
            END,
            "\n\n              No Transactions Found"
        )

        text.config(state="disabled")

        return


    # ==========================================
    # HEADER
    # ==========================================

    text.insert(
        END,
        f"{'ACCOUNT':<12}"
        f"{'TRANSACTION TYPE':<28}"
        f"{'AMOUNT':<18}"
        f"{'DATE & TIME':<25}\n"
    )

    text.insert(
        END,
        "=" * 83 + "\n"
    )


    # ==========================================
    # TRANSACTION RECORDS
    # ==========================================

    for row in records:

        account_no = row[0]
        transaction_type = row[1]
        amount = float(row[2])
        date_time = row[3]

        text.insert(
            END,
            f"{str(account_no):<12}"
            f"{str(transaction_type):<28}"
            f"Rs.{amount:<15.2f}"
            f"{str(date_time):<25}\n"
        )


    # ==========================================
    # DISABLE EDITING
    # ==========================================

    text.config(
        state="disabled"
    )  

def admin_fixed_deposit_management():

    window = Toplevel(root)
    window.title("Fixed Deposit Management")
    window.geometry("950x650")
    window.configure(bg="white")

    Label(
        window,
        text="FIXED DEPOSIT MANAGEMENT",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="darkgreen"
    ).pack(pady=15)

    # ==========================================
    # SEARCH
    # ==========================================

    search_frame = Frame(window, bg="white")
    search_frame.pack(pady=5)

    Label(
        search_frame,
        text="Account No:",
        font=("Arial", 11, "bold"),
        bg="white"
    ).pack(side="left", padx=5)

    search_entry = Entry(
        search_frame,
        font=("Arial", 11),
        width=15
    )
    search_entry.pack(side="left", padx=5)

    # ==========================================
    # FD LIST
    # ==========================================

    text = Text(
        window,
        width=110,
        height=23,
        font=("Courier New", 10)
    )

    text.pack(
        padx=10,
        pady=10
    )

    # ==========================================
    # LOAD FD
    # ==========================================

    def load_fds():

        text.config(state="normal")
        text.delete("1.0", END)

        account_no = search_entry.get().strip()

        if account_no == "":

            cursor.execute("""
                SELECT fd_id,
                       account_no,
                       amount,
                       years,
                       interest_rate,
                       maturity_amount,
                       status
                FROM fixed_deposits
                ORDER BY fd_id DESC
            """)

        else:

            try:
                account_no = int(account_no)

            except ValueError:

                messagebox.showerror(
                    "Error",
                    "Enter valid Account Number"
                )

                return

            cursor.execute("""
                SELECT fd_id,
                       account_no,
                       amount,
                       years,
                       interest_rate,
                       maturity_amount,
                       status
                FROM fixed_deposits
                WHERE account_no=?
                ORDER BY fd_id DESC
            """, (account_no,))

        records = cursor.fetchall()

        if not records:

            text.insert(
                END,
                "No Fixed Deposit Records Found"
            )

            text.config(state="disabled")

            return

        text.insert(
            END,
            "FD ID\tAccount\tAmount\tYears\tRate\tMaturity\tStatus\n"
        )

        text.insert(
            END,
            "=" * 105 + "\n"
        )

        for row in records:

            text.insert(
                END,
                f"{row[0]}\t"
                f"{row[1]}\t"
                f"Rs.{row[2]:.2f}\t"
                f"{row[3]}\t"
                f"{row[4]}%\t"
                f"Rs.{row[5]:.2f}\t"
                f"{row[6]}\n"
            )

        text.config(state="disabled")

    # ==========================================
    # SEARCH BUTTON
    # ==========================================

    Button(
        search_frame,
        text="🔍 Search",
        bg="#0B5ED7",
        fg="white",
        font=("Arial", 11, "bold"),
        command=load_fds
    ).pack(side="left", padx=5)

    # ==========================================
    # VIEW ALL BUTTON
    # ==========================================

    Button(
        search_frame,
        text="📋 View All",
        bg="darkgreen",
        fg="white",
        font=("Arial", 11, "bold"),
        command=lambda: [
            search_entry.delete(0, END),
            load_fds()
        ]
    ).pack(side="left", padx=5)

    # ==========================================
    # CLOSE / WITHDRAW FD
    # ==========================================

    Label(
        window,
        text="Enter FD ID to Close / Withdraw",
        font=("Arial", 11, "bold"),
        bg="white"
    ).pack(pady=(5, 2))

    fd_id_entry = Entry(
        window,
        font=("Arial", 11),
        width=15
    )

    fd_id_entry.pack(pady=5)

    def close_fd():

        fd_id_text = fd_id_entry.get().strip()

        if fd_id_text == "":

            messagebox.showerror(
                "Error",
                "Enter FD ID"
            )

            return

        try:
            fd_id = int(fd_id_text)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid FD ID"
            )

            return

        # ======================================
        # GET FD
        # ======================================

        cursor.execute("""
            SELECT account_no,
                   amount,
                   maturity_amount,
                   status
            FROM fixed_deposits
            WHERE fd_id=?
        """, (fd_id,))

        fd = cursor.fetchone()

        if not fd:

            messagebox.showerror(
                "Error",
                "Fixed Deposit not found"
            )

            return

        account_no = fd[0]
        amount = float(fd[1])
        maturity_amount = float(fd[2])
        status = fd[3]

        # ======================================
        # CHECK STATUS
        # ======================================

        if status != "Active":

            messagebox.showerror(
                "Error",
                f"FD is already {status}"
            )

            return

        # ======================================
        # CONFIRM
        # ======================================

        confirm = messagebox.askyesno(
            "Confirm FD Withdrawal",
            f"FD ID : {fd_id}\n"
            f"Account : {account_no}\n"
            f"Maturity Amount : Rs. {maturity_amount:.2f}\n\n"
            f"Close this Fixed Deposit?"
        )

        if not confirm:
            return

        # ======================================
        # CREDIT MATURITY AMOUNT
        # ======================================

        cursor.execute("""
            UPDATE accounts
            SET balance = balance + ?
            WHERE account_no=?
        """, (
            maturity_amount,
            account_no
        ))

        # ======================================
        # CLOSE FD
        # ======================================

        cursor.execute("""
            UPDATE fixed_deposits
            SET status='Closed'
            WHERE fd_id=?
        """, (fd_id,))

        # ======================================
        # TRANSACTION
        # ======================================

        date_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

        cursor.execute("""
            INSERT INTO transactions(
                account_no,
                transaction_type,
                amount,
                date_time
            )
            VALUES(?,?,?,?)
        """, (
            account_no,
            "FD Withdraw",
            maturity_amount,
            date_time
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"FD Withdrawn Successfully!\n\n"
            f"Account : {account_no}\n"
            f"Amount Credited : Rs. {maturity_amount:.2f}"
        )

        fd_id_entry.delete(0, END)

        load_fds()

    # ==========================================
    # CLOSE FD BUTTON
    # ==========================================

    Button(
        window,
        text="🔒 Close / Withdraw FD",
        bg="#DC3545",
        fg="white",
        font=("Arial", 12, "bold"),
        width=25,
        command=close_fd
    ).pack(pady=8)

    # ==========================================
    # FD SUMMARY
    # ==========================================

    def fd_summary():

        cursor.execute("""
            SELECT COUNT(*)
            FROM fixed_deposits
        """)

        total_fd = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM fixed_deposits
            WHERE status='Active'
        """)

        active_fd = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM fixed_deposits
            WHERE status='Closed'
        """)

        closed_fd = cursor.fetchone()[0]

        cursor.execute("""
            SELECT SUM(amount)
            FROM fixed_deposits
            WHERE status='Active'
        """)

        active_amount = cursor.fetchone()[0]

        if active_amount is None:
            active_amount = 0

        cursor.execute("""
            SELECT SUM(maturity_amount)
            FROM fixed_deposits
            WHERE status='Active'
        """)

        active_maturity = cursor.fetchone()[0]

        if active_maturity is None:
            active_maturity = 0

        messagebox.showinfo(
            "FD Summary",
            f"Total Fixed Deposits : {total_fd}\n\n"
            f"Active FD : {active_fd}\n"
            f"Closed FD : {closed_fd}\n\n"
            f"Active Deposit Amount : "
            f"Rs. {active_amount:.2f}\n\n"
            f"Active Maturity Amount : "
            f"Rs. {active_maturity:.2f}"
        )

    # ==========================================
    # SUMMARY BUTTON
    # ==========================================

    Button(
        window,
        text="📊 FD Summary",
        bg="#6A1B9A",
        fg="white",
        font=("Arial", 12, "bold"),
        width=25,
        command=fd_summary
    ).pack(pady=5)

    # ==========================================
    # CLOSE WINDOW
    # ==========================================

    Button(
        window,
        text="Close",
        bg="black",
        fg="white",
        font=("Arial", 11, "bold"),
        width=15,
        command=window.destroy
    ).pack(pady=10)

    # Load all FD initially
    load_fds()



def view_loan_requests():

    window = Toplevel(root)
    window.title("Loan Requests")
    window.geometry("800x500")
    window.configure(bg="white")


    Label(
        window,
        text="ALL LOAN REQUESTS",
        font=("Arial",18,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=15)


    text = Text(
        window,
        width=100,
        height=20
    )

    text.pack()


    cursor.execute("""
    SELECT 
    loan_id,
    account_no,
    loan_type,
    amount,
    interest,
    months,
    emi,
    status,
    date

    FROM loans
    ORDER BY loan_id DESC
    """)


    loans = cursor.fetchall()


    if not loans:

        text.insert(
            END,
            "No Loan Requests Found"
        )

        return


    for loan in loans:

        frame = Frame(window, bg="white")
        frame.pack(pady=5)

        text.insert(
            END,
            f"""
Loan ID       : {loan[0]}
Account No    : {loan[1]}
Loan Type     : {loan[2]}
Amount        : Rs. {loan[3]}
Interest      : {loan[4]}%
Months        : {loan[5]}
EMI           : Rs. {loan[6]:.2f}
Status        : {loan[7]}
Date          : {loan[8]}

--------------------------------------

"""
        )

        Button(
            frame,
            text="Approve",
            bg="green",
            fg="white",
            command=lambda id=loan[0]: update_loan_status(id, "Approved")
        ).pack(side=LEFT, padx=10)

        Button(
            frame,
            text="Reject",
            bg="red",
            fg="white",
            command=lambda id=loan[0]: update_loan_status(id, "Rejected")
        ).pack(side=LEFT, padx=10)

    text.config(state="disabled")

def update_loan_status(loan_id, status):

    cursor.execute("""
    SELECT account_no, amount
    FROM loans
    WHERE loan_id=?
    """,
    (loan_id,)
    )

    loan = cursor.fetchone()


    if loan is None:
        messagebox.showerror(
            "Error",
            "Loan Not Found"
        )
        return


    account_no = loan[0]
    amount = loan[1]


    cursor.execute("""
    UPDATE loans
    SET status=?
    WHERE loan_id=?
    """,
    (
        status,
        loan_id
    ))


    if status == "Approved":

        cursor.execute("""
        UPDATE accounts
        SET balance = balance + ?
        WHERE account_no=?
        """,
        (
            amount,
            account_no
        ))


    conn.commit()


    messagebox.showinfo(
        "Success",
        f"Loan {status}"
    )
def bank_summary():

    # ==========================
    # TOTAL ACCOUNTS
    # ==========================

    cursor.execute("""
        SELECT COUNT(*)
        FROM accounts
    """)
    total_accounts = cursor.fetchone()[0]


    # ==========================
    # TOTAL BANK BALANCE
    # ==========================

    cursor.execute("""
        SELECT SUM(balance)
        FROM accounts
    """)
    total_balance = cursor.fetchone()[0]

    if total_balance is None:
        total_balance = 0


    # ==========================
    # TOTAL TRANSACTIONS
    # ==========================

    cursor.execute("""
        SELECT COUNT(*)
        FROM transactions
    """)
    total_transactions = cursor.fetchone()[0]


    # ==========================
    # TOTAL LOANS
    # ==========================

    cursor.execute("""
        SELECT COUNT(*)
        FROM loans
    """)
    total_loans = cursor.fetchone()[0]


    # ==========================
    # PENDING LOANS
    # ==========================

    cursor.execute("""
        SELECT COUNT(*)
        FROM loans
        WHERE status='Pending'
    """)
    pending_loans = cursor.fetchone()[0]


    # ==========================
    # APPROVED LOANS
    # ==========================

    cursor.execute("""
        SELECT COUNT(*)
        FROM loans
        WHERE status='Approved'
    """)
    approved_loans = cursor.fetchone()[0]


    # ==========================
    # ATM CARDS
    # ==========================

    cursor.execute("""
        SELECT COUNT(*)
        FROM atm_cards
    """)
    total_atm_cards = cursor.fetchone()[0]


    # ==========================
    # FIXED DEPOSITS
    # ==========================

    cursor.execute("""
        SELECT COUNT(*)
        FROM fixed_deposits
    """)
    total_fds = cursor.fetchone()[0]


    # ==========================
    # SHOW SUMMARY
    # ==========================

    messagebox.showinfo(
        "Bank Summary",
        f"""🏦 BANK SUMMARY

Total Accounts      : {total_accounts}

Total Bank Balance  : Rs. {total_balance:.2f}

Total Transactions  : {total_transactions}

Total Loans         : {total_loans}

Pending Loans       : {pending_loans}

Approved Loans      : {approved_loans}

Total ATM Cards     : {total_atm_cards}

Total Fixed Deposits: {total_fds}
"""
    )

def create_account_admin():

    window = Toplevel(root)
    window.title("Create Account")
    window.geometry("400x400")
    window.configure(bg="white")

    Label(window,text="Create New Account",
          font=("Arial",16,"bold"),
          bg="white",
          fg="green").pack(pady=15)

    Label(window,text="Name",bg="white").pack()
    name_entry = Entry(window,font=("Arial",12))
    name_entry.pack(pady=5)

    Label(window,text="Opening Balance",bg="white").pack()
    balance_entry = Entry(window,font=("Arial",12))
    balance_entry.pack(pady=5)

    Label(window,text="PIN",bg="white").pack()
    pin_entry = Entry(window,font=("Arial",12),show="*")
    pin_entry.pack(pady=5)

    def save():

        name = name_entry.get().strip()
        balance = balance_entry.get().strip()
        pin = pin_entry.get().strip()

        if name=="" or balance=="" or pin=="":
            messagebox.showerror("Error","Fill all fields")
            return

        try:
            balance=float(balance)
        except:
            messagebox.showerror("Error","Invalid Balance")
            return

        cursor.execute("""
        INSERT INTO accounts(name,balance,pin)
        VALUES(?,?,?)
        """,(name,balance,pin))

        conn.commit()

        account_no = cursor.lastrowid

        messagebox.showinfo(
            "Success",
            f"Account Created Successfully\n\nAccount Number : {account_no}"
        )

        window.destroy()

    Button(
        window,
        text="Create",
        bg="green",
        fg="white",
        font=("Arial",12,"bold"),
        command=save
    ).pack(pady=20)  

def edit_customer():

    window = Toplevel(root)
    window.title("Edit Customer")
    window.geometry("400x450")
    window.configure(bg="white")

    Label(
        window,
        text="EDIT CUSTOMER",
        font=("Arial",18,"bold"),
        bg="white",
        fg="green"
    ).pack(pady=15)

    Label(window,text="Account Number",bg="white").pack()
    acc_entry = Entry(window,font=("Arial",12))
    acc_entry.pack(pady=5)

    Label(window,text="New Name",bg="white").pack()
    name_entry = Entry(window,font=("Arial",12))
    name_entry.pack(pady=5)

    Label(window,text="New PIN",bg="white").pack()
    pin_entry = Entry(window,font=("Arial",12))
    pin_entry.pack(pady=5)           

    def save():

        account_no = acc_entry.get()
        name = name_entry.get()
        pin = pin_entry.get()

        if account_no == "" or name == "" or pin == "":
            messagebox.showerror("Error","Fill all fields")
            return

        cursor.execute("""
        UPDATE accounts
        SET name=?, pin=?
        WHERE account_no=?
        """,(name,pin,account_no))

        conn.commit()

        if cursor.rowcount == 0:
            messagebox.showerror("Error","Account Not Found")
        else:
            messagebox.showinfo("Success","Customer Updated Successfully")
            window.destroy()

    Button(
        window,
        text="Save Changes",
        font=("Arial",12,"bold"),
        bg="green",
        fg="white",
        command=save
    ).pack(pady=20) 


def backup_database():

    try:

        shutil.copy("bank.db", "bank_backup.db")

        messagebox.showinfo(
            "Success",
            "Database Backup Created Successfully!"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )    

def restore_database():

    try:

        shutil.copy("bank_backup.db", "bank.db")

        messagebox.showinfo(
            "Success",
            "Database Restored Successfully!"
        )

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )

def interest_calculator():

    window = Toplevel(root)
    window.title("Interest Calculator")
    window.geometry("400x350")
    window.configure(bg="white")

    Label(
        window,
        text="INTEREST CALCULATOR",
        font=("Arial",18,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=15)

    Label(
        window,
        text="Account Number",
        bg="white",
        font=("Arial",12)
    ).pack()

    account_entry = Entry(
        window,
        font=("Arial",12)
    )
    account_entry.pack(pady=5) 

    Label(window, text="Interest Rate (%)", bg="white").pack()
    rate_entry = Entry(window, font=("Arial",12))
    rate_entry.pack(pady=5)

    Label(window, text="Years", bg="white").pack()
    years_entry = Entry(window, font=("Arial",12))
    years_entry.pack(pady=5)

    result = Label(
        window,
        text="",
        bg="white",
        font=("Arial",12,"bold"),
        fg="green"
    )
    result.pack(pady=15)

    

    def calculate():

        try:
            account_no = account_entry.get()

            cursor.execute("""
            SELECT balance
            FROM accounts
            WHERE account_no = ?
            """, (account_no,))

            data = cursor.fetchone()

            if data is None:
                messagebox.showerror(
                    "Error",
                    "Account Not Found"
                )
                return

            p = data[0]
            r = float(rate_entry.get())
            t = float(years_entry.get())

            interest = (p * r * t) / 100
            total = p + interest

            result.config(
                text=f"""
            Current Balance : Rs. {p:.2f}

            Interest : Rs. {interest:.2f}

            Total Amount : Rs. {total:.2f} 
            """
            )

        except ValueError:
            messagebox.showerror("Error", "Enter valid numbers")

    Button(
        window,
        text="Calculate",
        bg="green",
        fg="white",
        font=("Arial",12,"bold"),
        command=calculate
    ).pack(pady=10)

def fixed_deposit(account_no):

    window = Toplevel(root)
    window.title("Fixed Deposit")
    window.geometry("450x420")
    window.configure(bg="white")

    Label(
        window,
        text="FIXED DEPOSIT",
        font=("Arial",18,"bold"),
        bg="white",
        fg="darkgreen"
    ).pack(pady=15)

    Label(window, text="Deposit Amount", bg="white").pack()

    amount_entry = Entry(window, font=("Arial",12))
    amount_entry.pack(pady=5)

    Label(window, text="Years", bg="white").pack()

    years_entry = Entry(window, font=("Arial",12))
    years_entry.pack(pady=5)

    def create_fd():

        try:
            amount = float(amount_entry.get())
            years = int(years_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Enter valid values")
            return

        if amount <= 0 or years <= 0:
            messagebox.showerror("Error", "Invalid Amount or Years")
            return

        interest_rate = 8.0

        maturity_amount = amount + ((amount * interest_rate * years) / 100)

        # Check balance
        cursor.execute("""
        SELECT balance
        FROM accounts
        WHERE account_no=?
        """, (account_no,))

        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Account not found")
            return

        balance = result[0]

        if amount > balance:
            messagebox.showerror(
                "Error",
                "Insufficient Balance"
            )
            return

        # Deduct amount
        cursor.execute("""
        UPDATE accounts
        SET balance = balance - ?
        WHERE account_no=?
        """, (amount, account_no))

        cursor.execute("""
        INSERT INTO fixed_deposits
        (account_no, amount, years, interest_rate, maturity_amount, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            account_no,
            amount,
            years,
            interest_rate,
            maturity_amount,
            "Active"
        ))

        conn.commit()

        cursor.execute("""
        INSERT INTO transactions
        (account_no, transaction_type, amount, date_time)
        VALUES (?, ?, ?, ?)
        """, (
            account_no,
            "FD Created",
            amount,
            datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"""Fixed Deposit Created Successfully!

Deposit : Rs. {amount}

Interest : {interest_rate}%

Maturity Amount : Rs. {maturity_amount:.2f}
"""
        )

        window.destroy()

    Button(
        window,
        text="Create FD",
        bg="green",
        fg="white",
        font=("Arial",12,"bold"),
        command=create_fd
    ).pack(pady=20)   

def view_my_fd(account_no):

    window = Toplevel(root)
    window.title("My Fixed Deposits")
    window.geometry("700x400")
    window.configure(bg="white")

    Label(
        window,
        text="MY FIXED DEPOSITS",
        font=("Arial",18,"bold"),
        bg="white",
        fg="darkgreen"
    ).pack(pady=15)

    text = Text(window, width=90, height=18)
    text.pack()

    cursor.execute("""
    SELECT fd_id,
           amount,
           years,
           interest_rate,
           maturity_amount,
           status
    FROM fixed_deposits
    WHERE account_no = ?
    ORDER BY fd_id DESC
    """, (account_no,))

    records = cursor.fetchall()

    if not records:
        text.insert(END, "No Fixed Deposits Found")
        text.config(state="disabled")
        return

    text.insert(
        END,
        "FD ID\tAmount\tYears\tRate\tMaturity\tStatus\n"
    )

    text.insert(
        END,
        "=" * 80 + "\n"
    )

    for fd in records:

        text.insert(
            END,
            f"{fd[0]}\tRs.{fd[1]}\t{fd[2]}\t{fd[3]}%\tRs.{fd[4]}\t{fd[5]}\n"
        )

    text.config(state="disabled")   
        

def close_fixed_deposit(account_no):

    window = Toplevel(root)
    window.title("Close Fixed Deposit")
    window.geometry("400x320")
    window.configure(bg="white")

    Label(
        window,
        text="CLOSE FIXED DEPOSIT",
        font=("Arial",18,"bold"),
        bg="white",
        fg="red"
    ).pack(pady=15)

    Label(
        window,
        text="Enter FD ID",
        bg="white",
        font=("Arial",12)
    ).pack()

    fd_entry = Entry(window, font=("Arial",12))
    fd_entry.pack(pady=10)

    def close_fd():
        print("close_fd called")
        fd_id = fd_entry.get()

        print("FD ID =", fd_id)

        print("Account No =", account_no)

        cursor.execute("""
        SELECT fd_id, account_no, status
        FROM fixed_deposits
        WHERE fd_id = ?
        """, (fd_id,))

        print("FD Record =", cursor.fetchone())

        if fd_id == "":
            messagebox.showerror(
                "Error",
                "Enter FD ID"
            )
            return

        cursor.execute("""
        SELECT maturity_amount, status
        FROM fixed_deposits
        WHERE fd_id=? AND account_no=?
        """, (fd_id, account_no))

        fd = cursor.fetchone()

        if fd is None:
            messagebox.showerror(
                "Error",
                "FD Not Found"
            )
            return

        if fd[1] == "Closed":
            messagebox.showerror(
                "Error",
                "FD Already Closed"
            )
            return

        maturity_amount = fd[0]

        cursor.execute("""
        UPDATE accounts
        SET balance = balance + ?
        WHERE account_no = ?
        """, (maturity_amount, account_no))

        cursor.execute("""
        UPDATE fixed_deposits
        SET status = 'Closed'
        WHERE fd_id = ? AND account_no = ?
        """, (fd_id, account_no))

        conn.commit()

        print("Saving FD Closed transaction...")

        cursor.execute("""
        INSERT INTO transactions
        (account_no, transaction_type, amount, date_time)
        VALUES (?, ?, ?, ?)
        """, (
            account_no,
            "FD Closed",
            maturity_amount,
            datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        ))

        conn.commit()


        cursor.execute("""
        SELECT *
        FROM transactions
        WHERE account_no = ?
        ORDER BY id DESC
        LIMIT 5
        """, (account_no,))

        print(cursor.fetchall())

        print("FD Closed transaction saved.")

        messagebox.showinfo(
            "Success",
            "FD Closed Successfully"
        )

    Button(
        window,
        text="Close FD",
        bg="red",
        fg="white",
        font=("Arial",12,"bold"),
        command=close_fd
    ).pack(pady=20)    

def admin_fd_management():

    fd_window = Toplevel(root)
    fd_window.title("Fixed Deposit Management")
    fd_window.geometry("1000x650")
    fd_window.configure(bg="white")

    # ==========================================
    # TITLE
    # ==========================================

    Label(
        fd_window,
        text="🏦 FIXED DEPOSIT MANAGEMENT",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="darkgreen"
    ).pack(pady=15)

    # ==========================================
    # SEARCH FRAME
    # ==========================================

    search_frame = Frame(
        fd_window,
        bg="white"
    )

    search_frame.pack(pady=5)

    Label(
        search_frame,
        text="Search Account No:",
        font=("Arial", 11, "bold"),
        bg="white"
    ).pack(side="left", padx=5)

    search_entry = Entry(
        search_frame,
        font=("Arial", 11),
        width=20
    )

    search_entry.pack(side="left", padx=5)

    # ==========================================
    # FD LIST FRAME
    # ==========================================

    list_frame = Frame(
        fd_window,
        bg="white"
    )

    list_frame.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=10
    )

    # ==========================================
    # SCROLLBAR
    # ==========================================

    scrollbar = Scrollbar(
        list_frame,
        orient="vertical"
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ==========================================
    # LISTBOX
    # ==========================================

    fd_list = Listbox(
        list_frame,
        font=("Arial", 11),
        yscrollcommand=scrollbar.set,
        width=115,
        height=20
    )

    fd_list.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.config(
        command=fd_list.yview
    )

    # ==========================================
    # STORE FD DATA
    # ==========================================

    fd_data = []

    # ==========================================
    # LOAD FD DATA
    # ==========================================

    def load_fds():

        fd_list.delete(0, END)

        fd_data.clear()

        search_value = search_entry.get().strip()

        if search_value:

            cursor.execute("""
                SELECT
                    f.fd_id,
                    f.account_no,
                    a.name,
                    f.amount,
                    f.years,
                    f.interest_rate,
                    f.maturity_amount,
                    f.status
                FROM fixed_deposits f
                LEFT JOIN accounts a
                    ON f.account_no = a.account_no
                WHERE CAST(f.account_no AS TEXT) LIKE ?
                ORDER BY f.fd_id DESC
            """, (
                "%" + search_value + "%",
            ))

        else:

            cursor.execute("""
                SELECT
                    f.fd_id,
                    f.account_no,
                    a.name,
                    f.amount,
                    f.years,
                    f.interest_rate,
                    f.maturity_amount,
                    f.status
                FROM fixed_deposits f
                LEFT JOIN accounts a
                    ON f.account_no = a.account_no
                ORDER BY f.fd_id DESC
            """)

        rows = cursor.fetchall()

        if not rows:

            fd_list.insert(
                END,
                "No Fixed Deposit Found"
            )

            return

        # ======================================
        # HEADER
        # ======================================

        header = (
            f"{'FD ID':<8}"
            f"{'Account':<12}"
            f"{'Customer':<22}"
            f"{'Amount':<15}"
            f"{'Years':<8}"
            f"{'Rate':<10}"
            f"{'Maturity':<15}"
            f"{'Status':<12}"
        )

        fd_list.insert(
            END,
            header
        )

        fd_list.insert(
            END,
            "-" * 110
        )

        # ======================================
        # DATA
        # ======================================

        for row in rows:

            fd_data.append(row)

            fd_id = row[0]
            account_no = row[1]
            customer_name = row[2] if row[2] else "Unknown"
            amount = float(row[3])
            years = row[4]
            rate = float(row[5])
            maturity = float(row[6])
            status = row[7]

            line = (
                f"{str(fd_id):<8}"
                f"{str(account_no):<12}"
                f"{str(customer_name)[:20]:<22}"
                f"{'Rs.' + format(amount, '.2f'):<15}"
                f"{str(years):<8}"
                f"{str(rate) + '%':<10}"
                f"{'Rs.' + format(maturity, '.2f'):<15}"
                f"{str(status):<12}"
            )

            fd_list.insert(
                END,
                line
            )

    # ==========================================
    # SEARCH BUTTON
    # ==========================================

    # ==========================================
    # VIEW DETAILS
    # ==========================================

    def view_details():

        selected = fd_list.curselection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a Fixed Deposit"
            )

            return

        index = selected[0]

        # Ignore header
        if index < 2:

            messagebox.showerror(
                "Error",
                "Please select a Fixed Deposit"
            )

            return

        data_index = index - 2

        if data_index >= len(fd_data):

            return

        fd = fd_data[data_index]

        fd_id = fd[0]
        account_no = fd[1]
        customer_name = fd[2] if fd[2] else "Unknown"
        amount = float(fd[3])
        years = fd[4]
        rate = float(fd[5])
        maturity = float(fd[6])
        status = fd[7]

        details_window = Toplevel(fd_window)

        details_window.title("FD Details")

        details_window.geometry(
            "450x500"
        )

        details_window.configure(
            bg="white"
        )

        Label(
            details_window,
            text="🏦 FIXED DEPOSIT DETAILS",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="darkgreen"
        ).pack(pady=20)

        details_text = f"""
FD ID              : {fd_id}

Account Number     : {account_no}

Customer Name      : {customer_name}

Deposit Amount     : Rs. {amount:.2f}

Duration           : {years} Years

Interest Rate      : {rate:.2f}%

Maturity Amount    : Rs. {maturity:.2f}

Status             : {status}
"""

        Label(
            details_window,
            text=details_text,
            font=("Arial", 12),
            bg="white",
            justify=LEFT
        ).pack(
            pady=10,
            padx=20
        )

        Button(
            details_window,
            text="Close",
            bg="black",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            command=details_window.destroy
        ).pack(pady=20)

    # ==========================================
    # CLOSE / WITHDRAW FD
    # ==========================================

    def close_fd():

        selected = fd_list.curselection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a Fixed Deposit"
            )

            return

        index = selected[0]

        if index < 2:

            messagebox.showerror(
                "Error",
                "Please select a Fixed Deposit"
            )

            return

        data_index = index - 2

        if data_index >= len(fd_data):

            return

        fd = fd_data[data_index]

        fd_id = fd[0]
        account_no = fd[1]
        maturity_amount = float(fd[6])
        status = fd[7]

        if status != "Active":

            messagebox.showerror(
                "FD",
                f"This FD is already {status}"
            )

            return

        confirm = messagebox.askyesno(
            "Close Fixed Deposit",
            f"Are you sure you want to close FD #{fd_id}?\n\n"
            f"Account: {account_no}\n"
            f"Maturity Amount: Rs. {maturity_amount:.2f}"
        )

        if not confirm:

            return

        # ======================================
        # CREDIT MATURITY AMOUNT
        # ======================================

        cursor.execute("""
            UPDATE accounts
            SET balance = balance + ?
            WHERE account_no=?
        """, (
            maturity_amount,
            account_no
        ))

        # ======================================
        # CHECK ACCOUNT UPDATE
        # ======================================

        if cursor.rowcount == 0:

            conn.rollback()

            messagebox.showerror(
                "Error",
                "Account not found"
            )

            return

        # ======================================
        # UPDATE FD STATUS
        # ======================================

        cursor.execute("""
            UPDATE fixed_deposits
            SET status='Closed'
            WHERE fd_id=?
            AND account_no=?
            AND status='Active'
        """, (
            fd_id,
            account_no
        ))

        # ======================================
        # TRANSACTION
        # ======================================

        date_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

        cursor.execute("""
            INSERT INTO transactions(
                account_no,
                transaction_type,
                amount,
                date_time
            )
            VALUES(?,?,?,?)
        """, (
            account_no,
            "FD Closed",
            maturity_amount,
            date_time
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"Fixed Deposit Closed Successfully!\n\n"
            f"FD ID: {fd_id}\n"
            f"Amount Credited: Rs. {maturity_amount:.2f}"
        )

        load_fds()

    # ==========================================
    # FD SUMMARY
    # ==========================================

    def fd_summary():

        cursor.execute("""
            SELECT COUNT(*)
            FROM fixed_deposits
        """)

        total_fd = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM fixed_deposits
            WHERE status='Active'
        """)

        active_fd = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM fixed_deposits
            WHERE status='Closed'
        """)

        closed_fd = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0)
            FROM fixed_deposits
            WHERE status='Active'
        """)

        active_amount = float(
            cursor.fetchone()[0]
        )

        cursor.execute("""
            SELECT COALESCE(SUM(maturity_amount), 0)
            FROM fixed_deposits
            WHERE status='Active'
        """)

        active_maturity = float(
            cursor.fetchone()[0]
        )

        summary_window = Toplevel(fd_window)

        summary_window.title(
            "FD Summary"
        )

        summary_window.geometry(
            "450x420"
        )

        summary_window.configure(
            bg="white"
        )

        Label(
            summary_window,
            text="📊 FD SUMMARY",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="darkgreen"
        ).pack(pady=20)

        summary_text = f"""
Total Fixed Deposits : {total_fd}

Active Fixed Deposits : {active_fd}

Closed Fixed Deposits : {closed_fd}

Active Deposit Amount :
Rs. {active_amount:.2f}

Expected Maturity Amount :
Rs. {active_maturity:.2f}
"""

        Label(
            summary_window,
            text=summary_text,
            font=("Arial", 12),
            bg="white",
            justify=LEFT
        ).pack(pady=15)

        Button(
            summary_window,
            text="Close",
            bg="black",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15,
            command=summary_window.destroy
        ).pack(pady=15)

    # ==========================================
    # BUTTON FRAME
    # ==========================================

    button_frame = Frame(
        fd_window,
        bg="white"
    )

    button_frame.pack(
        pady=10
    )

    Button(
        button_frame,
        text="👁 View Details",
        bg="#0B5ED7",
        fg="white",
        font=("Arial", 11, "bold"),
        width=18,
        command=view_details
    ).grid(
        row=0,
        column=0,
        padx=5
    )

    Button(
        button_frame,
        text="❌ Close / Withdraw FD",
        bg="#DC3545",
        fg="white",
        font=("Arial", 11, "bold"),
        width=22,
        command=close_fd
    ).grid(
        row=0,
        column=1,
        padx=5
    )

    Button(
        button_frame,
        text="📊 FD Summary",
        bg="#198754",
        fg="white",
        font=("Arial", 11, "bold"),
        width=18,
        command=fd_summary
    ).grid(
        row=0,
        column=2,
        padx=5
    )

    # ==========================================
    # INITIAL LOAD
    # ==========================================

    load_fds()



def view_pending_loans():

    window = Toplevel(root)
    window.title("Pending Loan Requests")
    window.geometry("750x450")
    window.configure(bg="white")

    Label(
        window,
        text="PENDING LOAN REQUESTS",
        font=("Arial",18,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=15)

    text = Text(window, width=95, height=18)
    text.pack()

    cursor.execute("""
    SELECT loan_id, account_no, amount, interest, months, status
    FROM loans
    WHERE status='Pending'
    """)

    loans = cursor.fetchall()

    if not loans:
        text.insert(END, "No Pending Loan Requests")
        text.config(state="disabled")
        return

    text.insert(
        END,
        "Loan ID\tAcc No\tAmount\tInterest\tMonths\tStatus\n"
    )

    text.insert(
        END,
        "="*90 + "\n"
    )

    for loan in loans:
        text.insert(
            END,
            f"{loan[0]}\t{loan[1]}\tRs.{loan[2]}\t{loan[3]}%\t{loan[4]}\t{loan[5]}\n"
        )

    text.config(state="disabled")      
             
    
def open_admin_dashboard():

    dash = Toplevel(root)
    dash.title("Admin Dashboard")
    dash.geometry("950x700")
    dash.configure(bg="white")

    # ==========================================
    # ADMIN DASHBOARD SCROLL
    # ==========================================

    canvas = Canvas(
        dash,
        bg="white",
        highlightthickness=0
    )

    scrollbar = Scrollbar(
        dash,
        orient="vertical",
        command=canvas.yview
    )

    scroll_frame = Frame(
        canvas,
        bg="white"
    )

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=scroll_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ==========================================
    # ADMIN TITLE
    # ==========================================

    Label(
        scroll_frame,
        text="ADMIN DASHBOARD",
        font=("Arial",20,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=20)

    # ==========================================
    # DASHBOARD STATISTICS
    # ==========================================

    stats_frame = Frame(
        scroll_frame,
        bg="white"
    )

    stats_frame.pack(pady=15)

    # ------------------------------------------
    # DATABASE STATISTICS
    # ------------------------------------------

    cursor.execute(
        "SELECT COUNT(*) FROM accounts"
    )
    total_customers = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM atm_cards"
    )
    total_atm_cards = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM atm_cards
        WHERE status='Blocked'
    """)
    blocked_cards = cursor.fetchone()[0]

    # ==========================================
    # LOAN STATISTICS
    # ==========================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM loans
    """)
    total_loans = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM loans
        WHERE status='Pending'
    """)
    pending_loans = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM loans
        WHERE status='Approved'
    """)
    approved_loans = cursor.fetchone()[0]

    # ==========================================
    # FIXED DEPOSIT STATISTICS
    # ==========================================

    cursor.execute("""
        SELECT COUNT(*)
        FROM fixed_deposits
    """)
    total_fds = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM fixed_deposits
        WHERE status='Active'
    """)
    active_fds = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM fixed_deposits
        WHERE status='Closed'
    """)
    closed_fds = cursor.fetchone()[0]
    

    # ==========================================
    # TOTAL CUSTOMERS CARD
    # ==========================================

    customer_card = Frame(
        stats_frame,
        bg="#0B5ED7",
        width=220,
        height=110,
        bd=3,
        relief="ridge"
    )

    customer_card.grid(
        row=0,
        column=0,
        padx=10
    )

    customer_card.pack_propagate(False)

    Label(
        customer_card,
        text="👥 Total Customers",
        font=("Arial",12,"bold"),
        bg="#0B5ED7",
        fg="white"
    ).pack(pady=(15,5))

    Label(
        customer_card,
        text=str(total_customers),
        font=("Arial",24,"bold"),
        bg="#0B5ED7",
        fg="yellow"
    ).pack()

    # ==========================================
    # TOTAL ATM CARDS
    # ==========================================

    atm_card = Frame(
        stats_frame,
        bg="#006400",
        width=220,
        height=110,
        bd=3,
        relief="ridge"
    )

    atm_card.grid(
        row=0,
        column=1,
        padx=10
    )

    atm_card.pack_propagate(False)

    Label(
        atm_card,
        text="💳 Total ATM Cards",
        font=("Arial",12,"bold"),
        bg="#006400",
        fg="white"
    ).pack(pady=(15,5))

    Label(
        atm_card,
        text=str(total_atm_cards),
        font=("Arial",24,"bold"),
        bg="#006400",
        fg="yellow"
    ).pack()

    # ==========================================
    # BLOCKED ATM CARDS
    # ==========================================

    blocked_card = Frame(
        stats_frame,
        bg="#B00020",
        width=220,
        height=110,
        bd=3,
        relief="ridge"
    )

    blocked_card.grid(
        row=0,
        column=2,
        padx=10
    )

    blocked_card.pack_propagate(False)

    Label(
        blocked_card,
        text="🚫 Blocked Cards",
        font=("Arial",12,"bold"),
        bg="#B00020",
        fg="white"
    ).pack(pady=(15,5))

    Label(
        blocked_card,
        text=str(blocked_cards),
        font=("Arial",24,"bold"),
        bg="#B00020",
        fg="yellow"
    ).pack()

    # ==========================================
    # LOAN & FD STATISTICS
    # ==========================================

    stats2_frame = Frame(
        scroll_frame,
        bg="white"
    )

    stats2_frame.pack(pady=10)

    # ==========================================
    # TOTAL LOANS
    # ==========================================

    loan_card = Frame(
        stats2_frame,
        bg="#6A1B9A",
        width=220,
        height=110,
        bd=3,
        relief="ridge"
    )

    loan_card.grid(
        row=0,
        column=0,
        padx=10
    )

    loan_card.pack_propagate(False)

    Label(
        loan_card,
        text="💰 Total Loans",
        font=("Arial",12,"bold"),
        bg="#6A1B9A",
        fg="white"
    ).pack(pady=(15,5))

    Label(
        loan_card,
        text=str(total_loans),
        font=("Arial",24,"bold"),
        bg="#6A1B9A",
        fg="yellow"
    ).pack()


    # ==========================================
    # PENDING LOANS
    # ==========================================

    pending_loan_card = Frame(
        stats2_frame,
        bg="#FF8C00",
        width=220,
        height=110,
        bd=3,
        relief="ridge"
    )

    pending_loan_card.grid(
        row=0,
        column=1,
        padx=10
    )

    pending_loan_card.pack_propagate(False)

    Label(
        pending_loan_card,
        text="⏳ Pending Loans",
        font=("Arial",12,"bold"),
        bg="#FF8C00",
        fg="white"
    ).pack(pady=(15,5))

    Label(
        pending_loan_card,
        text=str(pending_loans),
        font=("Arial",24,"bold"),
        bg="#FF8C00",
        fg="yellow"
    ).pack()


    # ==========================================
    # APPROVED LOANS
    # ==========================================

    approved_loan_card = Frame(
        stats2_frame,
        bg="#198754",
        width=220,
        height=110,
        bd=3,
        relief="ridge"
    )

    approved_loan_card.grid(
        row=0,
        column=2,
        padx=10
    )

    approved_loan_card.pack_propagate(False)

    Label(
        approved_loan_card,
        text="✅ Approved Loans",
        font=("Arial",12,"bold"),
        bg="#198754",
        fg="white"
    ).pack(pady=(15,5))

    Label(
        approved_loan_card,
        text=str(approved_loans),
        font=("Arial",24,"bold"),
        bg="#198754",
        fg="yellow"
    ).pack()


    # ==========================================
    # FD STATISTICS
    # ==========================================

    stats3_frame = Frame(
        scroll_frame,
        bg="white"
    )

    stats3_frame.pack(pady=10)


    # ==========================================
    # TOTAL FIXED DEPOSITS
    # ==========================================

    total_fd_card = Frame(
        stats3_frame,
        bg="#006400",
        width=220,
        height=110,
        bd=3,
        relief="ridge"
    )

    total_fd_card.grid(
        row=0,
        column=0,
        padx=10
    )

    total_fd_card.pack_propagate(False)

    Label(
        total_fd_card,
        text="🏦 Total FDs",
        font=("Arial",12,"bold"),
        bg="#006400",
        fg="white"
    ).pack(pady=(15,5))

    Label(
        total_fd_card,
        text=str(total_fds),
        font=("Arial",24,"bold"),
        bg="#006400",
        fg="yellow"
    ).pack()


    # ==========================================
    # ACTIVE FIXED DEPOSITS
    # ==========================================

    active_fd_card = Frame(
        stats3_frame,
        bg="#0B5ED7",
        width=220,
        height=110,
        bd=3,
        relief="ridge"
    )

    active_fd_card.grid(
        row=0,
        column=1,
        padx=10
    )

    active_fd_card.pack_propagate(False)

    Label(
        active_fd_card,
        text="🟢 Active FDs",
        font=("Arial",12,"bold"),
        bg="#0B5ED7",
        fg="white"
    ).pack(pady=(15,5))

    Label(
        active_fd_card,
        text=str(active_fds),
        font=("Arial",24,"bold"),
        bg="#0B5ED7",
        fg="yellow"
    ).pack()


    # ==========================================
    # CLOSED FIXED DEPOSITS
    # ==========================================

    closed_fd_card = Frame(
        stats3_frame,
        bg="#B00020",
        width=220,
        height=110,
        bd=3,
        relief="ridge"
    )

    closed_fd_card.grid(
        row=0,
        column=2,
        padx=10
    )

    closed_fd_card.pack_propagate(False)

    Label(
        closed_fd_card,
        text="🔴 Closed FDs",
        font=("Arial",12,"bold"),
        bg="#B00020",
        fg="white"
    ).pack(pady=(15,5))

    Label(
        closed_fd_card,
        text=str(closed_fds),
        font=("Arial",24,"bold"),
        bg="#B00020",
        fg="yellow"
    ).pack()

    # ==========================================
    # CUSTOMER MANAGEMENT
    # ==========================================

    Label(
        scroll_frame,
        text="👥 CUSTOMER MANAGEMENT",
        font=("Arial",13,"bold"),
        bg="white",
        fg="#0B5ED7"
    ).pack(pady=(15,5))

    Button(
        scroll_frame,
        text="👥 View All Accounts",
        font=("Arial",12,"bold"),
        bg="#198754",
        fg="white",
        width=25,
        command=view_all_accounts 
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="🔍 Search Account",
        font=("Arial",12,"bold"),
        bg="#0B5ED7",
        fg="white",
        width=25,
        command=search_account
    ).pack(pady=5)




    Button(
        scroll_frame,
        text="➕ Create Account",
        font=("Arial",12,"bold"),
        bg="#006400",
        fg="white",
        width=25,
        command=create_account_admin
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="✏️ Edit Account",
        font=("Arial",12,"bold"),
        bg="#FF8C00",
        fg="white",
        width=25,
        command=edit_customer
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="🗑 Delete Account",
        font=("Arial",12,"bold"),
        bg="#DC3545",
        fg="white",
        width=25,
        command=delete_account
    ).pack(pady=5)

    # ==========================================
    # TRANSACTIONS & REPORTS
    # ==========================================

    Label(
        scroll_frame,
        text="📊 TRANSACTIONS & REPORTS",
        font=("Arial",13,"bold"),
        bg="white",
        fg="#6A1B9A"
    ).pack(pady=(15,5))

    Button(
        scroll_frame,
        text="📜 View All Transactions",
        font=("Arial",12,"bold"),
        bg="#6A1B9A",
        fg="white",
        width=25,
        command=view_all_transactions
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="🏦 Bank Summary",
        font=("Arial",12,"bold"),
        bg="#006400",
        fg="white",
        width=25,
        command=bank_summary
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="📄 Generate PDF Report",
        font=("Arial",12,"bold"),
        bg="#198754",
        fg="white",
        width=25,
        command=generate_admin_report
    ).pack(pady=5)

    # ==========================================
    # LOAN MANAGEMENT
    # ==========================================

    Label(
        scroll_frame,
        text="💰 LOAN MANAGEMENT",
        font=("Arial",13,"bold"),
        bg="white",
        fg="#8B4513"
    ).pack(pady=(15,5))

    Button(
        scroll_frame,
        text="📋 View Loan Requests",
        font=("Arial",12,"bold"),
        bg="#0B5ED7",
        fg="white",
        width=25,
        command=view_loan_requests
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="⏳ Pending Loans",
        font=("Arial",12,"bold"),
        bg="#8B4513",
        fg="white",
        width=25,
        command=view_pending_loans
    ).pack(pady=5)

    # ==========================================
    # FIXED DEPOSIT MANAGEMENT
    # ==========================================

    Label(
        scroll_frame,
        text="🏦 FIXED DEPOSIT MANAGEMENT",
        font=("Arial", 13, "bold"),
        bg="white",
        fg="darkgreen"
    ).pack(pady=(15, 5))

    Button(
        scroll_frame,
        text="🏦 Fixed Deposit Management",
        font=("Arial", 12, "bold"),
        bg="darkgreen",
        fg="white",
        width=25,
        command=admin_fixed_deposit_management
    ).pack(pady=5)

    # ==========================================
    # ATM MANAGEMENT
    # ==========================================

    Label(
        scroll_frame,
        text="💳 ATM MANAGEMENT",
        font=("Arial",13,"bold"),
        bg="white",
        fg="#0B5ED7"
    ).pack(pady=(15,5))

    Button(
        scroll_frame,
        text="📋 ATM Requests",
        font=("Arial",12,"bold"),
        bg="#343A40",
        fg="white",
        width=25,
        command=view_atm_requests
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="💳 ATM Management",
        font=("Arial",12,"bold"),
        bg="#0B5ED7",
        fg="white",
        width=25,
        command=admin_atm_dashboard
    ).pack(pady=5)



    # ==========================================
    # BANK TOOLS
    # ==========================================

    Label(
        scroll_frame,
        text="🛠 BANK TOOLS",
        font=("Arial",13,"bold"),
        bg="white",
        fg="#006400"
    ).pack(pady=(15,5))

    Button(
        scroll_frame,
        text="🧮 Interest Calculator",
        font=("Arial",12,"bold"),
        bg="#343A40",
        fg="white",
        width=25,
        command=interest_calculator
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="💾 Backup Database",
        font=("Arial",12,"bold"),
        bg="#8B4513",
        fg="white",
        width=25,
        command=backup_database
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="♻️ Restore Database",
        font=("Arial",12,"bold"),
        bg="#FF8C00",
        fg="white",
        width=25,
        command=restore_database
    ).pack(pady=5)

    # ==========================================
    # ADMIN CONTROL
    # ==========================================

    Label(
        scroll_frame,
        text="⚙️ ADMIN CONTROL",
        font=("Arial",13,"bold"),
        bg="white",
        fg="black"
    ).pack(pady=(15,5))

    Button(
        scroll_frame,
        text="⚙️ Admin Dashboard",
        font=("Arial",12,"bold"),
        bg="#198754",
        fg="white",
        width=25,
        command=admin_dashboard
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="🚪 Logout",
        font=("Arial",12,"bold"),
        bg="black",
        fg="white",
        width=25,
        command=dash.destroy
    ).pack(pady=20)

    # ==========================================
    # MOUSE WHEEL SCROLL
    # ==========================================

    def mouse_scroll(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind_all(
        "<MouseWheel>",
        mouse_scroll
    )

def deposit_money(account_no, balance_label):

    deposit_window = Toplevel(root)
    deposit_window.title("Deposit Money")
    deposit_window.geometry("350x250")
    deposit_window.configure(bg="white")

    Label(
        deposit_window,
        text="Deposit Money",
        font=("Arial",16,"bold"),
        bg="white",
        fg="green"
    ).pack(pady=20)

    Label(
        deposit_window,
        text="Enter Amount",
        font=("Arial",12),
        bg="white"
    ).pack()

    amount_entry = Entry(
        deposit_window,
        font=("Arial",12),
        width=20
    )
    amount_entry.pack(pady=10)

    def save_deposit():
        try:
            amount = float(amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Amount")
            return

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than zero")
            return

        cursor.execute("""
        UPDATE accounts
        SET balance = balance + ?
        WHERE account_no = ?
        """, (amount, account_no))
        conn.commit()

        from datetime import datetime

        date_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

        cursor.execute("""
        INSERT INTO transactions(account_no, transaction_type, amount, date_time)
        VALUES (?, ?, ?, ?)
        """, (
            account_no,
            "Deposit",
            amount,
            date_time
        ))
        conn.commit()

        cursor.execute("""
        SELECT balance
        FROM accounts
        WHERE account_no=?
        """, (account_no,))

        new_balance = cursor.fetchone()[0]

        balance_label.config(text=f"Balance : Rs. {new_balance}")

        messagebox.showinfo("Success", "Deposit Successful")

        deposit_window.destroy()

    Button(
        deposit_window,
        text="Deposit",
        font=("Arial",12,"bold"),
        bg="green",
        fg="white",
        command=save_deposit
    ).pack(pady=15)


def withdraw_money(account_no, balance_label):

    withdraw_window = Toplevel(root)
    withdraw_window.title("Withdraw Money")
    withdraw_window.geometry("350x250")
    withdraw_window.configure(bg="white")

    Label(
        withdraw_window,
        text="Withdraw Money",
        font=("Arial",16,"bold"),
        bg="white",
        fg="orange"
    ).pack(pady=20)

    Label(
        withdraw_window,
        text="Enter Amount",
        font=("Arial",12),
        bg="white"
    ).pack()

    amount_entry = Entry(
        withdraw_window,
        font=("Arial",12),
        width=20
    )
    amount_entry.pack(pady=10)

    def save_withdraw():
        try:
            amount = float(amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid Amount")
            return

        if amount <= 0:
            messagebox.showerror("Error", "Amount must be greater than zero")
            return

        # check current balance
        cursor.execute("""
        SELECT balance
        FROM accounts
        WHERE account_no=?
        """, (account_no,))

        row = cursor.fetchone()

        if row is None:
            messagebox.showerror("Error", "Account not found")
            withdraw_window.destroy()
            return

        current_balance = row[0]
        if amount > current_balance:
            messagebox.showerror("Error", "Insufficient Balance")
            return 

        # Check Approved Loan
        cursor.execute("""
        SELECT loan_id, amount, status
        FROM loans
        WHERE account_no = ? AND status = 'Approved'
        """, (account_no,))

        loan = cursor.fetchone()

        if loan is None:
            messagebox.showerror("Error", "No Approved Loan Found")
            return

        loan_id = loan[0]
        loan_balance = loan[1]

        if amount > loan_balance:
            messagebox.showerror(
                "Error",
                "EMI amount is greater than remaining loan amount"
            )
            return

        # Deduct Customer Balance
        cursor.execute("""
        UPDATE accounts
        SET balance = balance - ?
        WHERE account_no = ?
        """, (amount, account_no))

        # Update Loan Balance
        new_loan_balance = loan_balance - amount

        cursor.execute("""
        UPDATE loans
        SET amount = ?
        WHERE loan_id = ?
        """, (new_loan_balance, loan_id))

        conn.commit()

        from datetime import datetime

        date_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

        cursor.execute("""
        INSERT INTO transactions(account_no, transaction_type, amount, date_time)
        VALUES (?, ?, ?, ?)
        """, (
            account_no,
            "Withdraw",
            amount,
            date_time
        ))
        conn.commit()

        date_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

        # Save Transaction History
        cursor.execute("""
        INSERT INTO transactions(account_no, transaction_type, amount, date_time)
        VALUES (?, ?, ?, ?)
        """, (
            account_no,
            "EMI Payment",
            amount,
            date_time
        ))

        # Close Loan if Fully Paid
        if new_loan_balance <= 0:

            cursor.execute("""
            UPDATE loans
            SET status = 'Closed'
            WHERE loan_id = ?
            """, (loan_id,))

        conn.commit()

        messagebox.showinfo(
            "Success",
            f"EMI Payment Successful\nRemaining Loan : Rs. {new_loan_balance}"
        )

        cursor.execute("""
        SELECT balance
        FROM accounts
        WHERE account_no=?
        """, (account_no,))

        new_balance = cursor.fetchone()[0]

        balance_label.config(text=f"Balance : Rs. {new_balance}")

        messagebox.showinfo("Success", "Withdrawal Successful")

        withdraw_window.destroy()

    Button(
        withdraw_window,
        text="Withdraw",
        font=("Arial",12,"bold"),
        bg="orange",
        fg="white",
        command=save_withdraw
    ).pack(pady=15)

def transfer_money(account_no, balance_label):

    transfer_window = Toplevel(root)
    transfer_window.title("Transfer Money")
    transfer_window.geometry("350x300")
    transfer_window.configure(bg="white")

    Label(
        transfer_window,
        text="Transfer Money",
        font=("Arial",16,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=15)

    Label(
        transfer_window,
        text="Receiver Account Number",
        bg="white",
        font=("Arial",12)
    ).pack()

    receiver_entry = Entry(
        transfer_window,
        font=("Arial",12),
        width=25
    )
    receiver_entry.pack(pady=8)

    Label(
        transfer_window,
        text="Amount",
        bg="white",
        font=("Arial",12)
    ).pack()

    amount_entry = Entry(
        transfer_window,
        font=("Arial",12),
        width=25
    )
    amount_entry.pack(pady=8)    

    def save_transfer():
        receiver = receiver_entry.get()
        amount = amount_entry.get()

        if receiver == "" or amount == "":
            messagebox.showerror(
                "Error",
                "Fill all fields"
            )
            return

        try:
            amount = float(amount)

        except:
            messagebox.showerror(
                "Error",
                "Invalid Amount"
            )
            return


        # Check receiver account
        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no=?
            """,
            (receiver,)
        )

        receiver_data = cursor.fetchone()


        if receiver_data is None:
            messagebox.showerror(
                "Error",
                "Receiver Account Not Found"
            )
            return


        # Check sender balance
        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no=?
            """,
            (account_no,)
        )

        sender_balance = cursor.fetchone()[0]


        if amount > sender_balance:
            messagebox.showerror(
                "Error",
                "Insufficient Balance"
            )
            return


        # Remove money from sender

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance - ?
            WHERE account_no=?
            """,
            (amount, account_no)
        )


        # Add money to receiver

        cursor.execute(
            """
            UPDATE accounts
            SET balance = balance + ?
            WHERE account_no=?
            """,
            (amount, receiver)
        )


        conn.commit()


        from datetime import datetime

        date_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )


        # Sender transaction

        cursor.execute(
            """
            INSERT INTO transactions(
            account_no,
            transaction_type,
            amount,
            date_time
            )
            VALUES(?,?,?,?)
            """,
            (
                account_no,
                "Transfer Sent",
                amount,
                date_time
            )
        )


        # Receiver transaction

        cursor.execute(
            """
            INSERT INTO transactions(
            account_no,
            transaction_type,
            amount,
            date_time
            )
            VALUES(?,?,?,?)
            """,
            (
                receiver,
                "Transfer Received",
                amount,
                date_time
            )
        )


        conn.commit()


        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no=?
            """,
            (account_no,)
        )

        new_balance = cursor.fetchone()[0]


        balance_label.config(
            text=f"Balance : Rs. {new_balance}"
        )


        messagebox.showinfo(
            "Success",
            "Money Transfer Successful"
        )


        transfer_window.destroy()

    Button(
        transfer_window,
        text="Transfer",
        font=("Arial", 12, "bold"),
        bg="blue",
        fg="white",
        width=15,
        command=save_transfer
    ).pack(pady=15)

def upload_profile_photo(account_no, photo_label):

    file_path = filedialog.askopenfilename(
        title="Select Profile Photo",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg")
        ]
    )

    if not file_path:
        return

    cursor.execute("""
    UPDATE accounts
    SET photo=?
    WHERE account_no=?
    """, (file_path, account_no))

    conn.commit()

    # use the selected file path (row is undefined here)
    image = Image.open(file_path)
    image.thumbnail((150,150))

    photo = ImageTk.PhotoImage(image)

    photo_label.configure(
        image=photo,
        width=150,
        height=150
    )
    photo_label.image = photo

    messagebox.showinfo(
        "Success",
        "Profile Photo Updated Successfully"
    )    

def customer_profile(account_no=None):

    if account_no is None:
        messagebox.showerror("Error", "No account specified")
        return

    profile = Toplevel(root)
    profile.title("My Profile")
    profile.geometry("500x500")

    cursor.execute("""
    SELECT
        name,
        balance,
        phone,
        email,
        address
    FROM accounts
    WHERE account_no=?
    """,(account_no,))

    row = cursor.fetchone()

    if row is None:
        messagebox.showerror(
            "Error",
            "Customer not found"
        )
        profile.destroy()
        return

    Label(profile,text="Customer Profile",font=("Arial",16,"bold")).pack(pady=10)

    Label(profile,text=f"Name : {row[0]}").pack(anchor="w",padx=20,pady=5)

    Label(profile,text=f"Balance : Rs. {row[1]}").pack(anchor="w",padx=20,pady=5)

    Label(profile,text=f"Phone : {row[2]}").pack(anchor="w",padx=20,pady=5)

    Label(profile,text=f"Email : {row[3]}").pack(anchor="w",padx=20,pady=5)

    Label(profile,text=f"Address : {row[4]}").pack(anchor="w",padx=20,pady=5)


def customer_dashboard():
    ...    


def change_pin(account_no):

    pin_window = Toplevel(root)
    pin_window.title("Change PIN")
    pin_window.geometry("350x250")
    pin_window.configure(bg="white")

    Label(
        pin_window,
        text="Change PIN",
        font=("Arial",16,"bold"),
        bg="white",
        fg="brown"
    ).pack(pady=15)

    Label(pin_window, text="Current PIN", bg="white").pack()
    current_entry = Entry(pin_window, font=("Arial",12), show="*")
    current_entry.pack(pady=5)

    Label(pin_window, text="New PIN", bg="white").pack()
    new_entry = Entry(pin_window, font=("Arial",12), show="*")
    new_entry.pack(pady=5)

    Label(pin_window, text="Confirm New PIN", bg="white").pack()
    confirm_entry = Entry(pin_window, font=("Arial",12), show="*")
    confirm_entry.pack(pady=5)

    def save_pin():
        current = current_entry.get().strip()
        new = new_entry.get().strip()
        confirm = confirm_entry.get().strip()

        if current == "" or new == "" or confirm == "":
            messagebox.showerror("Error", "Fill all fields")
            return

        if new != confirm:
            messagebox.showerror("Error", "New PINs do not match")
            return

        cursor.execute(
            "SELECT pin FROM accounts WHERE account_no=?",
            (account_no,)
        )
        row = cursor.fetchone()
        if row is None:
            messagebox.showerror("Error", "Account not found")
            pin_window.destroy()
            return

        if str(row[0]) != current:
            messagebox.showerror("Error", "Current PIN is incorrect")
            return

        cursor.execute(
            "UPDATE accounts SET pin=? WHERE account_no=?",
            (new, account_no)
        )
        conn.commit()

        messagebox.showinfo("Success", "PIN changed successfully")
        pin_window.destroy()

    Button(
        pin_window,
        text="Change PIN",
        bg="brown",
        fg="white",
        font=("Arial",12,"bold"),
        command=save_pin
    ).pack(pady=15)


def apply_loan(account_no):

    loan_window = Toplevel(root)
    loan_window.title("Apply Loan")
    loan_window.geometry("400x500")
    loan_window.configure(bg="white")


    Label(
        loan_window,
        text="APPLY LOAN",
        font=("Arial",18,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=15)


    Label(
        loan_window,
        text="Loan Type",
        bg="white"
    ).pack()


    loan_type = Entry(
        loan_window,
        font=("Arial",12)
    )
    loan_type.pack(pady=5)


    Label(
        loan_window,
        text="Loan Amount",
        bg="white"
    ).pack()


    amount_entry = Entry(
        loan_window,
        font=("Arial",12)
    )
    amount_entry.pack(pady=5)


    Label(
        loan_window,
        text="Months",
        bg="white"
    ).pack()


    months_entry = Entry(
        loan_window,
        font=("Arial",12)
    )
    months_entry.pack(pady=5)


    def submit():

        try:
            amount = float(amount_entry.get())
            months = int(months_entry.get())

        except:
            messagebox.showerror(
                "Error",
                "Invalid Input"
            )
            return


        if amount <= 0:
            messagebox.showerror(
                "Error",
                "Loan amount must be greater than 0"
            )
            return

        if months <= 0:
            messagebox.showerror(
                "Error",
                "Months must be greater than 0"
            )
            return

        if loan_type.get().strip() == "":
            messagebox.showerror(
                "Error",
                "Enter Loan Type"
            )
            return


        interest = 8


        emi = (
            amount +
            (amount * interest/100)
        ) / months


        from datetime import datetime

        date = datetime.now().strftime(
            "%d-%m-%Y"
        )


        cursor.execute("""
        INSERT INTO loans(
        account_no,
        loan_type,
        amount,
        interest,
        months,
        emi,
        status,
        date
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            account_no,
            loan_type.get(),
            amount,
            interest,
            months,
            emi,
            "Pending",
            date
        ))


        conn.commit()


        messagebox.showinfo(
            "Success",
            f"Loan Applied Successfully\nEMI : Rs. {emi:.2f}"
        )


        loan_window.destroy()


    Button(
        loan_window,
        text="Apply Loan",
        bg="blue",
        fg="white",
        font=("Arial",12,"bold"),
        command=submit
    ).pack(pady=20)

def pay_loan_emi(account_no):

    loan_window = Toplevel(root)
    loan_window.title("Pay Loan EMI")
    loan_window.geometry("450x500")
    loan_window.configure(bg="white")

    # ==========================================
    # TITLE
    # ==========================================

    Label(
        loan_window,
        text="PAY LOAN EMI",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="green"
    ).pack(pady=15)

    # ==========================================
    # GET APPROVED LOANS
    # ==========================================

    cursor.execute("""
        SELECT loan_id, loan_type, emi, months
        FROM loans
        WHERE account_no=? AND status='Approved'
    """, (account_no,))

    loans = cursor.fetchall()

    if not loans:

        messagebox.showinfo(
            "Loan",
            "No Active Approved Loan Found"
        )

        loan_window.destroy()
        return

    # ==========================================
    # LOAN LIST
    # ==========================================

    Label(
        loan_window,
        text="Select Loan",
        font=("Arial", 12, "bold"),
        bg="white"
    ).pack(pady=(5, 2))

    loan_list = Listbox(
        loan_window,
        height=5,
        width=40,
        font=("Arial", 11)
    )

    loan_list.pack(pady=5)

    # Show available loans
    for loan in loans:

        loan_id = loan[0]
        loan_type = loan[1]
        emi = float(loan[2])
        months = loan[3]

        loan_list.insert(
            "end",
            f"Loan ID: {loan_id} | {loan_type} | EMI: Rs. {emi:.2f} | {months} Months"
        )

    # ==========================================
    # EMI AMOUNT
    # ==========================================

    Label(
        loan_window,
        text="Enter EMI Amount",
        font=("Arial", 12, "bold"),
        bg="white"
    ).pack(pady=(15, 5))

    emi_entry = Entry(
        loan_window,
        font=("Arial", 12),
        width=25
    )

    emi_entry.pack(pady=5)

    # ==========================================
    # PAY FUNCTION
    # ==========================================

    def pay():

        selected = loan_list.curselection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a loan"
            )

            return

        emi_text = emi_entry.get().strip()

        if emi_text == "":

            messagebox.showerror(
                "Error",
                "Enter EMI Amount"
            )

            return

        # ======================================
        # GET SELECTED LOAN
        # ======================================

        selected_index = selected[0]

        selected_loan = loans[selected_index]

        loan_id = selected_loan[0]

        # ======================================
        # CHECK EMI AMOUNT
        # ======================================

        try:

            entered_emi = float(emi_text)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Invalid EMI Amount"
            )

            return

        # ======================================
        # GET ACTUAL EMI FROM DATABASE
        # ======================================

        cursor.execute("""
            SELECT emi, months
            FROM loans
            WHERE loan_id=?
            AND account_no=?
            AND status='Approved'
        """, (
            loan_id,
            account_no
        ))

        loan_row = cursor.fetchone()

        if not loan_row:

            messagebox.showerror(
                "Error",
                "Loan not found or not approved"
            )

            return

        actual_emi = float(loan_row[0])
        remaining_months = int(loan_row[1])

        # ======================================
        # EXACT EMI CHECK
        # ======================================

        if abs(entered_emi - actual_emi) > 0.01:

            messagebox.showerror(
                "Wrong EMI",
                f"Please enter the exact EMI amount.\n\n"
                f"Required EMI: Rs. {actual_emi:.2f}"
            )

            return

        # ======================================
        # CHECK ACCOUNT BALANCE
        # ======================================

        cursor.execute("""
            SELECT balance
            FROM accounts
            WHERE account_no=?
        """, (account_no,))

        balance_row = cursor.fetchone()

        if not balance_row:

            messagebox.showerror(
                "Error",
                "Account not found"
            )

            return

        balance = float(balance_row[0])

        # ======================================
        # INSUFFICIENT BALANCE
        # ======================================

        if entered_emi > balance:

            messagebox.showerror(
                "Insufficient Balance",
                f"Available Balance: Rs. {balance:.2f}\n"
                f"Required EMI: Rs. {entered_emi:.2f}"
            )

            return

        # ======================================
        # DEDUCT EMI FROM ACCOUNT
        # ======================================

        cursor.execute("""
            UPDATE accounts
            SET balance = balance - ?
            WHERE account_no=?
        """, (
            entered_emi,
            account_no
        ))

        # ======================================
        # UPDATE LOAN MONTHS
        # ======================================

        new_months = remaining_months - 1

        if new_months <= 0:

            cursor.execute("""
                UPDATE loans
                SET months=0,
                    status='Paid'
                WHERE loan_id=?
                AND account_no=?
            """, (
                loan_id,
                account_no
            ))

        else:

            cursor.execute("""
                UPDATE loans
                SET months=?
                WHERE loan_id=?
                AND account_no=?
            """, (
                new_months,
                loan_id,
                account_no
            ))

        # ======================================
        # SAVE TRANSACTION
        # ======================================

        date_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

        cursor.execute("""
            INSERT INTO transactions(
                account_no,
                transaction_type,
                amount,
                date_time
            )
            VALUES(?,?,?,?)
        """, (
            account_no,
            "Loan EMI Payment",
            entered_emi,
            date_time
        ))

        # ======================================
        # COMMIT
        # ======================================

        conn.commit()

        # ======================================
        # SUCCESS MESSAGE
        # ======================================

        if new_months <= 0:

            messagebox.showinfo(
                "Loan Completed",
                "🎉 Congratulations!\n\n"
                "Final EMI Paid Successfully.\n"
                "Your Loan is now Fully Paid."
            )

        else:

            messagebox.showinfo(
                "Success",
                f"EMI Paid Successfully!\n\n"
                f"Paid: Rs. {entered_emi:.2f}\n"
                f"Remaining Months: {new_months}"
            )

        loan_window.destroy()

    # ==========================================
    # PAY EMI BUTTON
    # ==========================================

    Button(
        loan_window,
        text="💰 Pay EMI",
        bg="green",
        fg="white",
        font=("Arial", 12, "bold"),
        width=18,
        command=pay
    ).pack(pady=20)

def loan_emi_history(account_no):

    window = Toplevel(root)
    window.title("Loan EMI History")
    window.geometry("650x500")
    window.configure(bg="white")

    Label(
        window,
        text="💳 LOAN EMI PAYMENT HISTORY",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="blue"
    ).pack(pady=20)

    cursor.execute("""
        SELECT
            id,
            amount,
            date_time
        FROM transactions
        WHERE account_no=?
        AND transaction_type='Loan EMI Payment'
        ORDER BY id DESC
    """, (account_no,))

    payments = cursor.fetchall()

    if not payments:

        Label(
            window,
            text="No EMI Payments Found",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="red"
        ).pack(pady=50)

        return

    # ==========================================
    # TOTAL EMI PAID
    # ==========================================

    total_paid = sum(float(payment[1]) for payment in payments)

    Label(
        window,
        text=f"Total EMI Paid : Rs. {total_paid:.2f}",
        font=("Arial", 13, "bold"),
        bg="white",
        fg="green"
    ).pack(pady=5)

    # ==========================================
    # HISTORY LIST
    # ==========================================

    history_list = Listbox(
        window,
        width=70,
        height=15,
        font=("Arial", 11)
    )

    history_list.pack(
        padx=20,
        pady=15
    )

    for payment in payments:

        transaction_id = payment[0]
        amount = float(payment[1])
        date_time = payment[2]

        history_list.insert(
            "end",
            f"ID: {transaction_id} | "
            f"EMI: Rs. {amount:.2f} | "
            f"{date_time}"
        )

    # ==========================================
    # CLOSE BUTTON
    # ==========================================

    Button(
        window,
        text="Close",
        bg="red",
        fg="white",
        font=("Arial", 11, "bold"),
        width=15,
        command=window.destroy
    ).pack(pady=10)


def transaction_history(account_no):

    history_window = Toplevel(root)
    history_window.title("Transaction History")
    history_window.geometry("600x400")
    history_window.configure(bg="white")

    Label(
        history_window,
        text="Transaction History",
        font=("Arial",16,"bold"),
        bg="white",
        fg="purple"
    ).pack(pady=10)

    listbox = Listbox(
        history_window,
        width=80,
        height=15,
        font=("Consolas",10)
    )
    listbox.pack(pady=10)

    cursor.execute("""
    SELECT transaction_type, amount, date_time
    FROM transactions
    WHERE account_no = ?
    ORDER BY id DESC
    """, (account_no,))

    rows = cursor.fetchall()

    if not rows:
        listbox.insert(END, "No Transactions Found")
    else:
        for row in rows:
            t_type, amount, date_time = row
            listbox.insert(
                END,
                f"{date_time}   |   {t_type}   |   Rs. {amount}"
            )

def edit_profile_photo(account_no, photo_label):

    file_path = filedialog.askopenfilename(
        title="Select New Profile Photo",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg")
        ]
    )

    if not file_path:
        return

    try:
        # Save new photo path into database
        cursor.execute("""
        UPDATE accounts
        SET photo=?
        WHERE account_no=?
        """, (file_path, account_no))

        conn.commit()

        # Display new photo immediately
        image = Image.open(file_path)
        image = image.resize((150, 150))

        photo = ImageTk.PhotoImage(image)

        photo_label.config(
            image=photo,
            text=""
        )

        photo_label.image = photo

        messagebox.showinfo(
            "Success",
            "Profile Photo Updated Successfully"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Unable to update photo:\n{e}"
        )


def delete_profile_photo(account_no, photo_label):

    confirm = messagebox.askyesno(
        "Delete Photo",
        "Are you sure you want to delete your profile photo?"
    )

    if not confirm:
        return

    try:
        # Remove photo path from database
        cursor.execute("""
        UPDATE accounts
        SET photo=NULL
        WHERE account_no=?
        """, (account_no,))

        conn.commit()

        # Remove photo from dashboar
        photo_label.config(
            image="",
            text="No Photo",
            width=18,
            height=9
        )

        photo_label.image = None

        messagebox.showinfo(
            "Success",
            "Profile Photo Deleted Successfully"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            f"Unable to delete photo:\n{e}"
        )            


def mini_statement(account_no):

    print("Mini Statement Opened")
    print("Account =", account_no)

    window = Toplevel(root)

    statement_window = Toplevel(root)
    statement_window.title("Mini Statement")
    statement_window.geometry("600x350")
    statement_window.configure(bg="white")

    Label(
        statement_window,
        text="Mini Statement",
        font=("Arial",16,"bold"),
        bg="white",
        fg="purple"
    ).pack(pady=10)

    listbox = Listbox(
        statement_window,
        width=80,
        height=12,
        font=("Consolas",10)
    )
    listbox.pack(pady=10)
    cursor.execute(
        """
        SELECT transaction_type, amount, date_time
        FROM transactions
        WHERE account_no = ?
        ORDER BY id DESC
        LIMIT 5
        """, (account_no,)
    )

    rows = cursor.fetchall()

    cursor.execute("""
    SELECT transaction_type, amount, date_time
    FROM transactions
    WHERE account_no = ?
    ORDER BY id DESC
    LIMIT 5
    """,(account_no,))

    rows = cursor.fetchall()

    print(rows)

    if not rows:
        listbox.insert(END, "No Recent Transactions Found")
    else:
        for row in rows:
            t_type, amount, date_time = row
            listbox.insert(
                END,
                f"{date_time}   |   {t_type}   |   Rs. {amount}"
            )



def open_customer_dashboard(account):
    # account is a tuple: (account_no, name, balance, pin)
    account_no, name, balance, _ = account

    # create dashboard window
    dash = Toplevel(root)
    dash.title(f"Dashboard - {name}")
    dash.geometry("500x700")
    dash.configure(bg="white")

    canvas = Canvas(dash, bg="white")
    scrollbar = Scrollbar(dash, orient="vertical", command=canvas.yview)

    scroll_frame = Frame(canvas, bg="white")

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    welcome_label = Label(
        scroll_frame,
        text=f"Welcome, {name}",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="green"
    )
    welcome_label.pack(pady=20)

    account_label = Label(
        scroll_frame,
        text=f"Account No : {account_no}",
        font=("Arial", 14),
        bg="white"
    )
    account_label.pack()

    balance_frame = Frame(
    scroll_frame,
    bg="#0B5ED7",
    bd=3,
    relief="ridge"
    )
    balance_frame.pack(fill="x", padx=20, pady=10)

    Label(
        balance_frame,
        text="Available Balance",
        font=("Arial",12,"bold"),
        bg="#0B5ED7",
        fg="white"
    ).pack(pady=(10,0))

    balance_label = Label(
        balance_frame,
        text=f"Rs. {balance:,.2f}",
        font=("Arial",20,"bold"),
        bg="#0B5ED7",
        fg="yellow"
    )
    balance_label.pack(pady=(5,10))

    photo_label = Label(
        scroll_frame,
        text="No Photo",
        font=("Arial",11),
        bg="white",
        fg="gray",
        relief="groove",
        bd=2
    )
    photo_label.pack(pady=15)


    profile_card = Frame(
        scroll_frame,
        bg="#F5F5F5",
        bd=2,
        relief="groove",
        highlightbackground="#DDDDDD",
        highlightthickness=1
    )
    profile_card.pack(fill="x", padx=20, pady=15)

    profile_container = Frame(profile_card, bg="white")
    profile_container.pack(fill="x", padx=20, pady=20)

    left_frame = Frame(profile_container, bg="white")
    left_frame.pack(side="left", padx=10)

    right_frame = Frame(profile_container, bg="white")
    right_frame.pack(side="left", padx=20)

    status_canvas = Canvas(
        left_frame,
        width=24,
        height=24,
        bg="white",
        highlightthickness=0
    )
    status_canvas.place(x=120, y=120)

    status_canvas.create_oval(
        2,
        2,
        22,
        22,
        fill="limegreen",
        outline="white",
        width=2
    )

    Label(
        right_frame,
        text=name,
        font=("Arial",20,"bold"),
        fg="#0B5ED7",
        bg="white"
    ).pack(anchor="w")

    Label(
        right_frame,
        text=f"Account : {account_no}",
        font=("Arial",12),
        bg="white"
    ).pack(anchor="w", pady=5)

    Label(
        right_frame,
        text="👤 Account Holder",
        font=("Arial",11),
        bg="white"
    ).pack(anchor="w", pady=2)

    Label(
        right_frame,
        text="🟢 Active Customer",
        font=("Arial",11),
        fg="green",
        bg="white"
    ).pack(anchor="w")
    print("Checking Photo...")

    

    cursor.execute("""
    SELECT photo
    FROM accounts
    WHERE account_no=?
    """, (account_no,))

    row = cursor.fetchone()

    print(row)

    if row and row[0]:
        print("PHOTO =", row[0])

        try:
            image = Image.open(row[0]).convert("RGBA")
            image = image.resize((150,150))

            mask = Image.new("L", (150,150), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0,0,150,150), fill=255)

            image.putalpha(mask)

            photo = ImageTk.PhotoImage(image)
            
            photo_label.config(
                image=photo,
                text="",
                
            )


            photo_label.image = photo

            print("PHOTO DISPLAYED")

        except Exception as e:
            print("ERROR =", e)



    Label(
        profile_card,
        text="💰 MONEY SERVICES",
        font=("Arial",12,"bold"),
        bg="#F5F5F5",
        fg="#0B5ED7"
    ).pack(pady=(15,5))

    action_frame = Frame(
        scroll_frame,
        bg="#F5F5F5",
        bd=2,
        relief="groove"
    )
    action_frame.pack(fill="x", padx=20, pady=10)
    

    Button(
        action_frame,
        text="💰 Deposit",
        font=("Arial",11,"bold"),
        bg="green",
        fg="white",
        width=18,
        command=lambda: deposit_money(account_no, balance_label)
    ).grid(row=0, column=0, padx=8, pady=8)

    Button(
        action_frame,
        text="💸 Withdraw",
        font=("Arial",11,"bold"),
        bg="orange",
        fg="white",
        width=18,
        command=lambda: withdraw_money(account_no, balance_label)
    ).grid(row=0, column=1, padx=8, pady=8)

    Button(
        action_frame,
        text="🔄 Transfer",
        font=("Arial",11,"bold"),
        bg="#0B5ED7",
        fg="white",
        width=18,
        command=lambda: transfer_money(account_no, balance_label)
    ).grid(row=1, column=0, padx=8, pady=8)

    Button(
        action_frame,
        text="👤 My Profile",
        font=("Arial",11,"bold"),
        bg="purple",
        fg="white",
        width=18,
        command=lambda: customer_profile(account_no)
    ).grid(row=1, column=1, padx=8, pady=8)

    Button(
        profile_card,
        text="📷 Upload Photo",
        font=("Arial",11,"bold"),
        bg="#009688",
        fg="white",
        width=18,
        command=lambda: upload_profile_photo(account_no, photo_label)
    ).pack(pady=10)

    Button(
        action_frame,
        text="✏ Edit Photo",
        font=("Arial",10,"bold"),
        bg="#2196F3",
        fg="white",
        width=15,
        command=lambda: upload_profile_photo(account_no, photo_label)
    ).grid(row=3, column=0, pady=5)

    Button(
        action_frame,
        text="🗑 Delete",
        font=("Arial",10,"bold"),
        bg="red",
        fg="white",
        width=15,
        command=lambda: delete_profile_photo(account_no, photo_label)
    ).grid(row=3,column=1,pady=5)

    Label(
        scroll_frame,
        text="🏦 LOAN SERVICES",
        font=("Arial",13,"bold"),
        bg="white",
        fg="#8B4513"
    ).pack(pady=(15,5))


    loan_btn = Button(
        scroll_frame,
        text="Apply Loan",
        font=("Arial",12,"bold"),
        bg="blue",
        fg="white",
        width=20,
        command=lambda: apply_loan(account_no)
    ) 

    loan_btn.pack(pady=5)

    Button(
        scroll_frame,
        text="Loan Status",
        font=("Arial",12,"bold"),
        bg="purple",
        fg="white",
        width=20,
        command=lambda: loan_status(account[0])
    ).pack(pady=5)    

    Button(
        scroll_frame,
        text="Pay EMI",
        font=("Arial",12,"bold"),
        bg="darkgreen",
        fg="white",
        width=20,
        command=lambda: pay_loan_emi(account[0])
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="EMI Payment History",
        bg="orange",
        fg="white",
        font=("Arial", 12, "bold"),
        width=25,
        command=lambda: loan_emi_history(account_no)
    ).pack(pady=5)


    Label(
       scroll_frame,
       text="💳 ATM SERVICES",
       font=("Arial",13,"bold"),
       bg="white",
       fg="#0B5ED7"
    ).pack(pady=(15,5))
    
    Button(
        scroll_frame,
        text="Apply ATM Card",
        font=("Arial",12,"bold"),
        bg="darkblue",
        fg="white",
        width=20,
        command=lambda: apply_atm_card(account_no)
    ).pack(pady=5)

    


    Button(
        scroll_frame,
        text="ATM Withdrawal",
        font=("Arial",12,"bold"),
        bg="green",
        fg="white",
        width=20,
        command=lambda: atm_withdraw(account_no)
    ).pack(pady=5)
        
    print("ATM Button Created")

    Button(
        scroll_frame,
        text="ATM Cash Deposit",
        bg="green",
        fg="white",
        width=20,
        command=lambda: atm_deposit(account_no)
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="ATM Receipt",
        font=("Arial",12,"bold"),
        bg="blue",
        fg="white",
        width=15,
        command=lambda: atm_receipt(account_no)
    ).pack(pady=10)

    
    Button(
        scroll_frame,
        text="ATM Mini Statement",
        font=("Arial",12,"bold"),
        bg="purple",
        fg="white",
        width=20,
        command=lambda: atm_mini_statement(account_no)
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="ATM Balance Inquiry",
        font=("Arial",12,"bold"),
        bg="blue",
        fg="white",
        width=20,
        command=lambda: atm_balance_inquiry(account_no)
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="Unblock ATM Card",
        font=("Arial",12,"bold"),
        bg="green",
        fg="white",
        width=20,
        command=lambda: unblock_atm_card(account_no)
    ).pack(pady=5)

    Button(
        scroll_frame,
        text="Block ATM Card",
        font=("Arial",12,"bold"),
        bg="red",
        fg="white",
        width=20,
        command=lambda: block_atm_card(account_no)
    ).pack(pady=5)   
     

    Label(
        scroll_frame,
        text="💰 FIXED DEPOSIT SERVICES",
        font=("Arial",13,"bold"),
        bg="white",
        fg="#006400"
    ).pack(pady=(15,5))

    Button(
        scroll_frame,
        text="Fixed Deposit",
        font=("Arial",12,"bold"),
        bg="darkgreen",
        fg="white",
        width=20,
        command=lambda: fixed_deposit(account[0])
    ).pack(pady=5)    


    Button(
        scroll_frame,
        text="My Fixed Deposits",
        font=("Arial",12,"bold"),
        bg="darkblue",
        fg="white",
        width=20,
        command=lambda: view_my_fd(account[0])
    ).pack(pady=5)  


    Button(
        scroll_frame,
        text="Close Fixed Deposit",
        font=("Arial",12,"bold"),
        bg="brown",
        fg="white",
        width=20,
        command=lambda: close_fixed_deposit(account[0])
    ).pack(pady=5)     

    Label(
        scroll_frame,
        text="📜 STATEMENTS & HISTORY",
        font=("Arial",13,"bold"),
        bg="white",
        fg="#6A1B9A"
    ).pack(pady=(15,5))     

    history_btn = Button(
        scroll_frame,
        text="Transaction History",
        font=("Arial", 12, "bold"),
        bg="purple",
        fg="white",
        width=20,
        command=lambda: transaction_history(account_no)
    )
    history_btn.pack(pady=5) 

    statement_btn = Button(
        scroll_frame,
        text="Mini Statement",
        font=("Arial",12,"bold"),
        bg="purple",
        fg="white",
        width=20,
        command=lambda: mini_statement(account_no)
    )

    statement_btn.pack(pady=5)

    Label(
        scroll_frame,
        text="🔐 SECURITY SERVICES",
        font=("Arial",13,"bold"),
        bg="white",
        fg="#8B0000"
    ).pack(pady=(15,5))

    Button(
        scroll_frame,
        text="🔑 Change PIN",
        font=("Arial",12,"bold"),
        bg="brown",
        fg="white",
        width=20,
        command=lambda: change_pin(account_no)
    ).pack(pady=5)    


    Label(
        scroll_frame,
        text="👤 PROFILE SERVICES",
        font=("Arial",13,"bold"),
        bg="white",
        fg="#0B5ED7"
    ).pack(pady=(15,5))

    Button(
        scroll_frame,
        text="👤 Customer Profile",
        font=("Arial",12,"bold"),
        bg="#0B5ED7",
        fg="white",
        width=20,
        command=lambda: customer_profile(account_no)
    ).pack(pady=5)


    # ==========================================
    # CUSTOMER DASHBOARD MOUSE WHEEL SCROLL
    # ==========================================

    def customer_mouse_scroll(event):
        canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    canvas.bind(
        "<MouseWheel>",
        customer_mouse_scroll
    )

    def logout():
        messagebox.showinfo("Logout", "You have been logged out.")
        dash.destroy()

    logout_btn = Button(scroll_frame, text="Logout", font=("Arial", 12, "bold"), bg="red", fg="white", width=12, command=logout)
    logout_btn.pack(pady=20)

    def open_admin_login():

        admin = Toplevel(root)
        admin.title("Admin Login")
        admin.geometry("400x300")
        admin.configure(bg="white")

        Label(
            admin,
            text="ADMIN LOGIN",
            font=("Arial",18,"bold"),
            bg="white",
            fg="blue"
        ).pack(pady=20)

        Label(admin,text="Username",bg="white").pack()

        username_entry = Entry(admin,font=("Arial",12))
        username_entry.pack(pady=5)

        Label(admin,text="Password",bg="white").pack()

        password_entry = Entry(admin,font=("Arial",12),show="*")
        password_entry.pack(pady=5)

        Button(
            admin,
            text="Login",
            bg="blue",
            fg="white",
            font=("Arial",12,"bold"),
            command=lambda: admin_login(
                username_entry,
                password_entry,
                admin
            )
        ).pack(pady=20)

def loan_status(account_no):

    window = Toplevel(root)
    window.title("Loan Status")
    window.geometry("600x500")
    window.configure(bg="white")

    Label(
        window,
        text="🏦 LOAN STATUS",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="blue"
    ).pack(pady=20)

    cursor.execute("""
        SELECT
            loan_id,
            loan_type,
            amount,
            interest,
            months,
            emi,
            status,
            date
        FROM loans
        WHERE account_no=?
        ORDER BY loan_id DESC
    """, (account_no,))

    loans = cursor.fetchall()

    if not loans:

        Label(
            window,
            text="No Loan Found",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="red"
        ).pack(pady=50)

        return

    # ==========================================
    # LOAN LIST
    # ==========================================

    loan_list = Listbox(
        window,
        width=70,
        height=15,
        font=("Arial", 11)
    )

    loan_list.pack(padx=20, pady=10)

    for loan in loans:

        loan_id = loan[0]
        loan_type = loan[1]
        amount = float(loan[2])
        interest = float(loan[3])
        months = loan[4]
        emi = float(loan[5])
        status = loan[6]

        loan_list.insert(
            "end",
            f"ID: {loan_id} | "
            f"{loan_type} | "
            f"Rs.{amount:.2f} | "
            f"EMI: Rs.{emi:.2f} | "
            f"{months} Months | "
            f"{status}"
        )

    # ==========================================
    # VIEW DETAILS
    # ==========================================

    def view_details():

        selected = loan_list.curselection()

        if not selected:

            messagebox.showerror(
                "Error",
                "Please select a loan"
            )

            return

        loan = loans[selected[0]]

        loan_id = loan[0]
        loan_type = loan[1]
        amount = float(loan[2])
        interest = float(loan[3])
        months = loan[4]
        emi = float(loan[5])
        status = loan[6]
        date = loan[7]

        messagebox.showinfo(
            "Loan Details",
            f"""
🏦 LOAN DETAILS

Loan ID       : {loan_id}
Loan Type     : {loan_type}

Loan Amount   : Rs. {amount:.2f}
Interest      : {interest:.2f}%

EMI           : Rs. {emi:.2f}
Months Left   : {months}

Status        : {status}
Applied Date  : {date}
"""
        )

    Button(
        window,
        text="📋 View Loan Details",
        bg="blue",
        fg="white",
        font=("Arial", 12, "bold"),
        width=22,
        command=view_details
    ).pack(pady=15)

    Button(
        window,
        text="Close",
        bg="red",
        fg="white",
        font=("Arial", 11, "bold"),
        width=15,
        command=window.destroy
    ).pack()



def customer_profile(account_no):

    window = Toplevel(root)
    window.title("My Profile")
    window.geometry("450x450")
    window.configure(bg="white")

    Label(
        window,
        text="MY PROFILE",
        font=("Arial",18,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=15)

    # Customer Details
    cursor.execute("""
    SELECT account_no, name, balance
    FROM accounts
    WHERE account_no = ?
    """, (account_no,))

    customer = cursor.fetchone()

    # Loan Details
    cursor.execute("""
    SELECT amount, status
    FROM loans
    WHERE account_no = ?
    ORDER BY loan_id DESC
    LIMIT 1
    """, (account_no,))

    loan = cursor.fetchone()

    if loan:
        loan_amount = loan[0]
        loan_status = loan[1]
    else:
        loan_amount = 0
        loan_status = "No Loan"

    Label(
        window,
        text=f"""
Account Number : {customer[0]}

Name : {customer[1]}

Balance : Rs. {customer[2]}

Loan Status : {loan_status}

Remaining Loan : Rs. {loan_amount}
""",
        font=("Arial",12),
        bg="white",
        justify=LEFT
    ).pack(pady=20)

    Button(
        window,
        text="Close",
        font=("Arial",12,"bold"),
        bg="red",
        fg="white",
        command=window.destroy
    ).pack(pady=15)

def open_customer_login():
    login_window = Toplevel(root)
    login_window.title("Customer Login")
    login_window.geometry("500x400")
    login_window.configure(bg="white")

    title = Label(
        login_window,
        text="CUSTOMER LOGIN",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="green"
    )
    title.pack(pady=30)

    acc_label = Label(
        login_window,
        text="Account Number",
        font=("Arial", 14),
        bg="white"
    )
    acc_label.pack()

    acc_entry = Entry(
        login_window,
        font=("Arial", 14),
        width=25
    )
    acc_entry.pack(pady=10)

    pin_label = Label(
        login_window,
        text="PIN",
        font=("Arial", 14),
        bg="white"
    )
    pin_label.pack()

    pin_entry = Entry(
        login_window,
        font=("Arial", 14),
        width=25,
        show="*"
    )
    pin_entry.pack(pady=10)

    login_btn = Button(
        login_window,
        text="Login",
        font=("Arial", 14, "bold"),
        bg="green",
        fg="white",
        width=15,
        command=lambda: customer_login(acc_entry, pin_entry)
    )
    login_btn.pack(pady=20)

    back_btn = Button(
        login_window,
        text="Back",
        font=("Arial", 12, "bold"),
        bg="red",
        fg="white",
        width=10,
        command=login_window.destroy
    )
    back_btn.pack()


def open_admin_login():
    admin = Toplevel(root)
    admin.title("Admin Login")
    admin.geometry("400x300")
    admin.configure(bg="white")

    Label(
        admin,
        text="ADMIN LOGIN",
        font=("Arial",18,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=20)

    Label(admin,text="Username",bg="white").pack()

    username_entry = Entry(admin,font=("Arial",12))
    username_entry.pack(pady=5)

    Label(admin,text="Password",bg="white").pack()

    password_entry = Entry(admin,font=("Arial",12),show="*")
    password_entry.pack(pady=5)

    Button(
        admin,
        text="Login",
        bg="blue",
        fg="white",
        font=("Arial",12,"bold"),
        command=lambda: admin_login(
            username_entry,
            password_entry,
            admin
        )
    ).pack(pady=20)


def view_atm_requests():

    window = Toplevel(root)
    window.title("ATM Requests")
    window.geometry("800x450")
    window.configure(bg="white")

    Label(
        window,
        text="ATM CARD REQUESTS",
        font=("Arial",18,"bold"),
        bg="white",
        fg="blue"
    ).pack(pady=15)

    text = Text(window, width=95, height=18)
    text.pack()

    cursor.execute("""
    SELECT
        card_id,
        account_no,
        card_number,
        card_type,
        expiry_date,
        status
    FROM atm_cards
    ORDER BY card_id DESC
    """)

    records = cursor.fetchall()

    if not records:
        text.insert(END, "No ATM Requests Found")
        text.config(state="disabled")
        return

    text.insert(
        END,
        "ID\tAcc No\tCard Type\tStatus\n"
    )
    text.insert(
        END,
        "="*60 + "\n"
    )

    for row in records:
        text.insert(
            END,
            f"{row[0]}\t{row[1]}\t{row[3]}\t\t{row[5]}\n"
        )

        frame = Frame(window, bg="white")
        frame.pack()

        Button(
            frame,
            text="Approve",
            bg="green",
            fg="white",
            command=lambda id=row[0]: update_atm_status(id, "Approved")
        ).pack(side=LEFT, padx=5)

        Button(
            frame,
            text="Reject",
            bg="red",
            fg="white",
            command=lambda id=row[0]: update_atm_status(id, "Rejected")
        ).pack(side=LEFT, padx=5)

    text.config(state="disabled")    

def update_atm_status(card_id, status):

    cursor.execute("""
    UPDATE atm_cards
    SET status=?
    WHERE card_id=?
    """, (status, card_id))

    conn.commit()

    messagebox.showinfo(
        "Success",
        f"ATM Card {status}"
    )

root = Tk()

root.title("Bank Management System")
root.geometry("900x600")
root.configure(bg="#e8f4fc")
root.resizable(False, False)

title = Label(
    root,
    text="BANK MANAGEMENT SYSTEM",
    font=("Arial",24,"bold"),
    bg="#e8f4fc",
    fg="navy"
)

title.pack(pady=30)
customer_btn = Button(
    root,
    text="Customer Login",
    font=("Arial",16,"bold"),
    bg="green",
    fg="white",
    width=20,
    height=2,
    command=open_customer_login
)
customer_btn.pack(pady=15)

admin_btn = Button(
    root,
    text="Admin Login",
    font=("Arial",16,"bold"),
    bg="blue",
    fg="white",
    width=20,
    height=2,
    command=open_admin_login
)
admin_btn.pack(pady=15)

exit_btn = Button(
    root,
    text="Exit",
    font=("Arial",16,"bold"),
    bg="red",
    fg="white",
    width=20,
    height=2,
    command=root.destroy
)

exit_btn.pack(pady=20)

print("GUI STARTING")

root.mainloop()

print("GUI CLOSED")