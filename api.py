from fastapi import Depends, FastAPI
import logging
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schema import Access_Data, User_Data
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
    if crud.user_exists(access_item, Session) == True:
        crud.write_access_data(access_item, Session)
        return JSONResponse(content={"message": "Access data written to database","status_code":200})
    else:
        return JSONResponse(content={"message": "User not found","status_code":404})
        
    

@app.post("/user/create")
async def access(user_item:User_Data,Session = Depends(database.SQLAlchemy().get_db)):
    if crud.create_user(user_item, Session) == True:
        return {"message": "User data written to database"}
    else :
        return {"message": "User already exists"}