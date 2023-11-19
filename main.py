from fastapi import FastAPI, Depends, status, Response
from typing import Optional
from Model import schema, models, database
from sqlalchemy.orm import Session

app = FastAPI()

@app.get("/")
def index():
    return{"Application" : "Create and Read Blogs"}

@app.get("/blogsqueryparameter")
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

@app.post("/create_blog", status_code=status.HTTP_201_CREATED)
def create_blog(request: schema.Blog, db:Session = Depends(get_db)):

    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return{"response": new_blog}

@app.get("/blogs", status_code=status.HTTP_200_OK)
def get_all_blogs(db:Session = Depends(get_db)):

    blogs = db.query(models.Blog).all()
    
    return{"response": blogs}

@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def get_blog(id, response: Response, db:Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{"response": "Blog not found"}
    
    return{"response": blog}