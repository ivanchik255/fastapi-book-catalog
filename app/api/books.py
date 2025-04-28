import sys

sys.path.append("\\Users\\belko\\book_catalog\\app")

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)  # Создание таблиц (если их нет)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books


@router.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(db_book, key, value)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return db_book

@router.get("/books/{book_id}/rating")
def calculate_book_rating(book_id: int, db: Session = Depends(get_db)):
    #  Здесь логика расчета рейтинга на основе отзывов
    #  Например, запрос в БД для получения отзывов и средней оценки
    #  Заглушка:
    return {"book_id": book_id, "rating": 4.5}
