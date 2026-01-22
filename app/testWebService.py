import requests
import os
from dotenv import load_dotenv

# Load local .env so we can use the same key for testing
load_dotenv()

# 1. Update this to your actual Render URL
BASE_URL = "https://docker-fastapi-a1lx.onrender.com"

# Get the key from your local .env file
API_KEY = os.getenv("MY_API_KEY") 
API_HEADER = "X-API-Key"  # Must match the API_KEY_NAME in your main.py

def test_root():
    print("--- 1. Testing GET Root (Public) ---")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Root test passed!")
        else:
            print("❌ Root test failed.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

def test_protected_no_key():
    print("\n--- 2. Testing Protected Route (No Key) ---")
    try:
        # We purposely do NOT send headers here
        response = requests.get(f"{BASE_URL}/secret")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 403:
            print("✅ Security Check Passed! (Access correctly denied)")
        else:
            print(f"❌ Security Risk! Expected 403 but got {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

def test_protected_with_key():
    print("\n--- 3. Testing Protected Route (With Key) ---")
    
    if not API_KEY:
        print("❌ SKIPPING: No MY_API_KEY found in your local .env file.")
        return

    # Create the header dictionary
    headers = {API_HEADER: API_KEY}
    
    try:
        response = requests.get(f"{BASE_URL}/secret", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Authorized Access Passed!")
        elif response.status_code == 403:
            print("❌ Access Denied. Check if the Key on Render matches your local .env file.")
            print(f"Sending Header: {headers}")
        else:
            print(f"❌ Unexpected status: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_root()
    test_protected_no_key()
    test_protected_with_key()