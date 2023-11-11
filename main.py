from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return{"Application" : "Create and Read Blogs"}