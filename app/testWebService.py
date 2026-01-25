import requests
import os
from dotenv import load_dotenv

# Load local .env
load_dotenv()

# 1. Configuration
BASE_URL = "https://docker-fastapi-a1lx.onrender.com"
API_KEY = os.getenv("MY_API_KEY") 
JWT_TOKEN = os.getenv("TEST_JWT_TOKEN") # The long eyJ... string from JWT.io
API_HEADER = "X-API-Key"

def test_root():
    print("--- 1. Testing Public Endpoint ---")
    url = f"{BASE_URL}/"
    print(f"URL: {url}")
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        if response.status_code == 200:
            print("✅ Root test passed!")
    except Exception as e:
        print(f"An error occurred: {e}")

def test_api_key_protected():
    print("\n--- 2. Testing API Key Protected Endpoint ---")
    url = f"{BASE_URL}/secret"
    print(f"URL: {url}")
    
    # Test No Key
    print("Sub-test: No Key")
    res_no_key = requests.get(url)
    print(f"Status: {res_no_key.status_code} (Expected 403)")

    # Test With Key
    if API_KEY:
        print("Sub-test: With Key")
        headers = {API_HEADER: API_KEY}
        res_key = requests.get(url, headers=headers)
        print(f"Status: {res_key.status_code}")
        print(f"Response: {res_key.json()}")
        if res_key.status_code == 200:
            print("✅ API Key test passed!")

def test_jwt_messages():
    print("\n--- 3. Testing JWT Protected Endpoint (/messages) ---")
    url = f"{BASE_URL}/messages"
    print(f"URL: {url}")

    if not JWT_TOKEN:
        print("❌ SKIPPING: No TEST_JWT_TOKEN found in your .env")
        return

    # Use Bearer token format
    headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ JWT test passed!")
        else:
            print(f"❌ JWT test failed with status {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_root()
    test_api_key_protected()
    test_jwt_messages()