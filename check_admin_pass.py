from backend.auth_utils import verify_password
import sqlite3

conn = sqlite3.connect('travora.db')
h = conn.cursor().execute("SELECT password_hash FROM users WHERE role='admin'").fetchone()[0]
print("Admin pass verify password123:", verify_password("password123", h))
print("Admin pass verify admin123:", verify_password("admin123", h))
print("Admin pass verify admin:", verify_password("admin", h))
