import os
import subprocess
from fastapi import HTTPException

engagement_process = None  # Global variable to track the subprocess

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
