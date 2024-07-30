import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import config
from fastapi import FastAPI
import json



DB_HOST = config["DB_HOST"]
DB_USER = config["DB_USER"]
DB_PORT = config["DB_PORT"]
DB_PASS = config["DB_PASS"]
# Database connection string

DB_CONN = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/chatbot"
# 필요한 라이브러리 import하기
Base = declarative_base()

class SQLAlchemy:
    def __init__(self):
        print(DB_CONN)
        self.engine = create_engine(
            DB_CONN
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    def get_db(self):
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()


