import sys
sys.path.append("\\Users\\belko\\book_catalog\\app")
from fastapi import FastAPI
from api import books, authors, genres
from auth import users

app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(genres.router)
app.include_router(users.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Book Catalog API!"}


