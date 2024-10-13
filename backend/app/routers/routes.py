from fastapi import Depends, HTTPException
from app.auth import verify_token
from fastapi import APIRouter

router = APIRouter()

@router.get("/protected-route")
async def protected_route(token: str = Depends(verify_token)):
    # Now you have access to decoded Firebase token
    return {"message": "You have accessed a protected route!"}
