import sqlite3
from datetime import datetime

DB_FILE = "bank.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        pin INTEGER,
        balance REAL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER,
        receiver_id INTEGER,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (sender_id) REFERENCES users(id),
        FOREIGN KEY (receiver_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

def signup(name, pin, balance):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, pin, balance) VALUES (?, ?, ?)", (name, pin, balance))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login(name, pin):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE name=? AND pin=?", (name, pin))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_balance(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def transfer(sender_id, receiver_id, amount):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Check sender balance
    cursor.execute("SELECT balance FROM users WHERE id=?", (sender_id,))
    sender_balance = cursor.fetchone()[0]
    if sender_balance < amount:
        conn.close()
        return False

    # Update balances
    cursor.execute("UPDATE users SET balance = balance - ? WHERE id=?", (amount, sender_id))
    cursor.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, receiver_id))
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Record transactions
    cursor.execute("INSERT INTO transactions (sender_id, receiver_id, amount, type, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (sender_id, receiver_id, amount, 'debit', timestamp))
    cursor.execute("INSERT INTO transactions (sender_id, receiver_id, amount, type, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (sender_id, receiver_id, amount, 'credit', timestamp))
    
    conn.commit()
    conn.close()
    return True

def get_transactions(user_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.id, u1.name as sender, u2.name as receiver, t.amount, t.type, t.timestamp
        FROM transactions t
        LEFT JOIN users u1 ON t.sender_id = u1.id
        LEFT JOIN users u2 ON t.receiver_id = u2.id
        WHERE t.sender_id=? OR t.receiver_id=?
        ORDER BY t.timestamp DESC
    """, (user_id, user_id))
    result = cursor.fetchall()
    conn.close()
    return result

def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users")
    result = cursor.fetchall()
    conn.close()
    return result
