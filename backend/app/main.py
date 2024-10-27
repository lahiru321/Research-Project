from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.services.engagment_functon import start_engagement_system, stop_engagement_system
from app.database.firebase import get_learning_plans, initialize_firebase
import openai
# Load environment variables
# load_dotenv()

app = FastAPI()
openai.api_key = "sk-d0iNqax7iex9_P9TfIdzV2FJyXP1_JJ2j8rJMzVzpbT3BlbkFJ8iWXAkNLBt7myj8QB6nUYiJGNSN5zVPmMdp9-uzXkA"

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase once at the application startup
initialize_firebase()

@app.get("/learning-plans")
async def learning_plans():
    return await get_learning_plans()

@app.post("/start")
async def start_engagement(request: Request):
    return await start_engagement_system(request)

@app.post("/end")
async def end_engagement(request: Request):
    return await stop_engagement_system(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
