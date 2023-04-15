from dotenv import dotenv_values
from fastapi import FastAPI
from pymongo import MongoClient
from routes import router as seg_router

# run with python -m uvicorn main:app --reload

config = dotenv_values(".env")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(seg_router, tags=["segments"], prefix="/seg")


print(seg_router)