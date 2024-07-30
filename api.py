from fastapi import Depends, FastAPI
import logging
from sqlalchemy.orm import Session

from schema import Access_Data
import database
from sqlalchemy import create_engine
import crud
app = FastAPI()

@app.get("/")
async def root():
    logging.info("Hello World")
    return {"message": "Hello World"}

@app.post("/access")
async def access(access_item: Access_Data,Session = Depends(database.SQLAlchemy().get_db)):
    print(access_item)
    crud.write_access_data(access_item, Session)
    
    return {"message": "Access data written to database"}