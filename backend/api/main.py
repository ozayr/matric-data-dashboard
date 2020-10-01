from typing import List,Dict,Any
import pandas as pd
import shutil
import os

from fastapi import Depends, FastAPI, HTTPException,UploadFile,File,Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from api.db.models import DataBaseRecord,Base
from api.db.schemas import RequestRecord,ResponseRecord
from api.db.database import SessionLocal, engine

from api.api import api

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get("/records/", response_model=List[ResponseRecord])
def show_records(db: Session = Depends(get_db)):
    return api.show_records(db)

@app.get("/record/{emis_id}", response_model=ResponseRecord)
def show_record(emis_id: int , db: Session = Depends(get_db)):
    return api.show_record(emis_id,db)

@app.get("/get_charts/")
def deliver_charts(db: Session = Depends(get_db)):
    return api.deliver_charts(db)

@app.post("/create_record/",status_code=201)
def create_record(request: RequestRecord,db: Session = Depends(get_db)):
    return api.create_record(request,db)

@app.get("/api/status/",status_code=200)
def status():
    return {"msg":"alls good in the hood"}