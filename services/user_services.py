from unicodedata import name
from sqlalchemy.orm import Session
from schemas import user_schema
from models import models
from fastapi import status, HTTPException
from utils import bcrypt


class User_Service():
    def create(request: user_schema.User, db: Session):
        hashed_password = bcrypt.Hash.hash_password(request.password)
        new_user = models.User(
            name=request.name, email=request.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def get_user(id: int, db: Session):
        user = db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with id {id}")
        return user
