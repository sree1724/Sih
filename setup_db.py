import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    pin INTEGER NOT NULL,
    balance REAL NOT NULL
)
""")

# Transactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    amount REAL NOT NULL,
    type TEXT NOT NULL, -- 'credit' or 'debit'
    timestamp TEXT NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES users(id),
    FOREIGN KEY (receiver_id) REFERENCES users(id)
)
""")

conn.commit()
conn.close()
print("✅ Database setup complete")
