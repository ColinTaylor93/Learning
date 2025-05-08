from fastapi import FastAPI, Depends
from . import database
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup():
    database.Base.metadata.create_all(bind=database.engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}