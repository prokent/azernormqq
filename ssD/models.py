from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker
from token_all import sqlite

# Создание подключения к базе данных
engine = create_engine(sqlite)
Base = declarative_base()

# Определение модели рекрутера
class Recruiter(Base):
    __tablename__ = 'recruiters'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    available = Column(Boolean, default=True)
    telegram_id = Column(Integer, unique=True, nullable=True)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    content = Column(String)
    recruiter_id = Column(Integer, nullable=True)

# Создание таблиц
Base.metadata.create_all(bind=engine)
