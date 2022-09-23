from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config.db import get_db
from services.user_services import User_Service
from schemas import user_schema
from utils import validations, oauth2

router = APIRouter(
    prefix="/Users",
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=user_schema.Response_User)
def CREATE_USER(request: user_schema.User, db: Session = Depends(get_db)):

    if validations.check_email(request.email) == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Email")
    return User_Service.create(request, db)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=user_schema.Response_User)
def GET_USER(id, db: Session = Depends(get_db), current_user: user_schema.User = Depends(oauth2.get_current_user)):
    return User_Service.get_user(id, db)
