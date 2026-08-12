from fastapi import FastAPI
from api.file_api import router

app = FastAPI()


@app.get("/")
def home():
    return {"message": "ML Agent API is running"}

app.include_router(router)