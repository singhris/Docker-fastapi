import requests

BASE_URL = "https://docker-fastapi-a1lx.onrender.com"

def test_root():
    print("--- Testing GET Root ---")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response JSON: {response.json()}")
    except Exception as e:
        print(f"An error occurred: {e}")

def test_post_data():
    print("\n--- Testing POST Data ---")
    endpoint = "/items" 
    payload = {
        "name": "Test Product",
        "price": 25.50,
        "is_offer": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}{endpoint}", json=payload)
        if response.status_code == 200 or response.status_code == 201:
            print("Success!")
            print(f"Response: {response.json()}")
        elif response.status_code == 404:
            print("Error 404: This endpoint does not exist. Check your main.py routes.")
        else:
            print(f"Failed with Status Code: {response.status_code}")
            print(f"Message: {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_root()
