from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import config

DB_HOST = config["DB_HOST"]
DB_USER = config["DB_USER"]
DB_PORT = config["DB_PORT"]
DB_PASS = config["DB_PASS"]

DB_CONN = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/chatbot"
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



