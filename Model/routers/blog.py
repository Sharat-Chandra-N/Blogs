from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, database
from .repository import blog

router = APIRouter(tags=["Blogs"])

@router.get("/blogs", status_code=status.HTTP_200_OK)
def get_all_blogs(db:Session = Depends(get_db)):
    return blog.get_all(db)

@router.post("/create_blog", status_code=status.HTTP_201_CREATED, response_model=schema.ShowBlog)
def create_blog(request: schema.Blog, db:Session = Depends(database.get_db)):
    return blog.create(db, request)


@router.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schema.ShowBlog)
def get_blog(id, db:Session = Depends(database.get_db)):
    return blog.get(db, id)


@router.delete("/delete_blog/{id}", status_code=status.HTTP_200_OK)
def delete_blog(id, db:Session = Depends(database.get_db)):
    return blog.delete(id, db)


@router.put("/update_blog/{id}", status_code=status.HTTP_200_OK)
def update_blog(id, request: schema.Blog, db:Session = Depends(database.get_db)):
    return blog.update(id, request, db)
