from fastapi import Depends, FastAPI, Request, logger
import logging
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from schema import Access_Data, IoC_Data, IoC_Log, User_Data
import database
import crud

# for web
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import vt

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def access_view(request: Request, db: Session = Depends(database.SQLAlchemy().get_db)):
    template = "index.html"

    context = {"request": request, "ioc_list": reversed(crud.get_ioc(db)), "server_data": crud.get_server_data(),"user_list": crud.get_users(db)}
    # context = {"request": request,  "server_data": crud.get_server_data(),}

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
        return  JSONResponse(content= {"message": "User data written to database", "status_code": 200})
    else:
        return  JSONResponse(content={"message": "User already exists", "status_code": 402})


@app.get("/ioc")
async def get_ioc(Session=Depends(database.SQLAlchemy().get_db)):
    return JSONResponse(
        content={
            "access_data": crud.get_ioc(Session),
            "server_data": crud.get_server_data(),
        },
        status_code=200,
    )

@app.post('/ioc/log/create')
async def get_ioc(data: IoC_Log,Session=Depends(database.SQLAlchemy().get_db)):
    crud.write_ioc_log(data, Session)
    return JSONResponse(content={"message": "IoC log written to database", "status_code": 200})