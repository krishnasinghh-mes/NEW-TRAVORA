import sys
import os
import httpx

# Ensure UTF-8 stdout on Windows
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def test_full_system():
    print("==================================================================")
    print("  🚀 RUNNING COMPREHENSIVE END-TO-END SYSTEM VERIFICATION")
    print("  🌐 Target URL: " + BASE_URL)
    print("==================================================================")
    
    client = httpx.Client(base_url=BASE_URL, timeout=10.0)

    # 1. Test Static Index & HTML Shell
    r = client.get("/")
    assert r.status_code == 200, f"Root returned {r.status_code}"
    assert "TRAVORA" in r.text
    print("✓ [PASS] Static HTML Shell loaded successfully")

    # 2. Test CSS & JS Asset Availability
    r = client.get("/static/css/style.css")
    assert r.status_code == 200
    assert "--primary-600" in r.text
    print("✓ [PASS] Design System CSS tokens accessible")

    r = client.get("/static/js/app.js")
    assert r.status_code == 200
    assert "renderApp" in r.text
    print("✓ [PASS] Modular JavaScript SPA application bundle accessible")

    # 3. Test Destinations API
    r = client.get("/api/destinations")
    assert r.status_code == 200
    destinations = r.json()
    assert len(destinations) >= 7
    dest_names = [d["name"] for d in destinations]
    print(f"✓ [PASS] Loaded {len(destinations)} Indian destinations: {', '.join(dest_names[:5])}...")

    # 4. Test Tour Detail
    tours_list = client.get("/api/tours").json()
    assert len(tours_list) > 0, "No tours found"
    active_tour_id = tours_list[0]["id"]
    r = client.get(f"/api/tours/{active_tour_id}")
    assert r.status_code == 200
    tour = r.json()
    assert len(tour["itinerary_items"]) > 0
    print(f"✓ [PASS] Retrieved Tour #{tour['code']}: {tour['title']} (Items: {len(tour['itinerary_items'])})")
    print(f"   • Budget: ₹{tour['budget_total']:,.2f} | Billed: ₹{tour['estimated_cost']:,.2f} | Match: {tour['match_percentage']}%")

    # 5. Test 9-Step Dynamic Trip Planning API
    plan_payload = {
        "destination_name": "Kerala",
        "start_date": "2026-09-14",
        "end_date": "2026-09-18",
        "travelers_count": 2,
        "budget_total": 30000.0,
        "travel_style": "Nature + Relaxed + Wellness",
        "interests": ["Nature", "Wellness", "Food"],
        "accommodation_type": "4-Star Resort",
        "transport_type": "Express Train",
        "user_id": 1
    }
    r = client.post("/api/tours/plan", json=plan_payload)
    assert r.status_code == 200, f"Plan failed: {r.text}"
    plan_res = r.json()
    assert plan_res["success"] is True
    new_tour_id = plan_res["tour_id"]
    print(f"✓ [PASS] AI Personalized Tour Generator created Tour #{plan_res['code']} (ID: {new_tour_id})")

    # 6. Test Interactive Component Mutation
    items = tour["itinerary_items"]
    target_item = items[2]
    update_payload = {
        "item_id": target_item["id"],
        "new_title": "VIP Sunset Beachside Cabana Stroll",
        "new_cost": 500.0
    }
    r = client.put(f"/api/tours/{active_tour_id}/update-item", json=update_payload)
    assert r.status_code == 200
    mut_res = r.json()
    print(f"✓ [PASS] Interactive Itinerary Mutation updated item cost to ₹{mut_res['pricing']['total']:,.2f}")

    # 7. Test The Signature Disruption Simulation
    r = client.post(f"/api/tours/{active_tour_id}/disrupt")
    assert r.status_code == 200
    disrupt_res = r.json()
    change_event_id = disrupt_res["change_event_id"]
    print(f"✓ [PASS] Signature Disruption Triggered (Event ID: {change_event_id})")

    # Fetch updated tour with alternatives
    r = client.get(f"/api/tours/{active_tour_id}")
    tour_after_disrupt = r.json()
    assert len(tour_after_disrupt["change_events"]) > 0
    event = next((e for e in tour_after_disrupt["change_events"] if e["id"] == change_event_id), tour_after_disrupt["change_events"][0])
    print(f"   • Detected Event: {event['title']}")
    print(f"   • Impact Analysis: {event['impact_summary']}")
    assert len(event["alternatives"]) == 3
    for alt in event["alternatives"]:
        print(f"     -> {alt['title']} | Score: {alt['overall_score']}% | Price Delta: ₹{alt['price_delta']:+} | Recommended: {alt['is_recommended']}")

    # 8. Test One-Click Alternative Approval
    rec_alt = [a for a in event["alternatives"] if a["is_recommended"]][0]
    apply_payload = {
        "change_event_id": change_event_id,
        "alternative_id": rec_alt["id"]
    }
    r = client.post("/api/changes/apply", json=apply_payload)
    assert r.status_code == 200
    apply_res = r.json()
    assert apply_res["success"] is True
    print(f"✓ [PASS] Approved Alternative: {apply_res['message']} (New Total: ₹{apply_res['new_estimated_cost']:,.2f})")

    # 9. Test Operator Dashboard & KPIs
    r = client.get("/api/operator/dashboard")
    assert r.status_code == 200
    op_dash = r.json()
    assert "kpis" in op_dash
    print(f"✓ [PASS] Operator Control Center KPIs: Active Tours: {op_dash['kpis']['active_tours']}, Check-ins: {op_dash['kpis']['today_checkins']}, Revenue: {op_dash['kpis']['revenue']}")

    # 10. Test Operator Alerts, Vendors, and Groups
    r = client.get("/api/operator/alerts")
    assert r.status_code == 200
    print(f"✓ [PASS] Alerts Feed: {len(r.json())} active operational alerts monitored")

    r = client.get("/api/operator/vendors")
    assert r.status_code == 200
    print(f"✓ [PASS] Vendor Directory: {len(r.json())} supply chain partners active")

    r = client.get("/api/operator/groups")
    assert r.status_code == 200
    print(f"✓ [PASS] Tour Groups: {len(r.json())} active tour groups with assigned coordinators")

    # 11. Test Operator Analytics
    r = client.get("/api/operator/analytics")
    assert r.status_code == 200
    analytics = r.json()
    assert "destinations_share" in analytics
    print(f"✓ [PASS] Analytics Engine: Success Rate {analytics['overview']['successful_operations_rate']}%, Avg Resolution: {analytics['overview']['avg_resolution_minutes']}m")

    # 12. Test Travora AI Copilot
    ai_queries = [
        "Make my trip cheaper",
        "Add more adventure activities",
        "Why did you recommend this hotel?"
    ]
    for q in ai_queries:
        r = client.post("/api/ai/chat", json={"message": q, "tour_id": active_tour_id, "context_type": "traveler"})
        assert r.status_code == 200
        ai_res = r.json()
        print(f"✓ [PASS] AI Copilot Prompt: '{q}' -> {ai_res['reply'][:65]}...")

    # 13. Test Booking & Mock Checkout
    book_payload = {
        "tour_id": active_tour_id,
        "user_id": 1,
        "payment_method": "UPI (Google Pay)",
        "contact_phone": "+91 98765 43210"
    }
    r = client.post("/api/tours/book", json=book_payload)
    assert r.status_code == 200
    book_res = r.json()
    print(f"✓ [PASS] Tour Checkout: Booking Code {book_res['booking_code']} (Amount: ₹{book_res['amount_paid']:,.2f})")

    # 14. Test Reviews Submission
    review_payload = {
        "tour_id": active_tour_id,
        "user_id": 1,
        "overall_rating": 5.0,
        "hotel_rating": 4.8,
        "activity_rating": 5.0,
        "transport_rating": 4.7,
        "operator_rating": 5.0,
        "comment": "Outstanding dynamic tour adaptation! When Day 2 hotel changed, TRAVORA immediately replaced it with Hotel Paradise with zero delay."
    }
    r = client.post("/api/reviews", json=review_payload)
    assert r.status_code == 200
    print("✓ [PASS] Customer Review & Rating submitted successfully")

    print("==================================================================")
    print("🎉 ALL 14 FULL-STACK END-TO-END SYSTEM TESTS PASSED PERFECTLY!")
    print("==================================================================")

if __name__ == "__main__":
    test_full_system()
