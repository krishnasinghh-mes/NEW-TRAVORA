#!/usr/bin/env python
"""
==============================================================================
TRAVORA DATABASE MANAGEMENT & CRUD STUDIO (CLI)
==============================================================================
Command-line interface to inspect, create, update, and delete all records 
directly in the SQLite database (travora.db) in formatted, readable tables.

Usage:
  python manage_db.py stats
  python manage_db.py list users
  python manage_db.py list destinations
  python manage_db.py list hotels
  python manage_db.py list activities
  python manage_db.py list tours
  python manage_db.py list itinerary [--tour-id 1]
  python manage_db.py list vendors
  python manage_db.py list bookings
  python manage_db.py list reviews
  python manage_db.py add user --name "John" --email "john@travora.demo" --role traveler --password "pass123"
  python manage_db.py delete user <ID>
  python manage_db.py interactive
==============================================================================
"""

import sys
import os
import argparse
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from backend.database import SessionLocal, engine, Base
from backend.models import (
    User, Destination, Hotel, Activity, Transport, Tour, ItineraryItem,
    ChangeEvent, AlternativeOption, Booking, Payment, Vendor, TourGroup, Review, Notification
)
from backend.auth_utils import hash_password, verify_password

def print_table(headers, rows, title=None):
    """Prints a clean, properly formatted ASCII table with dynamic column widths."""
    if title:
        print("\n" + "=" * 90)
        print(f"  📊 {title.upper()}")
        print("=" * 90)

    if not rows:
        print("  (No records found)")
        print("-" * 90)
        return

    # Calculate column widths
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val) if val is not None else "-"))

    # Header format
    header_line = " | ".join(f"{str(h):<{col_widths[i]}}" for i, h in enumerate(headers))
    separator_line = "-+-".join("-" * col_widths[i] for i in range(len(headers)))

    print(f" {header_line} ")
    print(f"-{separator_line}-")

    for row in rows:
        row_line = " | ".join(f"{str(val if val is not None else '-'):<{col_widths[i]}}" for i, val in enumerate(row))
        print(f" {row_line} ")
    print("-" * (len(header_line) + 2))
    print(f" Total Records: {len(rows)}\n")

# --- LIST COMMANDS ---

def cmd_stats():
    db = SessionLocal()
    headers = ["Table Name", "Record Count", "Entity Description"]
    rows = [
        ["users", db.query(User).count(), "Registered Travelers & Tour Operators"],
        ["destinations", db.query(Destination).count(), "Curated Indian Travel Destinations"],
        ["hotels", db.query(Hotel).count(), "Accommodations & Star Ratings"],
        ["activities", db.query(Activity).count(), "Curated Experiences & Adventures"],
        ["transports", db.query(Transport).count(), "Buses, Cabs & Transit Options"],
        ["tours", db.query(Tour).count(), "Personalized Generated Itineraries"],
        ["itinerary_items", db.query(ItineraryItem).count(), "Day-by-day Itinerary Schedule Items"],
        ["vendors", db.query(Vendor).count(), "Supply Chain Hotel/Transport Partners"],
        ["tour_groups", db.query(TourGroup).count(), "Active Operational Batch Groups"],
        ["bookings", db.query(Booking).count(), "Confirmed Tour Reservations"],
        ["change_events", db.query(ChangeEvent).count(), "Disruptions & AI Adaptations"],
        ["reviews", db.query(Review).count(), "Customer Ratings & Reviews"],
        ["notifications", db.query(Notification).count(), "Real-time Platform Alerts"]
    ]
    db.close()
    print_table(headers, rows, "TRAVORA Database Summary Statistics")

def cmd_list_users():
    db = SessionLocal()
    users = db.query(User).order_by(User.id).all()
    headers = ["ID", "Name", "Email", "Role", "Company / Agency", "Rating", "Fleet / Phone"]
    rows = [
        [
            u.id, 
            u.name, 
            u.email, 
            u.role.upper(), 
            u.company_name or "-", 
            f"{u.rating}★" if u.role == "operator" else "-",
            u.fleet_size if u.role == "operator" else (u.phone or "-")
        ]
        for u in users
    ]
    db.close()
    print_table(headers, rows, "Users & Operators Table (users)")

