import sys

sys.path.append("\\Users\\belko\\book_catalog\\app")

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter()


@router.post("/authors/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """Создает нового автора."""
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Возвращает список авторов."""
    authors = db.query(models.Author).offset(skip).limit(limit).all()
    return authors


@router.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    """Возвращает автора по ID."""
    author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: int, author_update: schemas.AuthorCreate, db: Session = Depends(get_db)):
    """Обновляет существующего автора."""
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in author_update.dict(exclude_unset=True).items():
        setattr(db_author, key, value)

    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.delete("/authors/{author_id}", response_model=schemas.Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Удаляет автора."""
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    db.delete(db_author)
    db.commit()
    return db_author
