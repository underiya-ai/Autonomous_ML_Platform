from fastapi import FastAPI
from api.file_api import router as file_router
from api.profile_report_api import router as report_router

app = FastAPI()


@app.get("/")
def home():
    return {"message": "ML Agent API is running"}

app.include_router(file_router)
app.include_router(report_router)