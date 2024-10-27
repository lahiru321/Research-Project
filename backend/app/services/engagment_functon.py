import subprocess
from fastapi import HTTPException
from app.models.learning_plan import get_learning_plan

import os
engagement_process = None  

async def start_engagement_system(request):
    global engagement_process
    data = await request.json()
    subject = data.get('subject')
    topic = data.get('topic')  

    if not subject or not topic:
        raise HTTPException(status_code=400, detail="Subject and topic are required")

    if engagement_process is None or engagement_process.poll() is not None:
        try:
            engagement_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engagement_system.py")
            engagement_process = subprocess.Popen(["python", engagement_script_path])
            return {"status": "Engagement system started", "subject": subject, "topic": topic}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to start engagement system: {e}")
    return {"status": "Engagement system is already running"}

async def stop_engagement_system(request):
    global engagement_process
    data = await request.json()
    subject = data.get('subject')
    topic = data.get('topic')
    score = data.get('score')  

    if not subject or not topic or score is None:
        raise HTTPException(status_code=400, detail="Subject, topic, and score are required")

    if engagement_process and engagement_process.poll() is None:
        try:
            engagement_process.terminate()
            engagement_process = None
            learning_plan = await get_learning_plan(score, subject, topic)
            return {"status": "Engagement system stopped", "learning_plan": learning_plan}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to stop engagement system: {e}")
    return {"status": "Engagement system is not running"}
