from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from app.academic import start_engagement_system, stop_engagement_system
from app.sociel import get_data, submit_text, TextInput
import logging

app = FastAPI()

templates = Jinja2Templates(directory="templates")

logging.info('FastAPI server started')

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
async def start_engagement_system_endpoint():
    return await start_engagement_system()

@app.post("/end")
async def stop_engagement_system_endpoint():
    return await stop_engagement_system()




@app.get("/data", response_model=dict)
async def get_data_endpoint():
    return await get_data()

@app.post("/submit")
async def submit_text_endpoint(input: TextInput):
    return await submit_text(input)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
