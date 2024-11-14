# api_master_v1/api_master/integration_tests.py
# IMPORTANT,DATABASE FILE new_models.sqlite is api_master_v1/new_models.sqlite
import requests
import json

BASE_URL = 'http://localhost:5009/api'  # Adjust the base URL as needed

def test_create_auth():
    """Auth Test :  creating a new Auth record."""
    payload = {
        "uid": 1,
        "user_email": "test_user@example.com",
        "password_hash": "hashed_password",
        "role": "Admin"
    }
    response = requests.post(f"{BASE_URL}/auth", json=payload)
    print("Auth Test : Create Auth Response:", response.status_code, response.json())
    return response.json()

def test_get_all_auths():
    """Auth Test : retrieving all Auth records."""
    response = requests.get(f"{BASE_URL}/auth")
    print("\n\nAuth Test : Get All Auths Response:", response.status_code, response.json())
    return response.json()

def test_get_auth_by_uid(uid):
    """Auth Test : retrieving a specific Auth record by UID."""
    response = requests.get(f"{BASE_URL}/auth/{uid}")  # Assuming uid=1 exists
    print(f"fetched length is : {len(response.json())}")
    print("\n\nAuth Test : Get Auth by UID Response:", response.status_code, response.json())
    return response.json()

def test_update_auth(uid):
    """Auth Test: updating an Auth record."""
    payload = {
        "user_email": "updated_user@example.com",
        "password_hash": "new_hashed_password",
        "role": "User"
    }
    response = requests.put(f"{BASE_URL}/auth/{uid}", json=payload)  # Assuming uid=1 exists
    print("\n\nAuth Test : Update Auth Response:", response.status_code, response.json())
    return response.json()

def test_delete_auth(uid):
    """Auth Test: deleting an Auth record."""
    try:
        response = requests.delete(f"{BASE_URL}/auth/{uid}")  # Assuming uid=1 exists
        print("\n\nAuth Test :Delete Auth Response:", response.status_code)
        if response.status_code == 204:
            return True 
        else:
            return False 
    except Exception as e:
        return False

def test_reset_auth(uid):
    """Auth Test: resetting authentication for a user."""
    response = requests.post(f"{BASE_URL}/auth/reset/{uid}")  # Assuming uid=1 exists
    print("\n\nAuth Test : Reset Auth Response:", response.status_code, response.json())
    return response.json()

def test_verify_auth_token(uid, token):
    """Auth Test: verifying the authentication token for a user."""
    payload = {
        "token": token  # Assuming you have a valid token to verify
    }
    response = requests.post(f"{BASE_URL}/auth/token/verify/{uid}", json=payload)  # Assuming uid=1 exists
    print("\n\nAuth Test : Verify Auth Token Response:", response.status_code, response.json())
    return response.json()


# Location Test Functions
def test_create_location():
    """Location Test: creating a new Location record."""
    payload = {
        "uid": 1,
        "name": "Central Park",
        "location_pin_type": "park",
        "latitude": "40.785091",
        "longitude": "-73.968285",
        "user_id": 1  # Assuming a user_id is required
    }
    response = requests.post(f"{BASE_URL}/location", json=payload)
    print("\n\nLocation Test : Create Location Response:", response.status_code, response.json())
    return response.json() 


def test_get_all_locations():
    """Location Test: retrieving all Location records."""
    response = requests.get(f"{BASE_URL}/location")
    print("\n\nLocation Test : Get All Locations Response:", response.status_code, response.json())
    return response.json() 


def test_get_location_by_user_id(user_id):
    """Location Test: retrieving a specific Location record by user ID."""
    response = requests.get(f"{BASE_URL}/location/{user_id}")  # Assuming user_id=1 exists
    print("\n\nLocation Test : Get Location by User ID Response:", response.status_code, response.json())
    return response.json() 


def test_update_location(user_id):
    """Location Test: updating a Location record."""
    payload = {
        "name": "Updated Central Park",
        "location_pin_type": "park",
        "latitude": "40.785091",
        "longitude": "-73.968285"
    }
    response = requests.put(f"{BASE_URL}/location/{user_id}", json=payload)  # Assuming user_id=1 exists
    print("\n\nLocation Test : Update Location Response:", response.status_code, response.json())
    return response.json() 


def test_delete_location(user_id):
    """Location Test: deleting a Location record."""
    response = requests.delete(f"{BASE_URL}/location/{user_id}")  # Assuming user_id=1 exists
    print("\n\nLocation Test : Delete Location Response:", response.status_code)
    return response.json() 


if __name__ == "__main__":
    print("Running Integration Tests...\n")
    
    test_create_auth()
    test_get_all_auths()
    test_get_auth_by_uid()
    test_update_auth()
    test_delete_auth()
    
    # test_create_location()
    # test_get_all_locations()
    # test_get_location_by_uid()
    # test_update_location()
    # test_delete_location()