def cmd_list_destinations():
    db = SessionLocal()
    dests = db.query(Destination).order_by(Destination.id).all()
    headers = ["ID", "Name", "State", "Starting Price", "Travel Styles", "Score", "Season"]
    rows = [
        [d.id, d.name, d.state, f"₹{d.starting_price:,.0f}", d.travel_styles, f"{d.match_score}%", d.popular_season]
        for d in dests
    ]
    db.close()
    print_table(headers, rows, "Destinations Table (destinations)")

def cmd_list_hotels():
    db = SessionLocal()
    hotels = db.query(Hotel).order_by(Hotel.id).all()
    headers = ["ID", "Name", "Destination", "Stars", "Price/Night", "Rating", "Availability", "Beach Prox."]
    rows = [
        [h.id, h.name, h.destination.name if h.destination else h.destination_id, f"{h.stars}★", f"₹{h.price_per_night:,.0f}", f"{h.rating}★", h.availability_status.capitalize(), h.beach_proximity or "-"]
        for h in hotels
    ]
    db.close()
    print_table(headers, rows, "Hotels Table (hotels)")

def cmd_list_activities():
    db = SessionLocal()
    acts = db.query(Activity).order_by(Activity.id).all()
    headers = ["ID", "Name", "Destination", "Category", "Duration", "Price", "Rating", "Default Slot"]
    rows = [
        [a.id, a.name, a.destination.name if a.destination else a.destination_id, a.category, f"{a.duration_hours}h", f"₹{a.price:,.0f}", f"{a.rating}★", a.time_slot_default or "-"]
        for a in acts
    ]
    db.close()
    print_table(headers, rows, "Activities Table (activities)")

def cmd_list_tours():
    db = SessionLocal()
    tours = db.query(Tour).order_by(Tour.id).all()
    headers = ["ID", "Code", "Customer", "Destination", "Days", "Travelers", "Budget", "Billed Cost", "Status"]
    rows = [
        [t.id, t.code, t.user.name if t.user else "Customer", t.destination.name if t.destination else "Goa", t.duration_days, t.travelers_count, f"₹{t.budget_total:,.0f}", f"₹{t.estimated_cost:,.0f}", t.status.upper()]
        for t in tours
    ]
    db.close()
    print_table(headers, rows, "Tours Table (tours)")

def cmd_list_itinerary(tour_id=None):
    db = SessionLocal()
    query = db.query(ItineraryItem)
    if tour_id:
        query = query.filter(ItineraryItem.tour_id == tour_id)
    items = query.order_by(ItineraryItem.tour_id, ItineraryItem.day_number, ItineraryItem.order_index).all()
    headers = ["ID", "Tour ID", "Day", "Type", "Title", "Time Slot", "Cost", "Location", "Disrupted?"]
    rows = [
        [it.id, it.tour_id, f"Day {it.day_number}", it.item_type.capitalize(), it.title, f"{it.time_start} - {it.time_end}", f"₹{it.cost:,.0f}", it.location_name, "⚠️ YES" if it.is_disrupted else "Normal"]
        for it in items
    ]
    db.close()
    print_table(headers, rows, f"Itinerary Items Table (itinerary_items){' for Tour #' + str(tour_id) if tour_id else ''}")

def cmd_list_vendors():
    db = SessionLocal()
    vendors = db.query(Vendor).order_by(Vendor.id).all()
    headers = ["ID", "Vendor Name", "Category", "Rating", "Availability", "Price Range", "Contact", "Location"]
    rows = [
        [v.id, v.name, v.category, f"{v.rating}★", v.availability, v.price_range, v.contact, v.location]
        for v in vendors
    ]
    db.close()
    print_table(headers, rows, "Vendors Table (vendors)")

def cmd_list_bookings():
    db = SessionLocal()
    bookings = db.query(Booking).order_by(Booking.id).all()
    headers = ["ID", "Booking Code", "Customer", "Tour Code", "Amount Paid", "Payment Status", "Booking Status", "Date"]
    rows = [
        [b.id, b.booking_code, b.user.name if b.user else "Customer", b.tour.code if b.tour else "-", f"₹{b.amount_paid:,.0f}", b.payment_status.upper(), b.booking_status.upper(), b.created_at.strftime("%Y-%m-%d %H:%M") if b.created_at else "-"]
        for b in bookings
    ]
    db.close()
    print_table(headers, rows, "Bookings Table (bookings)")

