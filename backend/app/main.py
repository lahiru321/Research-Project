from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI
from app.routers import routes
import subprocess
import os

app = FastAPI()

app.include_router(routes.router)

engagement_process = None  # Global variable to track the subprocess

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}


@app.post("/start")
async def start_engagement_system():
    global engagement_process
    if engagement_process is None or engagement_process.poll() is not None:
        try:
            engagement_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "services", "engagement_system.py")
            engagement_process = subprocess.Popen(["python", engagement_script_path])
            return {"status": "Engagement system started"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to start engagement system: {e}")
    return {"status": "Engagement system is already running"}

@app.post("/end")
async def stop_engagement_system():
    global engagement_process
    if engagement_process and engagement_process.poll() is None:
        try:
            engagement_process.terminate()
            engagement_process = None
            return {"status": "Engagement system stopped"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to stop engagement system: {e}")
    return {"status": "Engagement system is not running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
