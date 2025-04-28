import sys
sys.path.append("\\Users\\belko\\book_catalog\\app")

sys.path.append("\\Users\\belko\\book_catalog")


from fastapi.testclient import TestClient
from main import app
import models
from db import SessionLocal, engine

client = TestClient(app)

def setup_db():
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    models.Base.metadata.drop_all(bind=engine)

def test_create_book():
    response = client.post(
        "/books/",
        json={"title": "Test Book", "description": "Test Description", "author_id": 1, "genre_id": 1},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Book"

def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200
