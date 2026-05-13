"""
Test script to verify authentication endpoints and database compatibility
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
HEALTH_ENDPOINT = f"{BASE_URL}/health"
REGISTER_ENDPOINT = f"{BASE_URL}/register"
LOGIN_ENDPOINT = f"{BASE_URL}/login"

# Test data
test_users = [
    {"username": "testuser1", "password": "password123"},
    {"username": "testuser2", "password": "securepass456"},
]


def test_health_check():
    """Test the health check endpoint"""
    print("\n=== Testing Health Check ===")
    try:
        response = requests.get(HEALTH_ENDPOINT)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("database_connected"):
                print("✓ Database is connected!")
            else:
                print("✗ Database is NOT connected!")
        return response.status_code == 200
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_register():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    all_passed = True
    
    for user in test_users:
        print(f"\nRegistering user: {user['username']}")
        try:
            response = requests.post(
                REGISTER_ENDPOINT,
                json=user
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 201:
                print(f"✓ Successfully registered {user['username']}")
            else:
                print(f"✗ Failed to register {user['username']}")
                all_passed = False
        except Exception as e:
            print(f"✗ Error: {e}")
            all_passed = False
    
    return all_passed


def test_duplicate_registration():
    """Test that duplicate registration fails"""
    print("\n=== Testing Duplicate Registration (Should Fail) ===")
    user = test_users[0]
    
    try:
        response = requests.post(
            REGISTER_ENDPOINT,
            json=user
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 400:
            print("✓ Duplicate registration correctly rejected")
            return True
        else:
            print("✗ Duplicate registration should have been rejected")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_login():
    """Test user login"""
    print("\n=== Testing User Login ===")
    all_passed = True
    
    for user in test_users:
        print(f"\nLogging in user: {user['username']}")
        try:
            response = requests.post(
                LOGIN_ENDPOINT,
                json=user
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
            if response.status_code == 200:
                print(f"✓ Successfully logged in {user['username']}")
            else:
                print(f"✗ Failed to log in {user['username']}")
                all_passed = False
        except Exception as e:
            print(f"✗ Error: {e}")
            all_passed = False
    
    return all_passed


def test_invalid_login():
    """Test login with invalid credentials"""
    print("\n=== Testing Invalid Login (Should Fail) ===")
    invalid_user = {"username": "testuser1", "password": "wrongpassword"}
    
    try:
        response = requests.post(
            LOGIN_ENDPOINT,
            json=invalid_user
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 401:
            print("✓ Invalid login correctly rejected")
            return True
        else:
            print("✗ Invalid login should have been rejected")
            return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("FastAPI Authentication Endpoints Test Suite")
    print("=" * 50)
    
    # Wait for server to be ready
    print("\nWaiting for server to be ready...")
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("✓ Server is ready!")
                break
        except:
            if i == max_retries - 1:
                print("✗ Server is not responding. Make sure it's running!")
                return
            time.sleep(1)
    
    # Run tests
    results = {
        "Health Check": test_health_check(),
        "User Registration": test_register(),
        "Duplicate Registration": test_duplicate_registration(),
        "User Login": test_login(),
        "Invalid Login": test_invalid_login(),
    }
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    total_passed = sum(1 for r in results.values() if r)
    total_tests = len(results)
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n✓ All tests passed!")
    else:
        print(f"\n✗ {total_tests - total_passed} test(s) failed")


if __name__ == "__main__":
    run_all_tests()
