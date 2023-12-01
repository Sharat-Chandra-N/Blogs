from fastapi import FastAPI, Depends, status, Response
from typing import Optional, List
from Model import schema, models, database, hashing
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/")
def index():
    return{"Application" : "Create and Read Blogs"}

@app.get("/blogsqueryparameter", tags=["blogs"])
def blogs_with_query_parameter(published: bool = True, limit: int = 25, sort: Optional[str] = None):
    if(published):
        return{"data": f'Published Posts {limit} are fetched {sort}'}
    else:   
        return{"data": f'Unpublished Posts {limit} are fetched {sort}'}

models.Base.metadata.create_all(bind = database.engine)

def get_db(): 
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/create_blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create_blog(request: schema.Blog, db:Session = Depends(get_db)):

    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return{"response": new_blog}

@app.get("/blogs", status_code=status.HTTP_200_OK, tags=["blogs"])
def get_all_blogs(db:Session = Depends(get_db)):

    blogs = db.query(models.Blog).all()
    
    return{"response": blogs}

@app.get("/blog/{id}", status_code=status.HTTP_200_OK, response_model=schema.ShowBlog, tags=["blogs"])
def get_blog(id, response: Response, db:Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"response": "Blog not found"}
    
    return blog

@app.delete("/delete_blog/{id}", status_code=status.HTTP_200_OK, tags=["blogs"])
def delete_blog(id, response: Response, db:Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"response": "Blog not found"}
    
    blog.delete(synchronize_session=False)
    db.commit()

    return{"response": "Blog Deleted"}

@app.put("/update_blog/{id}", status_code=status.HTTP_200_OK, tags=["blogs"])
def update_blog(id, request: schema.Blog, response: Response, db:Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"response": "Blog not found"}
    
    blog.update({"title": request.title, "body": request.body})
    db.commit()

    return{"response": "Blog Updated"}

@app.post("/create_user", status_code=status.HTTP_200_OK, response_model=schema.ShowUser, tags=["users"])
def create_user(request: schema.User, db:Session = Depends(get_db)):

    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.create_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schema.ShowUser, tags=["users"])
def get_user(id, response: Response, db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"response": "User not found"}
    
    return user