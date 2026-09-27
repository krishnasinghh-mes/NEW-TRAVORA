import sqlite3

conn = sqlite3.connect('travora.db')
c = conn.cursor()
updates = [
    ('/static/assets/destinations/goa_beach_sunset.jpg', '%Goa%'),
    ('/static/assets/destinations/jaipur_royal_palace.jpg', '%Jaipur%'),
    ('/static/assets/destinations/kerala_houseboat_lake.jpg', '%Kerala%'),
    ('/static/assets/destinations/manali_snow_peaks.jpg', '%Manali%'),
    ('/static/assets/destinations/udaipur_lake_palace.jpg', '%Udaipur%'),
    ('/static/assets/destinations/kashmir_snow_resort.jpg', '%Kashmir%'),
    ('/static/assets/destinations/varanasi_ganga_ghats.jpg', '%Rishikesh%'),
    ('/static/assets/destinations/varanasi_ganga_ghats.jpg', '%Varanasi%'),
    ('/static/assets/destinations/andaman_havelock_beach.jpg', '%Andaman%')
]
for img, pattern in updates:
    c.execute('UPDATE destinations SET image_url = ? WHERE name LIKE ?', (img, pattern))
conn.commit()
rows = c.execute('SELECT id, name, image_url FROM destinations').fetchall()
print('Updated destinations:')
for r in rows:
    print(r)
conn.close()
