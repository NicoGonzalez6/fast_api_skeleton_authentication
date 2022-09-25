

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from models import models
from config.db import get_db
from utils import bcrypt, token


router = APIRouter(
    tags=["Authentication"]
)


@router.post('/login')
def Login_User(request:  OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"not user found with email {request.username}")
    if bcrypt.Hash.verify_password(request.password, user.password) == False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid credentials")
    access_token = token.Token.create_access_token(
        data={"sub": user.email, "id": user.id, "role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer", "user": {"email": user.email, "name": user.name, "role": user.role}}
