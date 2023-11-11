from fastapi import FastAPI
from typing import Optional

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