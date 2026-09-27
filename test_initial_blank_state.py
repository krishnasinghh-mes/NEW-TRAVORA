import sys
sys.stdout.reconfigure(encoding='utf-8')
import httpx

c = httpx.Client(base_url='http://127.0.0.1:8000', timeout=10.0)

print("--- 1. Testing New User Creation & Initial Blank Itinerary State ---")
import uuid
random_email = f"new_traveler_{uuid.uuid4().hex[:6]}@travora.demo"

# Register a brand new traveler
reg_res = c.post('/api/auth/register', json={
    "name": "Rohan Sharma",
    "email": random_email,
    "password": "password123",
    "role": "traveler",
    "phone": "+91 91234 56789"
}).json()
assert reg_res['success'] is True
user_id = reg_res['user']['id']
print(f"✓ Registered brand new user: {reg_res['user']['name']} (ID #{user_id})")

# Verify user initially has 0 tours planned
tours = c.get(f'/api/tours?user_id={user_id}').json()
assert len(tours) == 0, f"Expected 0 tours initially, found {len(tours)}"
print(f"✓ Initial planned tours count for new traveler = {len(tours)} (Clean blank state)")

# Verify destinations are available for recommendations
dests = c.get('/api/destinations').json()
assert len(dests) >= 7
print(f"✓ Retrieved {len(dests)} recommended destinations for vacation inspiration: {[d['name'] for d in dests[:4]]}...")

# 2. Plan a dynamic custom tour for this user
plan_res = c.post('/api/tours/plan', json={
    "destination_name": "Goa",
    "start_date": "2026-10-01",
    "end_date": "2026-10-05",
    "travelers_count": 2,
    "budget_total": 28000.0,
    "travel_style": "Beach + Adventure + Food",
    "interests": ["Beach", "Adventure", "Food"],
    "accommodation_type": "3-Star Deluxe",
    "transport_type": "Volvo AC Sleeper Bus",
    "user_id": user_id
}).json()
assert plan_res['success'] is True
tour_id = plan_res['tour_id']
print(f"✓ Created custom dynamic itinerary for traveler: Tour ID #{tour_id} (Code: {plan_res['code']})")

# Verify the user now has exactly 1 planned tour
user_tours_after = c.get(f'/api/tours?user_id={user_id}').json()
assert len(user_tours_after) == 1
assert user_tours_after[0]['id'] == tour_id
print(f"✓ Traveler's dashboard now contains newly generated Tour #{user_tours_after[0]['code']}: {user_tours_after[0]['title']}")

print("\n==================================================================")
print("🎉 ALL INITIAL BLANK STATE AND SCOPED PLANNING TESTS PASSED!")
print("==================================================================")
