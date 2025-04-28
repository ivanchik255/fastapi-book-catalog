from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./book_catalog.db"  # Путь к базе данных SQLite

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Подключение к БД

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Создание сессии

Base = declarative_base()  # Базовый класс для моделей
