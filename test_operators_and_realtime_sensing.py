import urllib.request
import urllib.parse
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000/api"

def make_req(endpoint, method="GET", data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def run_tests():
    print("🧪 Running Tests for 14 Operators, Real-Time Landmark Sensing & AI Matchmaker...\n")

    # 1. Test Operator Listing
    print("1. Testing GET /api/operators...")
    operators = make_req("/operators")
    assert len(operators) >= 14, f"Expected at least 14 operators, got {len(operators)}"
    print(f"   ✓ Success! Found {len(operators)} registered Tour Operators.")
    for op in operators[:3]:
        print(f"     - {op['name']} ({op['company_name']}) | Rating: {op['rating']}★ | Fleet: {op['fleet_size']}")

    # 2. Test AI Matchmaker for Goa Trip with Scuba & Watersports
    print("\n2. Testing POST /api/operators/match (Goa Beach & Scuba)...")
    match_payload = {
        "destination_name": "Goa",
        "travel_style": "Beach + Adventure + Food",
        "interests": ["Beach", "Adventure"],
        "budget_total": 28000,
        "desired_places": ["Baga Beach Watersports", "Grande Island Scuba Diving & Dolphin Spotting"]
    }
    matches = make_req("/operators/match", method="POST", data=match_payload)
    assert len(matches) > 0, "Expected matched operators"
    top_match = matches[0]
    assert top_match["is_recommended"] == True
    assert top_match["match_score"] >= 90
    print(f"   ✓ Success! Top AI Recommended Match: {top_match['name']} ({top_match['company_name']})")
    print(f"     Score: {top_match['match_score']}% | Reason: {top_match['ai_recommendation_reason']}")

    # 3. Test Tour Planning with Real-Time Places Sensing
    print("\n3. Testing POST /api/tours/plan with Real-Time Sensed Places...")
    plan_payload = {
        "destination_name": "Goa",
        "start_date": "2026-09-12",
        "end_date": "2026-09-15",
        "travelers_count": 2,
        "budget_total": 30000,
        "travel_style": "Beach + Adventure + Food",
        "interests": ["Beach", "Adventure", "Food"],
        "accommodation_type": "3-Star",
        "transport_type": "Volvo Bus",
        "desired_places": ["Fort Aguada & 17th-Century Lighthouse", "Dudhsagar Waterfalls & Spice Safari"],
        "custom_places_text": "Anjuna Flea Market, Curlies Sunset Shack"
    }
    plan_res = make_req("/tours/plan", method="POST", data=plan_payload)
    assert plan_res["success"] == True
    tour_id = plan_res["tour_id"]
    print(f"   ✓ Success! Created Tour #{plan_res['code']} (ID: {tour_id})")
    print(f"     Assigned Operator: {plan_res['operator']['name']} ({plan_res['operator']['company_name']})")
    print(f"     Sensed Places: {plan_res['desired_places']}")

    # 4. Verify Tour Detail & Itinerary Schedule
    print("\n4. Testing GET /api/tours/{id}...")
    detail = make_req(f"/tours/{tour_id}")
    assert detail["operator_name"] is not None
    assert detail["desired_places"] is not None
    items = detail["itinerary_items"]
    assert len(items) >= 4, f"Expected itinerary items, got {len(items)}"
    print(f"   ✓ Success! Itinerary includes {len(items)} scheduled timeline slots.")
    for item in items[:4]:
        print(f"     - Day {item['day_number']} [{item['time_start']} - {item['time_end']}]: {item['title']} (₹{item['cost']})")

    # 5. Test Registering a New 15th Tour Operator Partner
    print("\n5. Testing POST /api/auth/register for New Tour Operator...")
    new_op_payload = {
        "name": "Karan Singhal",
        "email": f"karan.singhal.{tour_id}@travora.partner",
        "password": "partnerpass123",
        "role": "operator",
        "phone": "+91 98888 77766",
        "company_name": "Singhal Desert & Camel Caravans",
        "operating_destinations": "Jaipur, Udaipur, Jaisalmer",
        "fleet_size": "15 AC Coaches & 6 Desert Jeeps",
        "specialties": "Desert Camping, Cultural Shows, Royal Palaces"
    }
    reg_res = make_req("/auth/register", method="POST", data=new_op_payload)
    assert reg_res["success"] == True
    assert reg_res["user"]["role"] == "operator"
    assert reg_res["user"]["company_name"] == "Singhal Desert & Camel Caravans"
    # 6. Test Real-Time Places Sensing API
    print("\n6. Testing POST /api/places/sense (Real-Time Sensing & Personalization)...")
    sense_payload = {
        "destination_name": "Goa",
        "travel_style": "Beach + Adventure + Food",
        "desired_places": ["Grande Island Scuba Diving & Dolphin Spotting", "Fort Aguada & 17th-Century Lighthouse"],
        "custom_places_text": "Anjuna Flea Market, Curlies Sunset Shack"
    }
    sense_res = make_req("/places/sense", method="POST", data=sense_payload)
    assert sense_res["total_sensed"] == 4, f"Expected 4 sensed places, got {sense_res['total_sensed']}"
    assert len(sense_res["personalized_tips"]) >= 2, "Expected personalized tips"
    assert len(sense_res["matched_operators"]) >= 14, "Expected ranked operators"
    print(f"   ✓ Success! Sensed {sense_res['total_sensed']} spots. Style: {sense_res['style_breakdown']}")
    print(f"     Personalized tip: {sense_res['personalized_tips'][0]['title']} -> {sense_res['personalized_tips'][0]['tip'][:80]}...")
    print(f"     Top matched operator: {sense_res['matched_operators'][0]['name']} ({sense_res['matched_operators'][0]['match_score']}%)")

    print("\n🎉 ALL TESTS PASSED (100%)!\n")

if __name__ == "__main__":
    run_tests()
