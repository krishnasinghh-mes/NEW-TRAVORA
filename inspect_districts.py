import sqlite3, json

conn = sqlite3.connect('travora.db')
cursor = conn.cursor()
districts = ['North Goa', 'South Goa', 'Mumbai City', 'Varanasi', 'Kutch', 'Shimla', 'Patna', 'Puri', 'Mathura', 'Amritsar', 'Gangtok']
for d in districts:
    row = cursor.execute("SELECT name, state, tourist_places, heritage_places, religious_places, adventure_activities, cultural_experiences, terrain FROM districts WHERE name LIKE ?", (f"%{d}%",)).fetchone()
    if row:
        print(f"=== {row[0]} ({row[1]}) - Terrain: {row[7]} ===")
        print(f"  Tourist: {row[2]}")
        print(f"  Heritage: {row[3]}")
        print(f"  Adventure: {row[5]}")
        print(f"  Cultural: {row[6]}")
        print(f"  Religious: {row[4]}")