def cmd_list_reviews():
    db = SessionLocal()
    reviews = db.query(Review).order_by(Review.id).all()
    headers = ["ID", "Customer", "Tour ID", "Overall", "Hotel", "Activity", "Transport", "Operator", "Comment Snippet"]
    rows = [
        [r.id, r.user.name if r.user else "Customer", r.tour_id, f"{r.overall_rating}★", f"{r.hotel_rating}★", f"{r.activity_rating}★", f"{r.transport_rating}★", f"{r.operator_rating}★", (r.comment[:40] + "...") if len(r.comment) > 40 else r.comment]
        for r in reviews
    ]
    db.close()
    print_table(headers, rows, "Reviews Table (reviews)")

# --- CREATE COMMANDS ---

def cmd_add_user(name, email, role, password, phone):
    db = SessionLocal()
    email_clean = email.strip().lower()
    existing = db.query(User).filter(User.email.ilike(email_clean)).first()
    if existing:
        print(f"❌ Error: User with email '{email_clean}' already exists (ID #{existing.id}).")
        db.close()
        return
    
    user = User(
        name=name.strip(),
        email=email_clean,
        role=role.lower() if role.lower() in ["traveler", "operator"] else "traveler",
        password_hash=hash_password(password),
        phone=phone.strip() if phone else "+91 98765 43210",
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"✓ [SUCCESS] Created new user: ID #{user.id} | {user.name} ({user.email}) | Role: {user.role.upper()}")
    db.close()

def cmd_delete_record(table_name, record_id):
    db = SessionLocal()
    model_map = {
        "user": User, "users": User,
        "destination": Destination, "destinations": Destination,
        "hotel": Hotel, "hotels": Hotel,
        "activity": Activity, "activities": Activity,
        "tour": Tour, "tours": Tour,
        "item": ItineraryItem, "itinerary": ItineraryItem,
        "vendor": Vendor, "vendors": Vendor,
        "booking": Booking, "bookings": Booking,
        "review": Review, "reviews": Review
    }
    model = model_map.get(table_name.lower())
    if not model:
        print(f"❌ Error: Unknown table '{table_name}'. Available: users, destinations, hotels, activities, tours, itinerary, vendors, bookings, reviews.")
        db.close()
        return

    rec = db.query(model).filter(model.id == record_id).first()
    if not rec:
        print(f"❌ Error: Record ID #{record_id} not found in table '{table_name}'.")
        db.close()
        return

    db.delete(rec)
    db.commit()
    print(f"✓ [SUCCESS] Deleted record ID #{record_id} from table '{table_name}'.")
    db.close()

def cmd_reset_scratch():
    from reset_to_blank_scratch import reset_to_scratch
    reset_to_scratch()

# --- INTERACTIVE TERMINAL MENU ---

