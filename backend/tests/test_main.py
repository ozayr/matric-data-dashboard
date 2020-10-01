import json
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.db.database import Base
from api.main import app, get_db
from api.db.schemas import RequestRecord

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_status():
    response = client.get("/api/status")
    assert response.status_code == 200
    assert response.json() == {"msg":"alls good in the hood"}


def test_database_write_read():
    record = {
        "emis" : 123456789,
        "centre_no" : 4221011,
        "name" :"Orient Islamic School",
        "wrote_2014" : 100,
        "passed_2014" : 100,
        "wrote_2015" : 100,
        "passed_2015" : 100,
        "wrote_2016" : 100,
        "passed_2016" : 99,
        "province" : "Kwa zulu Natal"
    }

    response = client.post("/create_record/",json=record)
    assert response.status_code == 201
    response = client.get("/records/")
    response = response.json()[0]
    assert response['emis'] == 123456789

