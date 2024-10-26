import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException

# Initialize Firebase Admin SDK
cred = credentials.Certificate("credentials/research-project-8003b-firebase-adminsdk-b4h3x-b4ea62e36f.json")
firebase_admin.initialize_app(cred)

# Function to verify the Firebase token
async def verify_token(token: str):
    try:
        # Verify the token with Firebase Admin SDK
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")
