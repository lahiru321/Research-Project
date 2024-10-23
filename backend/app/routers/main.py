from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from fastapi import FastAPI
from app.routers import routes

app = FastAPI()

app.include_router(routes.router)


@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}