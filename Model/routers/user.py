from fastapi import APIRouter, status, Depends, Response, HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, database, hashing

router = APIRouter(
    tags=["Users"]
)

@router.post("/create_user", status_code=status.HTTP_200_OK, response_model=schema.ShowUser)
def create_user(request: schema.User, db:Session = Depends(database.get_db)):

    new_user = models.User(name=request.name, email=request.email, password=hashing.Hash.create_hash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/user/{id}", status_code=status.HTTP_200_OK, response_model=schema.ShowUser)
def get_user(id, response: Response, db:Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    
    return user