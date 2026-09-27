import sys
import os
import httpx

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def test_auth_and_crud_suite():
    print("==================================================================")
    print("  🚀 TESTING AUTHENTICATION & SEPARATE DATABASE CRUD SUITE")
    print("  🌐 Target URL: " + BASE_URL)
    print("==================================================================")

    client = httpx.Client(base_url=BASE_URL, timeout=10.0)

    # -------------------------------------------------------------
    # 1. TEST STRICT CREDENTIAL LOGIN & VERIFICATION
    # -------------------------------------------------------------
    print("\n--- 1. Testing Strict Password Authentication ---")

    # A) Attempt Login with Wrong Password -> MUST BE REJECTED (401)
    wrong_payload = {
        "email": "traveler@travora.demo",
        "password": "wrongpassword999",
        "role": "traveler"
    }
    r = client.post("/api/auth/login", json=wrong_payload)
    assert r.status_code == 401, f"Expected 401, got {r.status_code}"
    print("✓ [PASS] Wrong password rejected with 401 Unauthorized")

    # B) Attempt Login with Correct Password -> MUST SUCCEED (200)
    correct_traveler = {
        "email": "traveler@travora.demo",
        "password": "password123",
        "role": "traveler"
    }
    r = client.post("/api/auth/login", json=correct_traveler)
    assert r.status_code == 200, f"Login failed: {r.text}"
    user_data = r.json()["user"]
    assert user_data["email"] == "traveler@travora.demo"
    assert user_data["role"] == "traveler"
    print(f"✓ [PASS] Valid Traveler Login succeeded: {user_data['name']} ({user_data['email']})")

    # C) Operator Login with Correct Password
    correct_operator = {
        "email": "operator@travora.demo",
        "password": "password123",
        "role": "operator"
    }
    r = client.post("/api/auth/login", json=correct_operator)
    assert r.status_code == 200, f"Operator login failed: {r.text}"
    op_data = r.json()["user"]
    assert op_data["role"] == "operator"
    print(f"✓ [PASS] Valid Operator Login succeeded: {op_data['name']} ({op_data['email']})")

    # -------------------------------------------------------------
    # 2. TEST SIGNUP & USER REGISTRATION PERSISTENCE
    # -------------------------------------------------------------
    print("\n--- 2. Testing User Sign Up & Database Persistence ---")
    
    unique_email = f"explorer_{os.urandom(3).hex()}@travora.demo"
    register_payload = {
        "name": "Aryan Verma",
        "email": unique_email,
        "password": "securePass2026",
        "role": "traveler",
        "phone": "+91 99887 76655"
    }
    r = client.post("/api/auth/register", json=register_payload)
    assert r.status_code == 200, f"Registration failed: {r.text}"
    new_u = r.json()["user"]
    assert new_u["email"] == unique_email
    print(f"✓ [PASS] New User Registered: {new_u['name']} ({new_u['email']})")

    # Now login with the newly created account
    r = client.post("/api/auth/login", json={"email": unique_email, "password": "wrongpassword"})
    assert r.status_code == 401
    print("✓ [PASS] Newly registered user cannot login with wrong password")

    r = client.post("/api/auth/login", json={"email": unique_email, "password": "securePass2026", "role": "traveler"})
    assert r.status_code == 200
    print("✓ [PASS] Newly registered user logged in successfully with exact matching credentials!")

    # -------------------------------------------------------------
    # 2B. TEST FORGOT / RESET PASSWORD WITH REGISTERED MAIL
    # -------------------------------------------------------------
    print("\n--- 2B. Testing Forgot Password / Reset Password ---")

    # A) Attempt reset for un-registered mail -> MUST FAIL (404)
    r = client.post("/api/auth/reset-password", json={
        "email": "nonexistent_random_email_999@test.com",
        "new_password": "someNewPassword123"
    })
    assert r.status_code == 404, f"Expected 404, got {r.status_code}"
    print("✓ [PASS] Reset password with unregistered email correctly rejected with 404 Not Found")

    # B) Attempt reset for registered user with valid email
    reset_email = unique_email
    r = client.post("/api/auth/reset-password", json={
        "email": reset_email,
        "new_password": "brandNewUpdatedPassword2026"
    })
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    print(f"✓ [PASS] Password reset succeeded for registered email: {reset_email}")

    # C) Verify old password no longer works (401)
    r = client.post("/api/auth/login", json={
        "email": reset_email,
        "password": "securePass2026",
        "role": "traveler"
    })
    assert r.status_code == 401
    print("✓ [PASS] Old password no longer works (401 Unauthorized)")

    # D) Verify new password logs in successfully (200)
    r = client.post("/api/auth/login", json={
        "email": reset_email,
        "password": "brandNewUpdatedPassword2026",
        "role": "traveler"
    })
    assert r.status_code == 200
    print("✓ [PASS] Logged in successfully with newly updated password!")

    # -------------------------------------------------------------
    # 2C. TEST PROFILE UPDATE (NAME, EMAIL, PHONE, PASSWORD)
    # -------------------------------------------------------------
    print("\n--- 2C. Testing User Profile Update Menu ---")
    new_user_id = new_u["id"]
    new_prof_email = f"updated_{hex(hash(unique_email))[-6:]}@travora.demo"
    r = client.put("/api/auth/profile", json={
        "user_id": new_user_id,
        "name": "Aryan V. Updated",
        "email": new_prof_email,
        "phone": "+91 99999 88888",
        "new_password": "finalPassword2026"
    })
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    prof_data = r.json()["user"]
    assert prof_data["name"] == "Aryan V. Updated"
    assert prof_data["email"] == new_prof_email
    print(f"✓ [PASS] Profile updated successfully: {prof_data['name']} ({prof_data['email']})")

    # Verify login with updated profile credentials
    r = client.post("/api/auth/login", json={
        "email": new_prof_email,
        "password": "finalPassword2026",
        "role": "traveler"
    })
    assert r.status_code == 200
    print("✓ [PASS] Logged in successfully with updated profile credentials!")

    # -------------------------------------------------------------
    # 2D. TEST DELETE ACCOUNT & REVOKE ACCESS
    # -------------------------------------------------------------
    print("\n--- 2D. Testing Delete Account & Access Revocation ---")

    # A) Delete the registered account
    r = client.post("/api/auth/delete-account", json={"email": new_prof_email})
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    print(f"✓ [PASS] Account '{new_prof_email}' successfully deleted from SQLite database")

    # B) Try to login with deleted account -> MUST BE REJECTED (401)
    r = client.post("/api/auth/login", json={
        "email": new_prof_email,
        "password": "finalPassword2026",
        "role": "traveler"
    })
    assert r.status_code == 401
    err_detail = r.json().get("detail", "")
    assert "deleted" in err_detail.lower() or "not found" in err_detail.lower() or "create" in err_detail.lower()
    print("✓ [PASS] Deleted user is blocked from logging in with message: " + err_detail)

    # C) Verify DATABASE_VIEW.md was auto-updated and no longer contains reset_email
    with open("DATABASE_VIEW.md", "r", encoding="utf-8") as f:
        md_content = f.read()
    assert reset_email not in md_content, f"Deleted user {reset_email} should not be in DATABASE_VIEW.md"
    print("✓ [PASS] DATABASE_VIEW.md automatically updated and synchronized!")

    # -------------------------------------------------------------
    # 3. TEST SEPARATE DATABASE CRUD STUDIO (FULL CRUD OPERATIONS)
    # -------------------------------------------------------------
    print("\n--- 3. Testing Database CRUD Studio API ---")

    # Stats
    r = client.get("/api/crud/stats")
    assert r.status_code == 200
    stats = r.json()
    print(f"✓ [PASS] Database Stats: Users={stats['users']}, Destinations={stats['destinations']}, Hotels={stats['hotels']}, Activities={stats['activities']}, Tours={stats['tours']}")

    # CRUD on Users
    print("\n  -> Testing CRUD on 'users' table:")
    r = client.get("/api/crud/users")
    assert r.status_code == 200
    initial_users_count = len(r.json())
    print(f"     • READ: Found {initial_users_count} users in database")

    # CREATE user via CRUD
    crud_create_u = {
        "name": "Rohan Gupta",
        "email": f"rohan_{os.urandom(3).hex()}@travora.test",
        "role": "operator",
        "password": "rohanPassword456",
        "phone": "+91 91234 56789"
    }
    r = client.post("/api/crud/users", json=crud_create_u)
    assert r.status_code == 200
    created_id = r.json()["id"]
    print(f"     • CREATE: Inserted User ID #{created_id}")

    # UPDATE user via CRUD
    r = client.put(f"/api/crud/users/{created_id}", json={"name": "Rohan Gupta (Lead Operator)", "role": "operator"})
    assert r.status_code == 200
    print(f"     • UPDATE: Modified User ID #{created_id}")

    # DELETE user via CRUD
    r = client.delete(f"/api/crud/users/{created_id}")
    assert r.status_code == 200
    print(f"     • DELETE: Removed User ID #{created_id}")

    # CRUD on Destinations
    print("\n  -> Testing CRUD on 'destinations' table:")
    r = client.get("/api/crud/destinations")
    assert r.status_code == 200
    dests = r.json()
    print(f"     • READ: Found {len(dests)} destinations in database table")

    # CRUD on Vendors
    print("\n  -> Testing CRUD on 'vendors' table:")
    r = client.get("/api/crud/vendors")
    assert r.status_code == 200
    vendors = r.json()
    print(f"     • READ: Found {len(vendors)} vendors in database table")

    # CRUD on Itinerary Items
    print("\n  -> Testing CRUD on 'itinerary-items' table:")
    r = client.get("/api/crud/itinerary-items")
    assert r.status_code == 200
    items = r.json()
    print(f"     • READ: Found {len(items)} itinerary items in database table")

    print("\n==================================================================")
    print("🎉 ALL AUTHENTICATION AND DATABASE CRUD TESTS PASSED WITH 100% SUCCESS!")
    print("==================================================================")

if __name__ == "__main__":
    test_auth_and_crud_suite()
