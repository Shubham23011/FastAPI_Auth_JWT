from fastapi import FastAPI,Depends,HTTPException,status
from pydantic import BaseModel
from typing import Annotated,List
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import auth
from auth import get_current_user




app = FastAPI()
app.include_router(auth.router)


models.Base.metadata.create_all(bind=engine)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



@app.get("/",status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db : db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return {"User" : user}
