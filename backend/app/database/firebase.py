import firebase_admin
from firebase_admin import credentials, firestore
from fastapi import HTTPException

# Initialize Firebase Admin SDK
def initialize_firebase():
    cred = credentials.Certificate("./credentials/research-project-8003b-firebase-adminsdk-b4h3x-866535bb9c.json")  
    firebase_admin.initialize_app(cred)

# Get a Firestore client
def get_firestore_client():
    return firestore.client()

async def get_learning_plans():
    try:
        db = get_firestore_client()  # Get the Firestore client here
        plans_ref = db.collection('learning_plans').stream()
        plans = []
        for plan in plans_ref:
            plans.append({**plan.to_dict(), 'id': plan.id})  
        return plans
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch learning plans: {e}")

# Initialize Firebase at the start of your application
# initialize_firebase()
