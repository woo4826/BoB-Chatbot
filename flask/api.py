from fastapi import Depends, FastAPI, Request
import logging
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schema import Access_Data, User_Data
import database
import crud

#for web
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def access_view(request: Request, db: Session = Depends(database.SQLAlchemy().get_db)):
    template = 'index.html'
    context = {'request': request, 'ioc_list': crud.get_ioc(db)}
    return templates.TemplateResponse(template, context)


@app.post("/access")
async def access(access_item: Access_Data, Session=Depends(database.SQLAlchemy().get_db)):
    if crud.user_exists(access_item, Session) == True:
        crud.write_access_data(access_item, Session)
        return JSONResponse(content={"message": "Access data written to database", "status_code": 200})
    else:
        return JSONResponse(content={"message": "User not found", "status_code": 404})

@app.post("/user/create")
async def access(user_item: User_Data, Session=Depends(database.SQLAlchemy().get_db)):
    if crud.create_user(user_item, Session) == True:
        return {"message": "User data written to database"}
    else:
        return {"message": "User already exists"}

@app.get("/ioc")
async def get_ioc(Session=Depends(database.SQLAlchemy().get_db)):
    return JSONResponse(content={"access_data": crud.get_ioc(Session), "server_data": crud.get_server_data(),},status_code=200)
