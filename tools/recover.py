import sqlite3

source = "bank_old.db"
target = "recovered.db"

try:
    source_db = sqlite3.connect(source)
    target_db = sqlite3.connect(target)

    source_db.backup(target_db)

    source_db.close()
    target_db.close()

    print("Backup completed successfully")

except Exception as e:
    print("Recovery failed:", e)