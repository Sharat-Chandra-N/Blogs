from typing import Optional
from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = True

class User(BaseModel):
    name: str
    email: str
    password: str