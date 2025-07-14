# init_db.py
import sqlite3
import hashlib
import os

if os.path.exists("users.db"):
    os.remove("users.db")

conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
''')

# Insert users
users = [
    ("admin", "abc123"),
    ("jack", "qwerty"),
    ("alice", "password")
]

for u, p in users:
    user_hash = hashlib.md5(u.encode()).hexdigest()
    pass_hash = hashlib.md5(p.encode()).hexdigest()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user_hash, pass_hash))

conn.commit()
conn.close()

print("✅ users.db created with sample users.")
