from ... import models, schema
from fastapi import status, HTTPException
from sqlalchemy.orm import Session

def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    
    return blogs

def create(db: Session, request: schema.Blog):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog

def get(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if blog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog Not Found")
    
    return blog

def delete(db: Session, id: int):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if blog.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog Not Found")
    
    blog.delete(synchronize_session=False)
    db.commit()
    
    return blog

def update(db: Session, id: int, request:schema.BaseModel):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if blog.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog Not Found")
    
    blog.update({"title": request.title, "body": request.body})
    db.commit()

    return "Updated"