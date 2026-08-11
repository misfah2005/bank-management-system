import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()


# Create correct table
cursor.execute("""
CREATE TABLE atm_cards_new(

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


# Copy old data
cursor.execute("""
INSERT INTO atm_cards_new
(
account_no,
card_number,
card_type,
expiry_date,
status,
pin
)

SELECT
account_no,
card_number,
card_type,
expiry_date,
status,
pin
FROM atm_cards
""")


# Remove old table
cursor.execute("""
DROP TABLE atm_cards
""")


# Rename new table
cursor.execute("""
ALTER TABLE atm_cards_new
RENAME TO atm_cards
""")


conn.commit()
conn.close()

print("ATM TABLE FIXED")
