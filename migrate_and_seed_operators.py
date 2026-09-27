import sys
import sqlite3
import os

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "travora.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Check & Add columns to 'users' table
cursor.execute("PRAGMA table_info(users)")
user_cols = [row[1] for row in cursor.fetchall()]

new_user_cols = [
    ("company_name", "TEXT"),
    ("specialties", "TEXT"),
    ("operating_destinations", "TEXT"),
    ("rating", "FLOAT DEFAULT 4.8"),
    ("tours_completed", "INTEGER DEFAULT 120"),
    ("fleet_size", "TEXT DEFAULT '12 Vehicles'"),
    ("response_time_minutes", "INTEGER DEFAULT 5"),
    ("badge", "TEXT DEFAULT 'Verified Partner'"),
    ("bio", "TEXT")
]

for col_name, col_type in new_user_cols:
    if col_name not in user_cols:
        print(f"Adding column '{col_name}' to 'users' table...")
        cursor.execute(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}")

# 2. Check & Add columns to 'tours' table
cursor.execute("PRAGMA table_info(tours)")
tour_cols = [row[1] for row in cursor.fetchall()]

new_tour_cols = [
    ("operator_id", "INTEGER"),
    ("desired_places", "TEXT"),
    ("ai_recommendation_reason", "TEXT")
]

for col_name, col_type in new_tour_cols:
    if col_name not in tour_cols:
        print(f"Adding column '{col_name}' to 'tours' table...")
        cursor.execute(f"ALTER TABLE tours ADD COLUMN {col_name} {col_type}")

conn.commit()
conn.close()

# 3. Seed the 14 operators
from backend.database import SessionLocal
from backend.seed_data import seed_operators, seed_catalog
from backend.models import Destination, User

db = SessionLocal()
if db.query(Destination).count() == 0:
    seed_catalog(db)

# Delete existing operators if any so we get clean updated profiles
db.query(User).filter(User.role == "operator").delete()
db.commit()

seed_operators(db)
db.close()

print("✓ Database migration and 14 Tour Operator seed complete!")

# 4. Re-export database view
from export_database_view import generate_database_views
generate_database_views()
