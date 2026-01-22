import os
from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv


API_KEY_NAME = "X-API-Key"
# Load environment variables from .env file (local only)
load_dotenv()

app = FastAPI()

# Configuration

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(header_value: str = Security(api_key_header)):
    API_KEY = os.getenv("MY_API_KEY")
    # --- DEBUG LOGS ---
    print(f"DEBUG: Expected Key from .env: '{API_KEY}'")
    print(f"DEBUG: Received Header Value: '{header_value}'")
    # ------------------

    if header_value == API_KEY:
        return header_value
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )


# 1. Public Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome! This is a Rishi's publicendpoint."}

# 2. Protected Endpoint
@app.get("/secret")
async def read_protected_data(api_key: str = Security(get_api_key)):
    return {
        "message": "Access Granted",
        "secret_data": "The password to the vault is: HardWorkAndConsistency"
    }
