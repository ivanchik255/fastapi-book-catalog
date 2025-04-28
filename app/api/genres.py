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


@router.post("/genres/", response_model=schemas.Genre)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db)):
    """Создает новый жанр."""
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


@router.get("/genres/", response_model=List[schemas.Genre])
def read_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Возвращает список жанров."""
    genres = db.query(models.Genre).offset(skip).limit(limit).all()
    return genres


@router.get("/genres/{genre_id}", response_model=schemas.Genre)
def read_genre(genre_id: int, db: Session = Depends(get_db)):
    """Возвращает жанр по ID."""
    genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@router.put("/genres/{genre_id}", response_model=schemas.Genre)
def update_genre(genre_id: int, genre_update: schemas.GenreCreate, db: Session = Depends(get_db)):
    """Обновляет существующий жанр."""
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    for key, value in genre_update.dict(exclude_unset=True).items():
        setattr(db_genre, key, value)

    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


@router.delete("/genres/{genre_id}", response_model=schemas.Genre)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    """Удаляет жанр."""
    db_genre = db.query(models.Genre).filter(models.Genre.id == genre_id).first()
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")

    db.delete(db_genre)
    db.commit()
    return db_genre
