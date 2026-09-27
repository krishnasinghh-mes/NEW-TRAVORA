import sqlite3

conn = sqlite3.connect('travora.db')
cur = conn.cursor()
admins = cur.execute("SELECT id, name, email, role, password_hash FROM users WHERE role='admin'").fetchall()
print("Admins:", admins)
corp = cur.execute("SELECT id, name, email, role, password_hash FROM users WHERE role='business_operator'").fetchall()
print("Corporate:", corp)
