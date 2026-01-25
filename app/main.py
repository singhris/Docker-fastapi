import os
import jwt # This is from the 'pyjwt' package
from typing import Optional
from fastapi import FastAPI, HTTPException, Security, status, Header
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security, Depends

# 1. Load Environment Variables
load_dotenv()

app = FastAPI(title="Rishi's Secure Cloud API")

# --- Configuration & Secrets ---
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Fetch secrets from environment
MY_API_KEY = os.getenv("MY_API_KEY")
JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

# Sample Message Data
MESSAGES = [
    { "id": 1, "user_id": 1, "text": "Welcome to the platform!" },
    { "id": 2, "user_id": 2, "text": "Your report is ready for download." },
    { "id": 3, "user_id": 1, "text": "You have a new notification." },
    { "id": 4, "user_id": 3, "text": "Password will expire in 5 days." },
    { "id": 5, "user_id": 2, "text": "New login detected from a new device." },
    { "id": 6, "user_id": 3, "text": "Your subscription has been updated." }
]

# --- Dependency: API Key Validation ---
async def get_api_key(header_value: str = Security(api_key_header)):
    if header_value == MY_API_KEY:
        return header_value
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid API Key",
    )

# --- 1. Public Endpoint ---
@app.get("/")
def read_root():
    return {"message": "Welcome! This is Rishi's public endpoint."}

# --- 2. API Key Protected Endpoint ---
@app.get("/secret")
async def read_protected_data(api_key: str = Security(get_api_key)):
    return {
        "message": "Access Granted via API Key",
        "secret_data": "The password to the vault is: HardWorkAndConsistency"
    }


from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 1. This line is what makes the "Authorize" button appear in Swagger
security = HTTPBearer()

@app.get("/messages")
async def get_messages(auth: HTTPAuthorizationCredentials = Depends(security)):
    """
    The 'auth' parameter now automatically handles:
    - Looking for the 'Authorization: Bearer <token>' header.
    - Returning a 403 if the header is missing.
    - Showing the Lock Icon in Swagger UI.
    """
    token = auth.credentials  # This is your eyJ... string
    
    try:
        # 2. Decode using the SECRET from your screenshot
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        
        # 3. Extract claims (Matching your screenshot's payload keys)
        user_id = payload.get("sub")
        is_admin = payload.get("admin")  # Your screenshot uses "admin": true

        # 4. Authorization Logic
        if is_admin is True:
            return {"role": "admin", "messages": MESSAGES}
        
        # For regular users, filter by ID
        # Note: We use str() to ensure "1" matches 1 if types differ
        user_specific_messages = [
            m for m in MESSAGES if str(m["user_id"]) == str(user_id)
        ]
        
        return {
            "role": "user", 
            "user_id": user_id, 
            "messages": user_specific_messages
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token signature")