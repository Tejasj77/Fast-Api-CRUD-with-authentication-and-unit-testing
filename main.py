from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
import auth
from auth import get_current_user

app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)

# Validations
class BlogBase(BaseModel):
    title:str
    content:str
    user_id:int

class UserBase(BaseModel):
    username:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated(Session,Depends(get_db))
user_dependency = Annotated(dict,Depends(get_current_user))

@app.post("/users/",status_code=status.HTTP_201_CREATED)
async def create_user(user:user_dependency,db:db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.get("/users/${user_id}",status_code=status.HTTP_200_OK)
async def read_user(user_id:int,user:user_dependency,db:db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail='User not found')
    return user

@app.post("/blogs",status_code=status.HTTP_201_CREATED)
async def create_blog(blog:BlogBase,user:user_dependency,db:db_dependency):
    db_blog = models.Blog(**blog.dict())
    db.add(db_blog)
    db.commit()

@app.get("/blogs/{blog_id}",status_code=status.HTTP_200_OK)
async def read_blog(blog_id:int,user:user_dependency,db:db_dependency):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404,detail='blog was not found')
    return blog

@app.delete("/blogs/{blog_id}",status_code=status.HTTP_200_OK)
async def delete_blog(blog_id:int,user:user_dependency,db:db_dependency):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=404,detail="blog was not found")
    db.delete(db_blog)
    db.commit()