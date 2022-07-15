from venv import create
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = 'db'
DBNAME = 'fastapi_db'
USER = 'admin'
PASSWORD = 'password'

DATABASE = f'mysql://{USER}:{PASSWORD}@{HOST}/{DBNAME}?charset=utf8' 

engine = create_engine(DATABASE, encoding='utf-8', echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