def cmd_interactive():
    print("=" * 60)
    print("  TRAVORA Database Studio — Interactive CLI")
    print("=" * 60)
    while True:
        print("\nSelect an operation:")
        print(" 1. View Database Summary (Stats)")
        print(" 2. List Users")
        print(" 3. List Destinations")
        print(" 4. List Hotels")
        print(" 5. List Activities")
        print(" 6. List Tours")
        print(" 7. List Itinerary Items")
        print(" 8. List Vendors")
        print(" 9. List Bookings")
        print(" 10. List Reviews")
        print(" 11. Add New User")
        print(" 12. Delete a Record")
        print(" 13. Reset All Users & Start From Scratch")
        print(" 0. Exit")
        
        choice = input("\nEnter choice (0-12): ").strip()
        if choice == "0":
            print("Exiting Database Studio. Goodbye!")
            break
        elif choice == "1": cmd_stats()
        elif choice == "2": cmd_list_users()
        elif choice == "3": cmd_list_destinations()
        elif choice == "4": cmd_list_hotels()
        elif choice == "5": cmd_list_activities()
        elif choice == "6": cmd_list_tours()
        elif choice == "7":
            tid = input("Enter Tour ID (or leave blank for all): ").strip()
            cmd_list_itinerary(int(tid) if tid.isdigit() else None)
        elif choice == "8": cmd_list_vendors()
        elif choice == "9": cmd_list_bookings()
        elif choice == "10": cmd_list_reviews()
        elif choice == "11":
            name = input("Enter Full Name: ").strip()
            email = input("Enter Email Address: ").strip()
            role = input("Enter Role (traveler/operator) [traveler]: ").strip() or "traveler"
            password = input("Enter Password: ").strip() or "password123"
            phone = input("Enter Phone [+91 98765 43210]: ").strip() or "+91 98765 43210"
            if name and email:
                cmd_add_user(name, email, role, password, phone)
            else:
                print("❌ Name and Email are required.")
        elif choice == "12":
            tbl = input("Enter table name (users/destinations/hotels/activities/tours/vendors/reviews): ").strip()
            rid = input("Enter Record ID to delete: ").strip()
            if tbl and rid.isdigit():
                cmd_delete_record(tbl, int(rid))
            else:
                print("❌ Invalid input.")
        elif choice == "13":
            confirm = input("Are you sure you want to remove ALL users/operators and start from scratch? (y/N): ").strip().lower()
            if confirm == "y":
                cmd_reset_scratch()

def main():
    parser = argparse.ArgumentParser(description="TRAVORA Database Management & CRUD Studio")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # stats
    subparsers.add_parser("stats", help="Show summary counts for all tables")

    # reset-scratch
    subparsers.add_parser("reset-scratch", help="Remove all users, operators, and user data to start from scratch")

    # list
    list_parser = subparsers.add_parser("list", help="List records from a table in a formatted table")
    list_parser.add_argument("table", choices=["users", "destinations", "hotels", "activities", "tours", "itinerary", "vendors", "bookings", "reviews"])
    list_parser.add_argument("--tour-id", type=int, help="Optional tour ID filter for itinerary items")

    # add
    add_parser = subparsers.add_parser("add", help="Add a new record")
    add_sub = add_parser.add_subparsers(dest="entity", help="Entity to add")
    
    add_user_p = add_sub.add_parser("user", help="Add new user")
    add_user_p.add_argument("--name", required=True, help="Full name")
    add_user_p.add_argument("--email", required=True, help="Email address")
    add_user_p.add_argument("--role", default="traveler", choices=["traveler", "operator"], help="Role")
    add_user_p.add_argument("--password", default="password123", help="Password")
    add_user_p.add_argument("--phone", default="+91 98765 43210", help="Phone number")

    # delete
    del_parser = subparsers.add_parser("delete", help="Delete a record by table name and ID")
    del_parser.add_argument("table", help="Table name")
    del_parser.add_argument("id", type=int, help="Record ID")

    # interactive
    subparsers.add_parser("interactive", help="Start interactive CLI manager")

    args = parser.parse_args()

    if args.command == "stats":
        cmd_stats()
    elif args.command == "reset-scratch":
        cmd_reset_scratch()
    elif args.command == "list":
        if args.table == "users": cmd_list_users()
        elif args.table == "destinations": cmd_list_destinations()
        elif args.table == "hotels": cmd_list_hotels()
        elif args.table == "activities": cmd_list_activities()
        elif args.table == "tours": cmd_list_tours()
        elif args.table == "itinerary": cmd_list_itinerary(args.tour_id)
        elif args.table == "vendors": cmd_list_vendors()
        elif args.table == "bookings": cmd_list_bookings()
        elif args.table == "reviews": cmd_list_reviews()
    elif args.command == "add":
        if args.entity == "user":
            cmd_add_user(args.name, args.email, args.role, args.password, args.phone)
    elif args.command == "delete":
        cmd_delete_record(args.table, args.id)
    elif args.command == "interactive":
        cmd_interactive()
    else:
        # Default action: show stats and help
        cmd_stats()
        print("Run 'python manage_db.py --help' or 'python manage_db.py interactive' for more commands.")

if __name__ == "__main__":
    main()
