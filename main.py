from fastapi import FastAPI
from Model import models, database
from Model.routers import blog, user

app = FastAPI()
app.include_router(blog.router)
app.include_router(user.router)

@app.get("/")
def index():
    return{"Application" : "Create and Read Blogs"}

models.Base.metadata.create_all(bind = database.engine)