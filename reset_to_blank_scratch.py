import os
import sys

# Ensure UTF-8 stdout on Windows
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.database import SessionLocal, engine, Base
from backend.models import (
    User, Destination, Hotel, Activity, Transport, Tour, ItineraryItem,
    ChangeEvent, AlternativeOption, Booking, Payment, Vendor, TourGroup, Review, Notification
)
from backend.sync_hook import auto_sync_database_views
from backend.seed_data import seed_catalog

def reset_to_scratch():
    print("==================================================================")
    print("  TRAVORA — RESETTING USERS, OPERATORS & TOURS TO SCRATCH")
    print("==================================================================")
    
    # Ensure database schema is present
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # 1. Delete all user-generated and operation records
        print("1. Deleting notifications...")
        db.query(Notification).delete()
        
        print("2. Deleting reviews...")
        db.query(Review).delete()
        
        print("3. Deleting payments...")
        db.query(Payment).delete()
        
        print("4. Deleting bookings...")
        db.query(Booking).delete()
        
        print("5. Deleting alternative options...")
        db.query(AlternativeOption).delete()
        
        print("6. Deleting change events / disruptions...")
        db.query(ChangeEvent).delete()
        
        print("7. Deleting itinerary items...")
        db.query(ItineraryItem).delete()
        
        print("8. Deleting tours...")
        db.query(Tour).delete()
        
        print("9. Deleting tour groups...")
        db.query(TourGroup).delete()
        
        print("10. Deleting ALL users and operators...")
        db.query(User).delete()
        
        db.commit()
        print("✓ All users, operators, tours, and bookings cleared successfully.")
        
        # 2. Ensure catalog (Destinations, Hotels, Activities, Transports, Vendors) exists
        if db.query(Destination).count() == 0:
            print("Seeding Indian destinations, hotels, activities, and vendors catalog...")
            seed_catalog(db)
        else:
            print(f"✓ Master catalog preserved ({db.query(Destination).count()} Destinations, {db.query(Hotel).count()} Hotels, {db.query(Activity).count()} Activities, {db.query(Vendor).count()} Vendors).")
        
        print("\n--- Final Database Status ---")
        print(f"  Users (Travelers + Operators): {db.query(User).count()} (Clean Blank State)")
        print(f"  Tours:                        {db.query(Tour).count()}")
        print(f"  Bookings:                     {db.query(Booking).count()}")
        print(f"  Destinations:                 {db.query(Destination).count()}")
        print(f"  Hotels:                       {db.query(Hotel).count()}")
        print(f"  Activities:                   {db.query(Activity).count()}")
        print("==================================================================")
        
    finally:
        db.close()

    # Re-export clean database markdown and HTML views
    print("\nRegenerating DATABASE_VIEW.md and DATABASE_VIEW.html...")
    auto_sync_database_views()
    print("✓ Database views updated successfully.")

if __name__ == "__main__":
    reset_to_scratch()
